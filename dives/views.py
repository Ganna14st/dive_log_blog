import smtplib
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import BlogPost, Comment, LogBook
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from . import forms


def get_all_posts(request):
    posts = BlogPost.objects.all().order_by('-date')
    return render(request, 'index.html', context={'all_posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            messages.success(request, 'Registration successful')
            return HttpResponseRedirect('../')
        else:
            messages.error(request, message='Invalid information. Registration failed')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect('../')
        else:
            messages.error(request, message='Invalid information. Login failed')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('../')


def show_post(request, post_id):
    requested_post = BlogPost.objects.get(id=post_id)
    comments = Comment.objects.filter(post=requested_post)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST, request.FILES)
        if form.is_valid():
            row_comment = form.save(commit=False)
            row_comment.author = request.user
            row_comment.post = requested_post
            row_comment.save()
            return render(request, 'post.html', {'post': requested_post, 'form': form, 'all_comments': comments})
    else:
        form = forms.CommentForm()
    return render(request, 'post.html', {'post': requested_post, 'form': form, 'all_comments': comments})


def contact(request):
    try:
        if request.method == 'POST':
            my_email = 'gannatest6@gmail.com'
            password = 'ygiszijbwwiwcdit'
            data = request.POST.dict()
            letter = f'{data["name"]}\n{data["email"]}\n{data["phone"]}\nMessage\n*****\n{data["message"]}'
            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email, to_addrs='ganna14st@gmail.com',
                                    msg=f'Subject: New Message from Dive Blog!\n\n{letter}')
            messages.success(request, message="Your message was successfully sent.")
            return HttpResponseRedirect('../')
        else:
            return render(request, "contact.html")
    except smtplib.SMTPDataError:
        messages.success(request, message="Something went wrong. Please try again later or contact me on social media.")
        return render(request, "contact.html")

@login_required(login_url="../login/")
def add_new_post(request):
    if request.method == 'POST':
        form = forms.CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            row_post = form.save(commit=False)
            row_post.author = request.user
            row_post.save()
            return HttpResponseRedirect('../')
    else:
        form = forms.CreatePostForm()
    return render(request, 'make-post.html', {'form': form, 'is_edit': False})


# TODO: delete old post after editing
@login_required()
def edit_post(request, post_id):
    requested_post = BlogPost.objects.get(id=post_id)
    if request.method != 'POST':
        form = forms.CreatePostForm(instance=requested_post)
    else:
        form = forms.CreatePostForm(instance=requested_post, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated.')
            return render(request, "post.html", {'post': requested_post, 'is_edit': True})
    context = {'post': requested_post, 'id': post_id, 'form': form, 'is_edit': True}
    return render(request, 'make-post.html', context)


@login_required()
def delete_post(request, post_id):
    requested_post = BlogPost.objects.get(id=post_id)
    requested_post.delete()
    return HttpResponseRedirect('../../')


@login_required()
def comment_post(request, post_id):
    requested_post = BlogPost.objects.get(id=post_id)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST, request.FILES)
        if form.is_valid():
            row_comment = form.save(commit=False)
            row_comment.author = request.user
            row_comment.post = requested_post
            row_comment.save()
            return render(request, 'post.html', {'post.id': post_id, 'form': form, 'is_edit': False})
    else:
        form = forms.CreatePostForm()
    return render(request, 'post.html', {'form': form, 'is_edit': False})


def log_book(request):
    logs = LogBook.objects.filter(author=request.user).order_by('-date')
    return render(request, 'logbook.html', context={'logs': logs})


@login_required()
def show_log(request, log_id):
    requested_log = LogBook.objects.get(id=log_id)
    return render(request, "log.html", {'log': requested_log})


@login_required()
def add_log(request):
    if request.method == 'POST':
        form = forms.LogBookForm(request.POST, request.FILES)
        if form.is_valid():
            row_log = form.save(commit=False)
            row_log.author = request.user
            row_log.save()
            return HttpResponseRedirect('../log_book')
    else:
        form = forms.LogBookForm()
    return render(request, 'add_log.html', {'form': form, 'is_edit': False})


@login_required()
def edit_log(request, log_id):
    requested_log = LogBook.objects.get(id=log_id)
    if request.method != 'POST':
        form = forms.LogBookForm(instance=requested_log)
    else:
        form = forms.LogBookForm(instance=requested_log, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Log updated.')
            requested_log.delete()
            HttpResponseRedirect('../')
    return render(request, 'add_log.html', {'log': requested_log, 'id': log_id, 'form': form, 'is_edit': True})


@login_required()
def delete_log(request, log_id):
    requested_log = LogBook.objects.get(id=log_id)
    requested_log.delete()
    return HttpResponseRedirect('../../')
