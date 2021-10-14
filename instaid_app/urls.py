from django.urls import path
from instaid_app import views

app_name = "instaidapp"

urlpatterns = [
    path('', views.post, name="id_board"),
    path('write/', views.board, name="id_write"),
    path('post/<int:id>', views.detail, name='detail'),
]