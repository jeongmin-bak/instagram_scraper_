from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from instaid_app.models import id_Board, Instaid
from django.urls import reverse
import datetime
import xlwt
import requests, json, re, time
import math
# Create your views here.

def post(request):
    boards = {'boards': id_Board.objects.all()}
    return render(request, 'instaid_app/list.html', boards)

def board(request):
    if request.method == "POST":
        author = request.POST['author']
        instaid = request.POST['insta_id']
        query_hash = request.POST['query']
        cw_count = request.POST['count']

        # 게시물 데이터베이스 저장
        id_board = id_Board(author=author, keyword=instaid, count=cw_count, query=query_hash)
        id_board.save()
        data_json(instaid, int(cw_count), query_hash)

        return HttpResponseRedirect(reverse('instaidapp:id_board'))
    else:
        return render(request, 'instaid_app/write.html')

def detail(request, id):
    try:
        board = id_Board.objects.get(pk=id)
    except id_Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'instaid_app/detail.html', {'board': board})

def data_json(instaid, number, query):

    # 팔로워 수, 팔로우 수, 사용자 query i 획득
    header = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'ig_did=D1DE0A39-B59A-48A7-93E9-6E772C11677F; ig_nrcb=1; mid=YSNChwALAAHcg2qvR_y07V_zsx7K; fbm_124024574287414=base_domain=.instagram.com; datr=WUE2Yad0NDCn_G1ksFtdxcM4; ds_user_id=1979016495; csrftoken=YJ9jWWyrHaJyD0vl2MWAI031Os1P1Gq3; shbid="4334\0541979016495\0541664264534:01f70ba3d18472dc38718682283cea21b8360a2697c5f16f56e35b7de4d333abcf4f3035"; shbts="1632728534\0541979016495\0541664264534:01f79d84129a2620cb11c56428f8377a729ae7603f203f7263e2242dfdee52901ad65b64"; sessionid=1979016495%3AYT01JDT2JQd2X0%3A13; rur="VLL\0541979016495\0541664422429:01f7bf8e471169f785d393aa05fb4aec13fbf6c1cdd3aed17a2572dfb3d2e2573734fbed"',
        'referer': 'https://www.instagram.com/explore/tags/nike/',
        'sec-ch-ua': '""Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93""',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'x-asbd-id': '198387',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR01x9G6D8yE4YzI-iMSd2isxXngO3-DG1H6IutAzy5ZbyKL',
        'x-requested-with': 'XMLHttpRequest'
    }
    # header값 끝

    dataList = []

    URL = 'https://www.instagram.com/{0}/?__a=1'.format(instaid)
    res = requests.get(URL, headers=header)
    res = res.json()
    #res = res['graphql']['user']

    # 사용자 팔로워 수
    follower= res['graphql']['user']['edge_followed_by']['count']

    # 사용자 팔로잉 수
    following = res['graphql']['user']['edge_follow']['count']

    # 사용자 query id
    query_id = res['logging_page_id']
    query_id = re.sub(r'[^0-9]', '', query_id)

    MAX_PAGES = math.ceil(number/11)
    # instaid / number / query

    has_next_page = True

    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'
        end_cursor = ''
        count = 0

        # Use has_bext_page while loop to scrape all posts
        while count < MAX_PAGES:
            # while has_next_page: #for count in range(1, 4):
            print('PAGE: ', count)
            user_data = {}

            if count == 1:  # The profile page
                profile = 'https://www.instagram.com/' + instaid
            else:  # subsequent infinite scroll requests
                profile = 'https://www.instagram.com/graphql/query/?query_hash=' + query + '&variables={"id":"' + query_id + '","first":12,"after":"' + end_cursor + '"}'
            r = s.get(profile)
            print(profile)
            time.sleep(8)

            # 기존 데이터 추가
            user_data['crawling_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            user_data['insta_id'] = instaid
            user_data['follower'] = follower
            user_data['following'] = following

            if count == 1:  # Profile page
                data = re.search(
                    r'window._sharedData = (\{.+?});</script>', r.text).group(1)
                data = json.loads(data)

                data_point = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']
            else:  # subsequent infinite scroll requests
                data = json.loads(r.text)['data']
                data_point = data['user']['edge_owner_to_timeline_media']

            # Extract data and find the end cursor for the current page
            end_cursor = data_point['page_info']['end_cursor']
            has_next_page = data_point['page_info']['has_next_page']

            # 본문 내용 시작
            for link in data_point['edges']:
                # 게시물 타입
                user_data['media_type'] = link['node']['__typename']

                # 게시물 링크
                user_data['post_link'] = 'https://www.instagram.com' + '/p/' + link['node']['shortcode'] + '/'

                # 게시물 작성 시간
                post_time = link['node']['taken_at_timestamp']
                user_data['post_date'] = datetime.datetime.fromtimestamp(post_time).strftime('%Y-%m-%d %a %H:%M')

                # 본문 내용
                try:
                    user_data['caption'] = link['node']['edge_media_to_caption']['edges'][0]['node']['text']
                except:
                    user_data['caption'] = 'none'

                # 좋아요 수
                user_data['like'] = link['node']['edge_media_preview_like']['count']

                try:
                    user_data['comments_cnt'] = link['node']['edge_media_to_comment']['count']

                except:

                    user_data['comments_cnt'] = 0

                user_data['image_link'] = link['node']['display_url']

            dataList.append(user_data)
            count += 1
        print(dataList)




def export_users_xls(request,id):
    board = id_Board.objects.get(pk=id)
    response = HttpResponse(content_type='application/ms-excel')
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls'
    wb = xlwt.Workbook(encoding='ansi')
    ws = wb.add_sheet('sheet1')

    row_num = 0
    col_names = ['insta_id','crawling_date','profile','media_type','media_url','media_views','media_title','comments_cnt','like_cnt']

    # 열이름을 첫번째 행에 추가 시켜준다.
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name)

    rows = Instaid.objects.filter(insta_id=board.keyword).values_list('insta_id','crawling_date','profile','media_type','media_url','media_views','media_title','comments_cnt','like_cnt')
    for row in rows:
        row_num += 1
        for col_num, attr in enumerate(row):
            ws.write(row_num, col_num, attr)

    wb.save(response)

    return response



