from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from instaid_app.models import id_Board
from django.urls import reverse
import xlwt
import requests
import math
# Create your views here.

def post(request):
    boards = {'boards': id_Board.objects.all()}
    return render(request, 'instaid_app/list.html', boards)

def board(request):
    if request.method == "POST":
        author = request.POST['author']
        instaid = request.POST['insta_id']
        cw_count = request.POST['count']
        id_board = id_Board(author=author, keyword=instaid, count=cw_count)
        id_board.save()
        json(instaid, int(cw_count))

        return HttpResponseRedirect(reverse('instaidapp:id_board'))
    else:
        return render(request, 'instaid_app/write.html')

def detail(request, id):
    try:
        board = id_Board.objects.get(pk=id)
    except id_Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'instaid_app/detail.html', {'board': board})

def json(instaid, number):
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
    res = res['graphql']['user']

    for video in res['edge_felix_video_timeline']['edges']:
        video = video['node']
        data = {}

        # 인스타 계정 id
        data['insta_id'] = re['username']

        # 수집날짜
        data['crawling_date'] = datetime.now().strftime("%Y-%m-%d")

        # 인스타 계정 이름
        data['profile'] = re['full_name']

        # 미디어타입
        data['media_type'] = video['__typename']

        # 2. display_url -> video link
        data['media_url'] = video['display_url']

        # 3. video 조회수
        data['views'] = video['video_view_count']

        # 4. video title
        try:
            data['media_title'] = video['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            data['media_title'] = ''

        # 5. video comments cnt
        data['comments_cnt'] = video['edge_media_to_comment']['count']

        # 6. video like cnt
        data['like_cnt'] = video['edge_liked_by']['count']

        dataList.append(data)

        id = data['insta_id']
        crawling_date = data['crawling_date']
        profile = data['profile']
        media_type = data['media_type']
        media_url = data['media_url']
        media_views = data['views']
        media_title = data['media_title']
        comments_cnt = data['comments_cnt']
        like_cnt = data['like_cnt']

        info = Keyword()


    for media in res['edge_owner_to_timeline_media']['edges']:
        media = media['node']
        m_data = {}

        # 인스타 계정 id
        m_data['insta_id'] = re['username']

        # 수집날짜
        m_data['crawling_date'] = datetime.now().strftime("%Y-%m-%d")

        # 인스타 계정 이름
        m_data['profile'] = re['full_name']

        # 미디어타입
        m_data['media_type'] = media['__typename']

        # 2. display_url -> media link
        m_data['media_url'] = media['display_url']

        # 3. media 조회수
        m_data['views'] = "none"

        # 4. media title
        try:
            m_data['media_title'] = media['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            m_data['media_title'] = ''

        # 5. media comments cnt
        m_data['comments_cnt'] = media['edge_media_to_comment']['count']

        # 6. media like cnt
        m_data['like_cnt'] = media['edge_liked_by']['count']

        dataList.append(m_data)


