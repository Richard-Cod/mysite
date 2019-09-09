from django.shortcuts import render , get_object_or_404 ,redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm

from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list_view(request):
	posts= Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request,'blog/posts_list.html',{'posts':posts})

def post_detail(request,id):
	post= get_object_or_404(Post,pk=id)
	return render(request,'blog/posts_detail.html',{'post':post})

@login_required
def post_new(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail',id=post.id)
	else:
		form = PostForm()
	return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_edit(request,id):
	post = get_object_or_404(Post,id=id)
	if request.method == 'POST':
		form = PostForm(request.POST,instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail',id=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request,'blog/post_edit.html',{'form':form})

@login_required
def draft_list_view(request):
	posts= Post.objects.filter(published_date=None).order_by('-created_date')
	return render(request,'blog/posts_draft.html',{'posts':posts})

@login_required
def draft_list_publish(request,id):
	post = Post.objects.get(id=id)
	print(post)
	post.published_date = timezone.now()
	post.save()
	
	return redirect('post_list')