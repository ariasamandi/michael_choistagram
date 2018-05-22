from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from models import *
# Create your views here.
def index(request):
    return render(request, 'my_app/index.html')
def register(request):
    print request.POST
    result = User.objects.register_validator(request.POST)
    if 'errors' in result:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result['user'].id
        return redirect('/dashboard')
def login(request):
    result = User.objects.login_validator(request.POST)
    if 'errors' in result:
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result['user'].id
        return redirect('/dashboard')
def dashboard(request):
    if Post.objects.filter(posted_by__id=request.session['user_id']).count() >= User.objects.get(id=request.session['user_id']).post_tokens:
        context={
            'users_posts': Post.objects.filter(posted_by__id=request.session['user_id']).count(),
            'users_tokens': User.objects.get(id=request.session['user_id']).post_tokens,
            "user": User.objects.get(id=request.session["user_id"]),
            "photo": Post.objects.filter(posted_by__id=request.session['user_id']),
            "friends": User.objects.filter(friends__id=request.session['user_id']),
            "other_users": User.objects.exclude(friends__id=request.session['user_id']).exclude(id=request.session['user_id']),
            'message': "Must purchase space to add another post"
        }
    else:
        context = {
            'users_posts': Post.objects.filter(posted_by__id=request.session['user_id']).count(),
            'users_tokens': User.objects.get(id=request.session['user_id']).post_tokens,
            "user": User.objects.get(id=request.session["user_id"]),
            "photo": Post.objects.filter(posted_by__id=request.session['user_id']),
            "friends": User.objects.filter(friends__id=request.session['user_id']),
            "other_users": User.objects.exclude(friends__id=request.session['user_id']).exclude(id=request.session['user_id'])
        }
    return render(request, 'my_app/dashboard.html', context)
def add_photo(request):
    Post.objects.create(caption=request.POST['caption'], image=request.FILES['image'], posted_by=User.objects.get(id=request.session['user_id']))
    return redirect('/dashboard')
def users(request, id):
    context = {
        "user": User.objects.get(id=id),
        "friends": User.objects.filter(friends__id=id),
        "photo": Post.objects.filter(posted_by__id=id),
    }
    return render(request, 'my_app/users.html', context)
def add_friend(request, id):
    user_1 = User.objects.get(id=request.session['user_id'])
    user_2 = User.objects.get(id=id)
    user_1.friends.add(user_2)
    return redirect('/dashboard')
def remove(request, id):
    user_1 = User.objects.get(id=request.session['user_id'])
    user_2 = User.objects.get(id=id)
    user_1.friends.remove(user_2)
    return redirect('/dashboard')
def purchase(request):
    return render(request, 'my_app/purchase.html')
def prestripe(request):
    request.session['val'] = str(request.POST['purchase'])
    print str(request.POST['purchase'])
    return redirect('/stripe')
def stripe(request):
    return render(request, 'my_app/stripe.html')
def purchase_process(request):
    user = User.objects.get(id=request.session['user_id'])
    user.post_tokens += int(request.session['val']) * .05
    user.save()
    return redirect('/dashboard')
def logout(request):
    request.session.clear()
    return redirect('/')
