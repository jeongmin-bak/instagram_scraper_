from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from instaid_app.models import id_Board
from django.urls import reverse
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
        return HttpResponseRedirect(reverse('instaidapp:id_board'))
    else:
        return render(request, 'instaid_app/write.html')

def detail(request, id):
    try:
        board = id_Board.objects.get(pk=id)
    except id_Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'instaid_app/detail.html', {'board': board})