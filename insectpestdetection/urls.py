"""insectpestdetection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from modules import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'), 
    path('aboutus/', views.aboutus),
    path('contactus/', views.contactus),
    path('userreg/', views.userreg),
    path('user_reg/', views.user_details_add, name='user_reg'),
    path('user_login', views.user_login_check, name='user_login'),
    path('farmer_register', views.farmer_details_add, name='farmer_register'),
    path('krishi_register', views.krishi_details_add, name='krishi_register'),
    path('farmer_login', views.farmer_login_check, name='farmer_login'),
    path('user_login', views.user_login_check, name='user_login'),
    path('krishi_login', views.krishi_login_check, name='krishi_login'),
    path('login/', views.login),
    path('success', views.success,name='success'),
    path('invalid', views.invalid,name='invalid'),
    path('adminindex/', views.admin),
    path('farmer/', views.farmer),
    path('user/', views.user),
    path('krishi/', views.krishi),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_userview', views.userview,name='admin_userview'),
    path('admin_farmerview', views.farmerview,name='admin_farmerview'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('userhome', views.userhome),
    path('farmerhome', views.farmerhome),
    path('krishihome', views.krishihome),
    path('logout/', views.logout_request),
    path('feedback/', views.feedback),
    path('img/', views.img),
    path('search/', views.search),
    path('admin_kview', views.krishiview,name='admin_kview'),
    path('admin_approved_kview', views.krishi_approved_view,name='admin_approved_kview'),
    path('admin_approve/<int:pk>', views.approve_krishi_view,name='admin_approve'),
    path('admin_decline/<int:pk>', views.krishideletedata,name='admin_decline'),
    path('userdelete/<int:pk>', views.userdelete,name='userdelete'),
     path('farmerdelete/<int:pk>', views.farmerdelete,name='farmerdelete'),
    path('solution', views.farmer_request,name='solution'),
    path('farmerrequestview', views.farmer_request_view,name='farmerrequestview'),
    path('krishiviewrequest', views.krishiviewrequest,name='krishiviewrequest'),
    path('krishireply', views.krishi_reply,name='krishireply'),
    path('farmerviewreply', views.farmerviewreply,name='farmerviewreply'),
    path('profile', views.profile,name='profile'),
    path('profileedit', views.profile_edit,name='profileedit'),
    path('krishiprofile', views.kprofile,name='krishiprofile'),
    path('krishiprofileedit', views.krishiprofile_edit,name='krishiprofileedit'),
    path('userprofile', views.uprofile,name='userprofile'),
    path('userprofileedit', views.userprofile_edit,name='userprofileedit'),
    path('krishi_notification/', views.krishi_notification),
    path('savereply/',views.savereply),
    path('pfeedback',views.patientfeedback),
    path('patient_view_feedback', views.patient_feedback_view, name='patient_view_feedback'),
    path('admin-view-feedback', views.admin_view_feedback,name='admin-view-feedback'),
    path('admin-reply/<int:id>/', views.admin_reply,name='admin-reply'),
    path('reply/<int:id>/', views.reply,name='reply'),
    path('admin-view-request', views.admin_view_solution,name='admin-view-request'),
    path('user_changepassword', views.farmer_changepassword,name='user_changepassword'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

