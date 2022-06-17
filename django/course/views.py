from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from mysite.decorators import allowed_users
from django.contrib import messages
# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def index(request):
    customer = Customer.objects.all()
    context={
        "title" : "All Customer",
        "customers" : customer, 
    }

    return render(request,"course/index.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def view_users(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    context={
        "title" : "Customer Profile",
        "customer" : customer,
        "orders":orders,
    }

    return render(request,"course/profil.html",context)

@login_required(login_url='login')
def createOrderAdmin(request,pk):
    customer1 = Customer.objects.get(id=pk)
    course = Course.objects.all()
    data={
        "customer" : customer1,
        "product" : course[0],
        "status" : "On Progress",
    }
    form = orderForm(request.POST or None, initial=data)

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            return redirect("/customer/{}".format(customer1.id))
    context={
        "form" : form,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        "customer" : customer1,
        "action" : "Enroll",
    }
    return render(request,"course/order.html",context)

