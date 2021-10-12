from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django.urls import reverse
from board_app.models import Board, Keyword
import xlwt
import requests
import math

def post(request):
    boards = {'boards': Board.objects.all()}
    return render(request, 'board_app/list.html', boards)

def board(request):
    if request.method == "POST":
        author = request.POST['author']
        keyword = request.POST['keyword']
        content = request.POST['content']
        board = Board(author=author, keyword=keyword, content=content)
        board.save()
        json(keyword, int(content))
        #board.save()

        return HttpResponseRedirect(reverse('boardapp:board'))
    else:
        return render(request, 'board_app/write.html')

def detail(request, id):
    try:
        board = Board.objects.get(pk=id)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'board_app/detail.html', {'board': board})

def json(keyword, content):
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
    #header값 끝

    dataList = []
    URL = 'https://www.instagram.com/explore/tags/{0}/?__a=1'.format(keyword)

    count = math.ceil(content/30)
    i = 0
    while(i < count):
        res = requests.get(URL, headers=header)
        res = res.json()

        if 'next_page' not in res['data']['recent'].keys() or int(res['data']['recent']['next_page']) == 0:
            break
        max_id = res['data']['recent']['next_max_id']

        for n in res['data']['recent']['sections']:
            for m in ((n['layout_content']['medias'])):
                m = m['media']
                data = {}

                # hashtag
                data['hashtag'] = keyword

                # 게시글 작성 일자(date)
                try:
                    data['Date'] = datetime.fromtimestamp(m['caption']['created_at'])
                except:
                    continue

                # number
                data['number'] = str(m['user']['pk'])

                # insta_id
                data['insta_id'] = (m['user']['username'])

                # profile
                data['profile'] = (m['user']['full_name'])

                # contents
                data['contents'] = m['caption']['text']

                # like_cnt
                data['like'] = (m['like_count'])

                # comment_cnt, comments
                try:
                    data['comments_cnt'] = (m['comment_count'])
                    temp = []
                    if int(data['comments_cnt']) == 0:
                        data['comments'] = []
                    else:
                        for j in range(0, int(data['comments_cnt'])):
                            temp.append(m['comments'][j]['text'])
                        result = " ".join(temp)
                        data['comments'] = result

                except:
                    data['comments_cnt'] = 0
                    data['comments'] = []

                # feed_url
                data['URL'] = 'https://www.instagram.com/p/' + m['code'] + "/"

                dataList.append(data)

                hashtag = data['hashtag']
                url = data['URL']
                Date = data['Date']
                contents = data['contents']
                comments_cnt = data['comments_cnt']
                comments = data['comments']
                like = data['like']
                profile = data['profile']
                number = data['number']
                insta_id = data['insta_id']

                info = Keyword(keyword=hashtag, url=url, writeData=Date, content=contents, reply=comments_cnt, replyList=comments, like=like, user_name=profile, user_pk=number, user_id=insta_id)
                info.save()
        i = i+1
        URL = 'https://www.instagram.com/explore/tags/' + keyword + '/?__a=1&max_id=' + max_id

def export_users_xls(request,id):
    board = Board.objects.get(pk=id)
    response = HttpResponse(content_type='application/ms-excel')
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls'
    wb = xlwt.Workbook(encoding='ansi')
    ws = wb.add_sheet('sheet1')

    row_num = 0
    col_names = ['hashtag', 'Date', 'number','insta_id','profile','contents','like','comments_cnt','comments','url']

    # 열이름을 첫번째 행에 추가 시켜준다.
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name)

    #rows = Keyword.objects.filter(keyword=board.keyword).values_list(,'url','writeData','content','reply','replyList','like','user_name',)
    rows = Keyword.objects.filter(keyword=board.keyword).values_list('keyword','writeData','user_pk','user_id','user_name','content','like','reply','replyList','url')
    for row in rows:
        row_num += 1
        for col_num, attr in enumerate(row):
            ws.write(row_num, col_num, attr)

    wb.save(response)

    return response