from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from instaid_app.models import id_Board, Instaid, instagram_data
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
#     header = {
#     'accept': '*/*',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
#     'cookie': 'mid=YSXU5gALAAG_urUEo7e_R9CStRxH; ig_did=87649B4F-5B8B-4006-AC5C-CA1CD74066FD; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; datr=pd0xYVlBmIDyHJyjQwIb0xVQ; shbid="1369\0543270410388\0541669254271:01f795819803ace75d8540469caf4a6b51fc07a6c77bf721d1aab1868e54cc2b2c6dcb61"; shbts="1637718271\0543270410388\0541669254271:01f76bb9ac8dc4de8352f0b0c01ba84fe56d925f4fad1815102afee6ede31fcef7b76082"; fbsr_124024574287414=3bHBcveh4j8qzNumAbBvCdMgcylUQbagOGWDeSrfouA.eyJ1c2VyX2lkIjoiMTAwMDA0ODM5NDIxMzA0IiwiY29kZSI6IkFRQUY0UkFrSU56U3l3bWxPSVI4TlMzckY3Nk1LdlVjQzMza1pDU0IzQ1RvXzZ6Snl2M09ZZmpNOFQzTGF0bktnWDNYQklsemgtS3Zxb1VRT3hUVjF3TC04eWZDYzJNd3VNM0MtWTJxWU14RWVPeUt6OWpzWm9CSHpZek5mbzNyUlFqMlJlV0JsM2VNTjNJNjRFVlcya2dYOExVSDJrTF9xNkpqb0dnUE5YLWtBTmdwM3FaN0ktcE84SHhIcXVtVV9vTUlGajRtSEhYTTk4YWdfMEtBTXlwdVBXT0ZBUktDYmt3YUw2bTM0ZzIxQ1ZiXzZaOUtwZFFaZmZhZDVERjNvdmZqV3VLLWVLQ0FUcm92bkM1ZXJxU29ja2dJNWJVeVFEM29NYUV6U0dUa3RXUlFwSFFYenVNQXBjczNMRzVRbmk0eXFKUjBKQUdJV2NPX080bkw2dTgzIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUhDRThLUFVMc3puU2Rzd2tTQno4N1RDNTdESG4wUlF4anJUb2JXRWNWM1hmVkJRVWU3elpBYVREYWJYd3NucHlYVGl4M0lySUZlZk9yOXg1VGVnY1Q1SVNwT2VBVGk5QTdweGNmWkMzbFdLaEVUQWpFYmpwYkxJQ2I2bjlZMm1hSTVua0dSbEVFU3o1VWEzWDRDNlBLYWpIcnVUNjN3dzhRM1NkeGRXRXJUamY0OTlvWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYzNzgzMTgyNn0; fbsr_124024574287414=3bHBcveh4j8qzNumAbBvCdMgcylUQbagOGWDeSrfouA.eyJ1c2VyX2lkIjoiMTAwMDA0ODM5NDIxMzA0IiwiY29kZSI6IkFRQUY0UkFrSU56U3l3bWxPSVI4TlMzckY3Nk1LdlVjQzMza1pDU0IzQ1RvXzZ6Snl2M09ZZmpNOFQzTGF0bktnWDNYQklsemgtS3Zxb1VRT3hUVjF3TC04eWZDYzJNd3VNM0MtWTJxWU14RWVPeUt6OWpzWm9CSHpZek5mbzNyUlFqMlJlV0JsM2VNTjNJNjRFVlcya2dYOExVSDJrTF9xNkpqb0dnUE5YLWtBTmdwM3FaN0ktcE84SHhIcXVtVV9vTUlGajRtSEhYTTk4YWdfMEtBTXlwdVBXT0ZBUktDYmt3YUw2bTM0ZzIxQ1ZiXzZaOUtwZFFaZmZhZDVERjNvdmZqV3VLLWVLQ0FUcm92bkM1ZXJxU29ja2dJNWJVeVFEM29NYUV6U0dUa3RXUlFwSFFYenVNQXBjczNMRzVRbmk0eXFKUjBKQUdJV2NPX080bkw2dTgzIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUhDRThLUFVMc3puU2Rzd2tTQno4N1RDNTdESG4wUlF4anJUb2JXRWNWM1hmVkJRVWU3elpBYVREYWJYd3NucHlYVGl4M0lySUZlZk9yOXg1VGVnY1Q1SVNwT2VBVGk5QTdweGNmWkMzbFdLaEVUQWpFYmpwYkxJQ2I2bjlZMm1hSTVua0dSbEVFU3o1VWEzWDRDNlBLYWpIcnVUNjN3dzhRM1NkeGRXRXJUamY0OTlvWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYzNzgzMTgyNn0; csrftoken=cy9G8yzq7or4IE9WzBCRddnleABNTrhs; ds_user_id=50700987067; sessionid=50700987067:rzZWQ2I7XgVYYR:20; rur="VLL\05450700987067\0541669368170:01f73dce05ae137d9b0623604864513062f6d853eb3490735803c3f8acd52418632c18b3"',
#     'referer': 'https://www.instagram.com/explore/tags/nike/',
#     'sec-ch-ua': '""Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93""',
#     'sec-ch-ua-mobile': '?0',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
#     'x-asbd-id': '198387',
#     'x-ig-app-id': '936619743392459',
#     'x-ig-www-claim': 'hmac.AR01x9G6D8yE4YzI-iMSd2isxXngO3-DG1H6IutAzy5ZbyKL',
#     'x-requested-with': 'XMLHttpRequest'
#     }
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
            #print('PAGE: ', count)
            user_data = {}

            if count == 1:  # The profile page
                profile = 'https://www.instagram.com/' + instaid
            else:  # subsequent infinite scroll requests
                profile = 'https://www.instagram.com/graphql/query/?query_hash=' + query + '&variables={"id":"' + query_id + '","first":12,"after":"' + end_cursor + '"}'
            r = s.get(profile)
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

                crawling_date = user_data['crawling_date']
                insta_id = user_data['insta_id']
                user_follower = user_data['follower']
                user_following = user_data['following']
                media_type = user_data['media_type']
                post_link = user_data['post_link']
                post_date = user_data['post_date']
                caption = user_data['caption']
                like_cnt = user_data['like']
                comments_cnt = user_data['comments_cnt']
                image_link = user_data['image_link']

                insta_data = instagram_data(crawling_date=crawling_date, insta_id=insta_id, follower=user_follower,
                                            following=user_following, media_type=media_type, post_link=post_link,
                                            post_date=post_date, caption=caption, like_cnt=like_cnt,
                                            comments_cnt=comments_cnt, image_url=image_link)
                insta_data.save()

            dataList.append(user_data)
            count += 1

            # 데이터베이스에 저장


def export_users_xls(request,id):
    board = id_Board.objects.get(pk=id)
    response = HttpResponse(content_type='application/ms-excel')
    response["Content-Disposition"] = "attachment;filename*=UTF-8\'\'"  + board.keyword +'.xls'
    wb = xlwt.Workbook(encoding='ansi')
    ws = wb.add_sheet('sheet1')

    row_num = 0
    col_names = ['crawling_date', 'insta_id','follower','following','media_type','post_link','post_date','caption','like_cnt','comments_cnt','image_url']

    # 열이름을 첫번째 행에 추가 시켜준다.
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name)

    rows = instagram_data.objects.filter(insta_id=board.keyword).values_list('crawling_date', 'insta_id','follower','following','media_type','post_link','post_date','caption','like_cnt','comments_cnt','image_url')
    for row in rows:
        row_num += 1
        for col_num, attr in enumerate(row):
            ws.write(row_num, col_num, attr)

    wb.save(response)

    return response



