from django.shortcuts import render, redirect
from ..login_and_registration.models import User
from models import Distiller, Beverage, FavorPoint
from django.contrib import messages
from . import models

def index(request):
    if 'user' in request.session:
        context = {
            'whiskies': Beverage.objects.all(),
            'distillers': Distiller.objects.all(),
        }
        return render(request, 'beverages/index.html', context)
    return redirect('login:index')

def add_form(request):
    if 'user' in request.session:
        context = {
            'distillers': Distiller.objects.all(),
        }
        return render(request, 'beverages/add.html', context)
    return redirect('login:index')

def add(request):
    # print 'calling add method'
    # if 'user' in request.session:
    # print 'user in session'
    if request.method == 'POST':
        result = Beverage.objects.create_beverage(request)
        if result[0] == False:
            # print result[0], result[1]
            display_errors(request, result[1])
            return redirect('beverages:add_form')
        # print result[0]
    return redirect('login:index')

def display_errors(request, display_errors_list):
    for error in display_errors_list:
        #  VV    https://docs.djangoproject.com/en/1.10/ref/contrib/messages/    VV
        messages.add_message(request, messages.INFO, error)

def edit(request, id):
    if 'user' in request.session:
        print id
        pass
    return redirect('login:index')

def distiller_info(request, id):
    print 'distiller_info id: ', id
    this_distiller = Distiller.objects.get(id=id)
    context = {
        'this_distiller': this_distiller,
        'distillers': Distiller.objects.all(),
        'other_distillers': Distiller.objects.exclude_current_distiller(this_distiller),
    }
    return render(request, 'beverages/distiller.html', context)

def edit_distiller(request, id):
    if 'user' in request.session:
        context = {'this_distiller': Distiller.objects.get(id=id)}
        return render(request, 'beverages/edit_distiller.html', context)
    return redirect('login:index')

def update_distiller(request, id):
    if 'user' in request.session:
        if request.method == 'POST':
            Distiller.objects.update_distiller(id, request)
            # context = {'this_distiller': Distiller.objects.get(id=id)}
            return redirect('beverages:distiller_info', id)
    return redirect('LogReg:index')

def update_user(request, id):
    if user_in_session(request):
        if request.method == 'POST':
            User.objects.update_user(id, request)
            return redirect('/home')
    return redirect('LogReg:index')

def delete(request, id):
    if 'user' in request.session:
        # print 'in delete method'
        # print 'id:', id
        # if request.method == 'POST':
        Beverage.objects.delete_beverage(request, id)
        # print id
        # bev_id = Beverage.objects.delete_beverage(id, request)
        # print bev_id
    return redirect('login:index')

def delete_distiller(request, id):
    if 'user' in request.session:
        Distiller.objects.delete_distiller(request, id)
        # ha! exclude the chosen distiller, then redirect back to beverages:distiller_info...well...kinda ghetto forcing it back to id = 1 (Ardbeg) *****************
        return redirect('beverages:distiller_info', 1)
    return redirect('login:index')

# def create_try(request, id):
#     if 'user' in request.session:
#         # user = User.objects.get(id=id)
#         beverage = Beverage.objects.get(id=id)
#         print beverage
#         # print user
#         return render(request, 'beverages:index')

def favor(request, id):
    if 'user' in request.session:
        if request.method == 'POST':
            print 'user id: ', request.session['user']['user_id']
            # Favor.objects.create_favor(request.session.user.id), request.POST['whisky.id']
            favor_user = request.session['user']['user_id']
            favor_beverage = Beverage.objects.get(id=id)
            print 'favor_beverage: ', favor_beverage.id
            FavorPoint.objects.create_favor(favor_user, favor_beverage)
            # context = {
            #     'favor_user': request.session['user']['user_id'],
            #     'favor_beverage': whisky,
            # }
            # context = {
            #     'whiskies': Beverage.objects.all(),
            #     'distillers': Distiller.objects.all(),
            # }
            # return render(request, 'beverages/index.html', context)
            return redirect('beverages:index')
        else:
            return redirect('beverages:index')