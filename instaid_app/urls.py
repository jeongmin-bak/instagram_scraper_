from django.urls import path
from instaid_app import views

app_name = "instaidapp"

urlpatterns = [
    path('', views.post, name="id_board"),
    path('write/', views.board, name="id_write"),
    path('post/<int:id>', views.detail, name='detail'),

    #다운로드를 위한 경로 설정
    path('export_user_xls/<int:id>', views.export_users_xls, name="excel")
]