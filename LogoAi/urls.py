"""
URL configuration for LogoAi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from backoffice_engine import views
from LogoAi import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('about/', views.about),
    path('login/',views.login),
    path('signup/',views.signup),
    path('profile/',views.profile),
    path('pricing/',views.pricing),
    path('features/',views.features),
    path('blog/',views.blog),
    path('blogDetails/',views.blogDetails),
    path('contact/',views.contact),
    path('comingsoon/',views.comingsoon),
    path('faq/',views.faq),
    path('update_profile/<int:id>',views.update_profile),
    path('delete_account/<int:id>',views.delete_account),
    path('logout/',views.logout),
    path('forgot/',views.sendotp),
    path('set_password/',views.set_password),
    path('genrate_logo/',views.genrate_logo),
    path('genrateresult_logo/',views.genrateresult_logo),
    path('gallery/',views.gallery),
    path('paymentsuccessful/',views.paymentsuccessful),
    path('feedback/',views.feedback),
    path('check/',views.check),
    

]
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# aastha here