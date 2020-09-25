from django.shortcuts import render, get_object_or_404, redirect
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


def post_new(request):  # admin page
    
    if request.method == "POST":  # data has been entered into the fields
    
        form = PostForm(request.POST)  # access the submitted data
        
        if form.is_valid():
            post = form.save(commit = False)  # commit = False creates a form instance but doesn't save it to the database - useful when form data needs to be modified
            post.author = request.user  # note: required field
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)  # display post once saved
    
    else:  # new blank form
        form = PostForm()
    
    return render(request, 'blog/post_edit.html', {'form' : form})


def post_edit(request, pk):

    post = get_object_or_404(Post, pk = pk)  # find post
    
    if request.method == "POST":  # data has been changed
        
        form = PostForm(request.POST, instance = post)
        
        if form.is_valid():
            post = form.save(commit = False)  # create form instance
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    
    else:
        form = PostForm(instance = post)
    
    return render(request, 'blog/post_edit.html', {'form' : form})
            
    