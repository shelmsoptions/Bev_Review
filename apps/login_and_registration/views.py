from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

def user_in_session(request):
    if 'user' in request.session:
        print 'method - user in sessions True!!'
        return True
    else:
        print 'method - user in sessions False!!'
        return False

def index(request):
    if user_in_session(request):
        # VV  this is where to plug-in the app  VV   *****
        return redirect('beverages:index')
    return render(request, 'login_and_registration/login.html')

def register_login(request):
    # if request.method == 'POST':
    if request.POST['action'] == 'register':
        result = User.objects.reg_validation(request)
    elif request.POST['action'] == 'login':
        result = User.objects.login_validation(request)
    if result[0] == False:
        # print 'logged-in? False - incorrect data'
        request.session['errors'] = result[1]
        context = { 'errors': request.session['errors'], }
        # print 'errors from register_login method view: ', errors
        return render(request, 'login_and_registration/login.html', context)
    # print result[1]
    return login_user(request, result[1])


def login_user(request, user):
    # print user
    request.session['user'] = {
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'alias': user.alias,
        'email': user.email,
        # 'users': User.objects.all(),
        # 'errors': errors,
    }
    # VV  this is where to plug-in the app  VV   *****
    # return redirect('LogReg:home')
    return redirect('beverages:index')

def home(request):
    if user_in_session(request):
        context = { 'users': User.objects.all(), }
        return render(request, 'login_and_registration/home.html', context)
    return redirect('LogReg:index')

def edit(request, id):
    user = User.objects.get(id=int(id))
    print user.id
    context = {'user':user}
    return render(request, 'login_and_registration/update.html', context)


def update_user(request, id):
    if user_in_session(request):
        if request.method == 'POST':
            User.objects.update_user(id, request)
            return redirect('/home')
    return redirect('LogReg:index')
    # return redirect('LogReg:index')

def delete(request, id):
    User.objects.filter(id=id).delete()
    return redirect('/home')

def logout(request):
    request.session.clear()
    return render(request, 'login_and_registration/login.html')