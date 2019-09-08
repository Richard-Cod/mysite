from django.shortcuts import render , get_object_or_404
from django.utils import timezone

from .models import Post

# Create your views here.

def post_list_view(request):
	posts= Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request,'blog/posts_list.html',{'posts':posts})

def post_detail(request,id):
	post= get_object_or_404(Post,pk=id)
	return render(request,'blog/posts_detail.html',{'post':post})