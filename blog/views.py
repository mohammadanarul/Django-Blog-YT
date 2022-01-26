from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login
from .forms import RegisterForm, ProfileUpdate, PostForm, CommentForm, ContactForm
from .models import Profile, Post
from django.utils.text import slugify


# Create your views here.
def HomeView(request):
    posts = Post.objects.filter(status='Publish').order_by('-pk',)
    return render(request, 'home.html', {'posts': posts,})

def single_post(request, slug):
    post = Post.objects.get(slug=slug)
    
    post.view_count += 1
    post.save()
    form = CommentForm()
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post_id = post.id
            instance.user_id = profile.id
            instance.save()
            return redirect('single_post_view', slug=post.slug)
    return render(request, 'single-blog.html', {'object': post, 'form': form})

def profile_view(request, pk):
    profile = Profile.objects.get(pk=pk)
    objects = Post.objects.filter(user=profile)
    context = {
        'profile': profile,
        'objects': objects
        }
    return render(request, 'profile.html', context)

def profile_update_view(request, pk):
    profile = Profile.objects.get(pk=pk)
    form = ProfileUpdate(instance=profile)
    if request.method == 'POST':
        form = ProfileUpdate(request.POST or None, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print('profile updated....')
            return redirect('/')
    return render(request, 'profile-update.html', {'form': form})

def post_create_view(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES)
        profile = Profile.objects.get(user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.title)
            instance.user = profile
            instance.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'post-create.html', {'form': form})

def post_update_view(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        post = Post.objects.get(slug=slug)
        form = PostForm(request.POST or None, request.FILES, instance=post)
        profile = Profile.objects.get(user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.title)
            instance.user = profile
            instance.save()
            return redirect('/')
    return render(request, 'post-create.html', {'form': form})





def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            print('account created..')
            return redirect('/')
    return render(request, 'sign-up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('login successfully..')
            return redirect('/')
        else:
            print('User Invalid.')
    return render(request, 'login.html')
        

def logout_view(request):
    logout(request)
    return redirect('/')


def comment_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'contact.html', {'form': form})