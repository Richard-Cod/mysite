from . import views
from django.urls import path

urlpatterns = [
    path('',views.post_list_view,name='post_list'),
]