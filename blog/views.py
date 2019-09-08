from django.shortcuts import render , get_object_or_404 ,redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm

# Create your views here.

def post_list_view(request):
	posts= Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request,'blog/posts_list.html',{'posts':posts})

def post_detail(request,id):
	post= get_object_or_404(Post,pk=id)
	return render(request,'blog/posts_detail.html',{'post':post})

def post_edit(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail',id=post.pk)
	else:
		print("Un biz tout vide")
		form = PostForm()
	return render(request,'blog/post_edit.html',{'form':form})