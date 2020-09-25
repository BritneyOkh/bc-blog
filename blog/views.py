from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.

def post_list(request):  # homepage

    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')  # order posts by published date
    return render(request, 'blog/post_list.html', {'posts' : posts})


def post_detail(request, pk):  # post page

    post = get_object_or_404(Post, pk = pk) # first  check if post exists
    return render(request, 'blog/post_detail.html', {'post' : post})


@login_required
def post_new(request):  #  make new post
    
    if request.method == "POST":  # data has been entered into the fields
    
        form = PostForm(request.POST)  # access the submitted data
        
        if form.is_valid():
            post = form.save(commit = False)  # commit = False creates a form instance but doesn't save it to the database - useful when form data needs to be modified
            post.author = request.user  # note: required field
            ##post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)  # display post once saved
    
    else:  # new blank form
        form = PostForm()
    
    return render(request, 'blog/post_edit.html', {'form' : form})


@login_required
def post_edit(request, pk):  # edit page

    post = get_object_or_404(Post, pk = pk)  # find post
    
    if request.method == "POST":  # data has been changed
        
        form = PostForm(request.POST, instance = post)
        
        if form.is_valid():
            post = form.save(commit = False)  # create form instance
            post.author = request.user
            ##post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    
    else:
        form = PostForm(instance = post)
    
    return render(request, 'blog/post_edit.html', {'form' : form})
  

@login_required
def post_draft_list(request):  # drafts page
    
    posts = Post.objects.filter(published_date__isnull = True).order_by('-created_date')  # order drafts by creation date
    return render(request, 'blog/post_draft_list.html', {'posts' : posts})


@login_required
def post_publish(request, pk):  # publish function
    
    post = get_object_or_404(Post, pk = pk)  # first find post - in case user types in url
    post.publish()
    return redirect('post_detail', pk = pk)  # show post

@login_required
def post_remove(request, pk):  # delete function

    post = get_object_or_404(Post, pk = pk)
    post.delete()
    return redirect('post_list')
    