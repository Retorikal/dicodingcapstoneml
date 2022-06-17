from django.contrib import admin
from django.urls import path,include
from mysite.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('customer/',include("course.urls")),
    path('register/', registerPage,name="register"),
    path('login/',loginPage,name="login"),
    path('logout/',logoutUser,name="logout"),
    path('user/',userPage,name="userpage"),
    path('user/update/<str:update_id>',updateOrder,name="updateOrder"),
    path('user/courses',allCourses,name="allCourses"),
    path('user/courses/create/<str:course_id>',createOrder,name="createOrder"),
    path("user/learningpath",learningPath,name="learningpath"),
    path("user/recommend",recommendation,name="recommendation"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
