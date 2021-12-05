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

        return HttpResponseRedirect(reverse('boardapp:board'))
    else:
        return render(request, 'board_app/write.html')

def detail(request, id):
    try:
        board = Board.objects.get(pk=id)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'board_app/detail.html', {'board': board})

def json(keyword, number):
    header = {
        'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'mid=YT9iBwALAAH3fBwN4E2AFyQnSse3; ig_did=3D563871-0F4D-4685-96A1-5F249BBFA080; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; fbsr_124024574287414=y1CJMq0CasTxPPX22LzHEOy5zxRDxtl2CCKw5GZ74TM.eyJ1c2VyX2lkIjoiMTAwMDA0ODM5NDIxMzA0IiwiY29kZSI6IkFRRE95b3ktSjRsYktzaGhnSkxOMFo0bW4wRXRLRjZBRW0zSUgyNEFITXNHVHZDRUlyUTFEMTZDTmJRYmllUnJUMjZsZ1ppakk5Zy0xOFpTUnR2bWtsYzZqRDZkQlNhRWU2SGV3MXRBb2dLd3l5QzRlMGF1azBObXdSRm4xLXRwWE9vc0xxbHRQUl9rQU81MUk0SEpYOTFhRm44Rl9rQm5yNXpqUmxVUkp6YVFJRk0tNGFYWEZyS2t5eFBnVDN4RTQtX3FOMk41ckVWeEw3UkNNZmgtZFVtVl91RE9RMTBsc054MmdvU2x1ckxmX3JQM1pGU0I0dDBFQUhDRTZySFhxd2lIdzA4YThmZDNaU01MZDFTNnN0S1V5UzhmVkVZSk1DLXJ2T1RaQndxeWZtUjFuLXhLLThEMWUyVEVZY0F2VEQ4T3dpd2YwNTZVU0VHZllmQkotTURXIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQU44OWVLSEdrREZHR3pkM2dTVFpBWUt1b05ZRHF5YW9lS0k5YUYyV2paQWZQWkJQM0lCYWxMZ1d5WGF6Qmx3dFM5aFZ6b1lIdnA5M0I5Nk82elpCcVdsaTRaQWJaQTBmNEpKOXB3NmFwQjhCS2dKNnJxVUZLRFNwb2oya2xmOE1jclY5ZDRoQ1EwUFVaQUtjVWFMS091RkN6U0lkOWpsUkU2S3RaQ3IxVkxzREtXN3c3NnczTDg0Qzc4OU11ZEY3b1FaRFpEIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE2Mzg2ODk5MzF9; csrftoken=1QUT2KxORftJvf3TFQNwuBgM52IbFYc3; ds_user_id=50700987067; sessionid=50700987067:3VcyaT7WVTxROM:22; fbsr_124024574287414=y1CJMq0CasTxPPX22LzHEOy5zxRDxtl2CCKw5GZ74TM.eyJ1c2VyX2lkIjoiMTAwMDA0ODM5NDIxMzA0IiwiY29kZSI6IkFRRE95b3ktSjRsYktzaGhnSkxOMFo0bW4wRXRLRjZBRW0zSUgyNEFITXNHVHZDRUlyUTFEMTZDTmJRYmllUnJUMjZsZ1ppakk5Zy0xOFpTUnR2bWtsYzZqRDZkQlNhRWU2SGV3MXRBb2dLd3l5QzRlMGF1azBObXdSRm4xLXRwWE9vc0xxbHRQUl9rQU81MUk0SEpYOTFhRm44Rl9rQm5yNXpqUmxVUkp6YVFJRk0tNGFYWEZyS2t5eFBnVDN4RTQtX3FOMk41ckVWeEw3UkNNZmgtZFVtVl91RE9RMTBsc054MmdvU2x1ckxmX3JQM1pGU0I0dDBFQUhDRTZySFhxd2lIdzA4YThmZDNaU01MZDFTNnN0S1V5UzhmVkVZSk1DLXJ2T1RaQndxeWZtUjFuLXhLLThEMWUyVEVZY0F2VEQ4T3dpd2YwNTZVU0VHZllmQkotTURXIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQU44OWVLSEdrREZHR3pkM2dTVFpBWUt1b05ZRHF5YW9lS0k5YUYyV2paQWZQWkJQM0lCYWxMZ1d5WGF6Qmx3dFM5aFZ6b1lIdnA5M0I5Nk82elpCcVdsaTRaQWJaQTBmNEpKOXB3NmFwQjhCS2dKNnJxVUZLRFNwb2oya2xmOE1jclY5ZDRoQ1EwUFVaQUtjVWFMS091RkN6U0lkOWpsUkU2S3RaQ3IxVkxzREtXN3c3NnczTDg0Qzc4OU11ZEY3b1FaRFpEIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE2Mzg2ODk5MzF9; rur="VLL\05450700987067\0541670225964:01f702d7baa010e391b5588d677c7867e826189421b5f72ac60a6bb5b9c483e802101c29"',
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

    count = math.ceil(number/30)
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
                try:
                    data['profile'] = (m['user']['full_name'])
                except:
                    data['profile'] = []

                # contents
                try:
                    data['contents'] = m['caption']['text']
                except:
                    data['contents'] = []

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
