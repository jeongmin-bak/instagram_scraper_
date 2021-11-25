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
    'cookie': 'mid=YSXU5gALAAG_urUEo7e_R9CStRxH; ig_did=87649B4F-5B8B-4006-AC5C-CA1CD74066FD; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; datr=pd0xYVlBmIDyHJyjQwIb0xVQ; shbid="1369\0543270410388\0541669254271:01f795819803ace75d8540469caf4a6b51fc07a6c77bf721d1aab1868e54cc2b2c6dcb61"; shbts="1637718271\0543270410388\0541669254271:01f76bb9ac8dc4de8352f0b0c01ba84fe56d925f4fad1815102afee6ede31fcef7b76082"; fbsr_124024574287414=3bHBcveh4j8qzNumAbBvCdMgcylUQbagOGWDeSrfouA.eyJ1c2VyX2lkIjoiMTAwMDA0ODM5NDIxMzA0IiwiY29kZSI6IkFRQUY0UkFrSU56U3l3bWxPSVI4TlMzckY3Nk1LdlVjQzMza1pDU0IzQ1RvXzZ6Snl2M09ZZmpNOFQzTGF0bktnWDNYQklsemgtS3Zxb1VRT3hUVjF3TC04eWZDYzJNd3VNM0MtWTJxWU14RWVPeUt6OWpzWm9CSHpZek5mbzNyUlFqMlJlV0JsM2VNTjNJNjRFVlcya2dYOExVSDJrTF9xNkpqb0dnUE5YLWtBTmdwM3FaN0ktcE84SHhIcXVtVV9vTUlGajRtSEhYTTk4YWdfMEtBTXlwdVBXT0ZBUktDYmt3YUw2bTM0ZzIxQ1ZiXzZaOUtwZFFaZmZhZDVERjNvdmZqV3VLLWVLQ0FUcm92bkM1ZXJxU29ja2dJNWJVeVFEM29NYUV6U0dUa3RXUlFwSFFYenVNQXBjczNMRzVRbmk0eXFKUjBKQUdJV2NPX080bkw2dTgzIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUhDRThLUFVMc3puU2Rzd2tTQno4N1RDNTdESG4wUlF4anJUb2JXRWNWM1hmVkJRVWU3elpBYVREYWJYd3NucHlYVGl4M0lySUZlZk9yOXg1VGVnY1Q1SVNwT2VBVGk5QTdweGNmWkMzbFdLaEVUQWpFYmpwYkxJQ2I2bjlZMm1hSTVua0dSbEVFU3o1VWEzWDRDNlBLYWpIcnVUNjN3dzhRM1NkeGRXRXJUamY0OTlvWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYzNzgzMTgyNn0; fbsr_124024574287414=3bHBcveh4j8qzNumAbBvCdMgcylUQbagOGWDeSrfouA.eyJ1c2VyX2lkIjoiMTAwMDA0ODM5NDIxMzA0IiwiY29kZSI6IkFRQUY0UkFrSU56U3l3bWxPSVI4TlMzckY3Nk1LdlVjQzMza1pDU0IzQ1RvXzZ6Snl2M09ZZmpNOFQzTGF0bktnWDNYQklsemgtS3Zxb1VRT3hUVjF3TC04eWZDYzJNd3VNM0MtWTJxWU14RWVPeUt6OWpzWm9CSHpZek5mbzNyUlFqMlJlV0JsM2VNTjNJNjRFVlcya2dYOExVSDJrTF9xNkpqb0dnUE5YLWtBTmdwM3FaN0ktcE84SHhIcXVtVV9vTUlGajRtSEhYTTk4YWdfMEtBTXlwdVBXT0ZBUktDYmt3YUw2bTM0ZzIxQ1ZiXzZaOUtwZFFaZmZhZDVERjNvdmZqV3VLLWVLQ0FUcm92bkM1ZXJxU29ja2dJNWJVeVFEM29NYUV6U0dUa3RXUlFwSFFYenVNQXBjczNMRzVRbmk0eXFKUjBKQUdJV2NPX080bkw2dTgzIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUhDRThLUFVMc3puU2Rzd2tTQno4N1RDNTdESG4wUlF4anJUb2JXRWNWM1hmVkJRVWU3elpBYVREYWJYd3NucHlYVGl4M0lySUZlZk9yOXg1VGVnY1Q1SVNwT2VBVGk5QTdweGNmWkMzbFdLaEVUQWpFYmpwYkxJQ2I2bjlZMm1hSTVua0dSbEVFU3o1VWEzWDRDNlBLYWpIcnVUNjN3dzhRM1NkeGRXRXJUamY0OTlvWkQiLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYzNzgzMTgyNn0; csrftoken=cy9G8yzq7or4IE9WzBCRddnleABNTrhs; ds_user_id=50700987067; sessionid=50700987067:rzZWQ2I7XgVYYR:20; rur="VLL\05450700987067\0541669368170:01f73dce05ae137d9b0623604864513062f6d853eb3490735803c3f8acd52418632c18b3"',
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