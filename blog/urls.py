from . import views
from django.urls import path

urlpatterns = [
    path('',views.post_list_view,name='post_list'),
    path('post/<int:id>/',views.post_detail,name='post_detail'),
    path('post/new/',views.post_edit,name='post_new'),
    path('post/edit/',views.post_edit,name='post_edit'),
]