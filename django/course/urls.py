from django.urls import path

from mysite.views import learningPath
from .views import *

urlpatterns = [
    path("",index,name="allcustomer"),
    path('<str:pk>',view_users,name="uniquecustomer"),
    path('<str:pk>/order',createOrderAdmin,name="createOrderAdmin"),
    path("learningpath",learningPath,name="learningpath")
]
