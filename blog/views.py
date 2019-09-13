from django.shortcuts import render , get_object_or_404 ,redirect
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Post,Comment
from .forms import PostForm ,CommentForm ,UserForm

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



@login_required
def comment_to_post(request,id):
	post = get_object_or_404(Post,id=id)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.author =request.user
			comment.save()
			return redirect('post_detail',id=id)
	else:
		form = CommentForm()
	return render(request,'blog/comment_to_post.html',{'form':form})
	
@login_required
def remove_comment(request,id):
	comment = get_object_or_404(Comment,id=id)
	poste_id= comment.post.id
	comment.delete()
	return redirect('post_detail',id=poste_id)



@login_required
def approve_comment(request,id):
	comment = get_object_or_404(Comment,id=id)
	poste_id= comment.post.id
	comment.approve()
	return redirect('post_detail',id=poste_id)



def signup(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(**form.cleaned_data)
			login(request,new_user)
			return redirect('post_list')
	else:
		form = UserForm()
	return render(request,'registration/signup.html',{'form':form})

	