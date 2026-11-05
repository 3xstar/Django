from django.shortcuts import redirect, render
from .forms import CommentForm, PostForm
from .models import Comment, Post


def index(request):
    posts = Post.objects.all()
    return render(request, "main/index.html", {"posts": posts})


def add_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect("main:index")
    else:
        post_form = PostForm()
    return render(request, "main/add_post.html", {"post_form": post_form})


def post_info(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("main:post_info", post_id=post.id)
    else:
        comment_form = CommentForm()

    comments = Comment.objects.filter(post=post).order_by("created_at")
    return render(
        request,
        "main/post_info.html",
        {"post": post, "comment_form": comment_form, "comments": comments},
    )


def post_delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect("main:index")