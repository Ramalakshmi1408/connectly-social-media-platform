
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterForm, ProfileUpdateForm, PostForm

from .models import Post, Follow, Like, Comment
from .forms import RegisterForm, ProfileUpdateForm, PostForm
from django.db.models import Q

# USER REGISTRATION
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Your account has been created successfully!'
            )
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'social/register.html', {'form': form})

# USER LOGIN
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, 'Welcome back!')
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'social/login.html', {'form': form})

# USER LOGOUT
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully.')
        return redirect('login')

    return redirect('home')

# VIEW USER PROFILE
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=profile_user)

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })

# EDIT USER PROFILE
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect(
                'profile',
                username=request.user.username
            )
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'social/edit_profile.html', {
        'form': form
    })

# HOME PAGE / NEWS FEED
# HOME PAGE
def home_view(request):
    posts = Post.objects.select_related(
        'author'
    ).prefetch_related(
        'comments',
        'likes'
    ).all()

    liked_post_ids = set()

    if request.user.is_authenticated:
        liked_post_ids = set(
            Like.objects.filter(
                user=request.user
            ).values_list('post_id', flat=True)
        )

    return render(request, 'social/home.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
    })

# CREATE A NEW POST
@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, 'Your post has been published!')
            return redirect('home')

    else:
        form = PostForm()

    return render(request, 'social/create_post.html', {
        'form': form
    })
# LIKE AND UNLIKE POSTS
@login_required
def like_post_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        existing_like = Like.objects.filter(
            post=post,
            user=request.user
        ).first()

        if existing_like:
            existing_like.delete()
        else:
            Like.objects.create(
                post=post,
                user=request.user
            )

    return redirect('home')
# ADD A COMMENT
@login_required
def add_comment_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        content = request.POST.get('content', '').strip()

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

            messages.success(request, 'Your comment was added!')

    return redirect('home')
# FOLLOW AND UNFOLLOW USERS
@login_required
def follow_view(request, username):
    if request.method == 'POST':
        target_user = get_object_or_404(User, username=username)

        if target_user != request.user:
            existing_follow = Follow.objects.filter(
                follower=request.user,
                following=target_user
            ).first()

            if existing_follow:
                existing_follow.delete()
            else:
                Follow.objects.create(
                    follower=request.user,
                    following=target_user
                )

        return redirect('profile', username=username)

    return redirect('profile', username=username)
# EDIT A POST
@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Your post was updated!')
            return redirect('home')

    else:
        form = PostForm(instance=post)

    return render(request, 'social/edit_post.html', {
        'form': form,
        'post': post
    })
# DELETE A POST
@login_required
def delete_post_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(
            Post,
            id=post_id,
            author=request.user
        )

        post.delete()
        messages.success(request, 'Your post was deleted!')

    return redirect('home')
# SEARCH USERS AND POSTS
def search_view(request):
    query = request.GET.get('q', '').strip()

    users = User.objects.filter(
        username__icontains=query
    ) if query else User.objects.none()

    posts = Post.objects.filter(
        Q(caption__icontains=query) |
        Q(author__username__icontains=query)
    ).select_related('author') if query else Post.objects.none()

    return render(request, 'social/search.html', {
        'query': query,
        'users': users,
        'posts': posts,
    })