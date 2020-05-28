"""contest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from application.views import homepage
from contestant.views import (contest, contest_detail, application, contest_application,
                              contest_application_update, commission_contests, contest_review, contest_result)
from user.views import profile
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', contest, name='contestant-home'),
    # path('contests/<int:pk>/', ContestDetailView.as_view(), name='contestant-detail'),
    path('contests/<int:pk>/', contest_detail, name='contestant-detail'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('contests/<int:pk>/application/', application, name='application'),
    path('contests/<int:pk_1>/application/<int:pk_2>/review/', contest_review, name='contest-review'),
    path('contests/<int:pk>/applications/', contest_application, name='contest-applications'),
    path('contests/<int:pk>/results/', contest_result, name='contest-result'),
    # path('contests/<int:pk>/applications/<int:pk>/', contest_application_update, name='contest-applications-update'),
    # commission
    path('commission/<int:pk>/', commission_contests, name='commission-contests'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)