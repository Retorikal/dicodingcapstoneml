from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from course.models import *
from course.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from mysite.decorators import allowed_users, unauthenticated_user,admin_only
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
import numpy as np

import googleapiclient.discovery
from google.api_core.client_options import ClientOptions
import requests
#import json



def predict_lp(project, region, model, instances, version="learningpath"):
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

def predict_course(project, region, model, instances, version="recommender"):
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

def output(model_output):
    learning_path = ['AD', 'ML', 'CC']
    return learning_path[np.argmax(model_output[0])]


@login_required(login_url='login')
@admin_only
def index(request):
    context={
        "title" : "Latihan Relational",
        "subtitle" : "latihan relational database untuk CRM"
    }

    return render(request,"index.html",context)

@unauthenticated_user
def registerPage(request):
    form = createUserForm()
    course = Course.objects.all()
    if request.method == "POST":
        form = createUserForm(request.POST,request.FILES)
        if form.is_valid:
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            url = 'https://asia-southeast2-zippy-elf-352113.cloudfunctions.net/ocr-request'
            cv_path = "{}".format(user.cv)
            myobj = {'data': cv_path}
            ocr_request = requests.post(url, json = myobj)
            input_prediction = [ocr_request.text]
            test = predict_lp("zippy-elf-352113","asia-southeast1","dicoding_project",instances=input_prediction)
            predict = output(test)
            Customer.objects.create(
                user=user,
                email=user.email,
                name=user.fullname,
                linkedin=user.linkedin,
                age=user.age,
                learningpath = predict,
                user_cv=user.cv,     
            )
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],)
            login(request,user)

            return redirect('home')


    context={
        "form" : form,
        
    }
    return render(request,'course/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username or password is incorrect")

    context={}
    return render(request,'course/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def userPage(request):
    lpkey={
        'AD' : 'Android Developer',
        'CC' : 'Cloud Computing',
        'ML' : 'Machine Learning'
    }
    user = request.user.customer
    learningpath = lpkey[user.learningpath]
    orders = request.user.customer.order_set.filter(status="On Progress")
    p = Paginator(orders.all(),5)
    page = request.GET.get('page')
    orderpage = p.get_page(page)
    context={
        "orders":orderpage,
        "user" :user,
        "lp" : learningpath
    }
    return render(request,"course/user.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def createOrder(request,course_id):
     courses = Course.objects.get(id=course_id)
     all_courses = Course.objects.all()
     user = request.user.customer
     orders = request.user.customer.order_set.all()
     data={
         "customer" : user,
         "product" : courses,
         "status" : "On Progress"
     }
     form = orderForm(request.POST or None, initial=data)
     next = request.POST.get('next', '/')
     order_name=[]
     for k in range(len(orders)):
        order_name.append(orders[k].product.name)
     if request.method == 'POST':
        if courses.name in order_name:
            return redirect(request.path_info)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    

     context = {
         'form' : form,
         'user' : user,
         "all_courses":all_courses,
         "orders":orders,
         "courses":courses,
         "action" : "take",
     }
     return render(request,'course/order.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def updateOrder(request,update_id):
    order_update= Order.objects.get(id=update_id)
    user = request.user.customer
    data={
        "status":"Finished",

    }
    form = orderForm(request.POST or None ,initial=data,instance=order_update)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/user/recommend')

    context = {
        'form' : form,
        'action' : "finish",
        'user' :user,
     }
    return render(request,'course/order.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def allCourses(request):
    user = request.user.customer
    orders = request.user.customer.order_set.order_by('-status')
    p = Paginator(orders.all(),5)
    page = request.GET.get('page')
    orderpage = p.get_page(page)
    order_list=[]
    for k in range(len(orders)):
        order_name = orders[k].product.name
        order_list.append(order_name)
    p2 = Paginator(Course.objects.exclude(name__in=order_list),5)
    coursepage = p2.get_page(page)

    context={
        "user" : user,
        "courses" : coursepage,
        "user_courses" : orderpage,
        "order_list" :order_list,
        "num_p1" : p.num_pages,
        "num_p2" : p2.num_pages,
    }
    return render(request,"course/course.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def learningPath(request):
    user = request.user.customer
    orders = request.user.customer.order_set.all()
    p = Paginator(orders.all(),5)
    page = request.GET.get('page')
    orderpage = p.get_page(page)
    p2 = Paginator(Course.objects.filter(category=user.learningpath),5)
    coursepage = p2.get_page(page)
    order_list=[]
    if request.method=='GET':
        request.session['learningpath'] = request.META.get('HTTP_REFERER','/')
    for k in range(len(orders)):
        order_name = orders[k].product.name
        order_list.append(order_name)
        
    context={
        "user" : user,
        "courses" : coursepage,
        "user_courses" : orderpage,
        "order_list" :order_list,
    }
    return render(request,"course/learningpath.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def recommendation(request):
    user = request.user.customer
    orders = request.user.customer.order_set.filter(status="Finished")
    all_orders = request.user.customer.order_set.all()
    id_list=[]
    order_list=[]
    for k in range(len(orders)):
        order_id = int(orders[k].product.id)
        order_name = orders[k].product.name
        order_list.append(order_name)
        id_list.append(order_id)

    if len(id_list)<5:
        for i in range(5-len(id_list)):
            id_list.insert(0,0)
    if len(id_list)>5:
        id_list = id_list[-5:]

    id_list=[id_list]
    next_course = predict_course("zippy-elf-352113","asia-southeast1","dicoding_project",instances=id_list)
    strings=next_course[0]["output_2"][:5]

    order_list=[]

    for k in range(len(all_orders)):
        order_name = all_orders[k].product.name
        order_list.append(order_name)
    queryset =Course.objects.filter(name__in=strings).exclude(name__in=order_list)
    context={
        "user" : user,  
        "courses" : queryset,
        "order_list" :order_list,
    }

    return render(request, "course/rekomendasi.html", context)