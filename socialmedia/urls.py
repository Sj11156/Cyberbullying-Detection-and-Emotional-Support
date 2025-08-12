"""socialmedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialapp.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('index/',index,name='index'),
    path('Registration/',Registration,name='Registration'),
    path('login',login,name='login'),
    path('postadd/',postadd,name='postadd'),
    path('regaction/',regaction,name='regaction'),
    path('postaction/',postaction,name='postaction'),
    path('laction/',laction,name='laction'),
    path('adminhome/',adminhome,name='adminhome'),
    path('userhome/',userhome,name='userhome'),
    path('viewpost/',viewpost,name='viewpost'),
    path('viewreg/',viewreg,name='viewreg'),
    path('group/',group,name='group'),
    path('gaction/',gaction,name='gaction'),
    path('message/',message,name='message'),
    path('maction/',maction,name='maction'),
    path('req/',req,name='req'),
    path('viewmessage/',viewmessage,name='viewmessage'),
    path('profile/',profile,name='profile'),
    path('paction/',paction,name='paction'),
    path('viewprofile/',viewprofile,name='viewprofile'),
    path('page/',page,name='page'),
    path('pagen/',pagen,name='pagen'),
    path('viewpage/',viewpage,name='viewpage'),
    path('accept/',accept,name='accept'),
    path('groupreq/',groupreq,name='groupreq'),
    path('mssg/',mssg,name='mssg'),

    path('umsg',umsg,name='umsg'),
	path('umsgaction/',umsgaction,name='umsgaction'),
	path('urplyaction/',urplyaction,name='umsgaction'),
	path('delpost/',delpost,name='delpost'),
	path('postimage/',postimage,name='postimage'),
	path('imgaction/',imgaction,name='imgaction'),
	path('delimg/',delimg,name='delimg'),
	path('viewUsers/',viewUsers,name='viewUsers'),
	path('viewUsersPost/',viewUsersPost,name='viewUsersPost'),
	path('delUpost/',delUpost,name='delUpost'),
	path('delUserr/',delUserr,name='delUserr'),
	path('unfriend/',unfriend,name='unfriend'),
	path('comments/',comments,name='comments'),
 
	path('cmdaction/',cmdaction,name='cmdaction'),
    path('careview/',careview,name='careview'),
	path('vblock/',vblock,name='vblock'),
	path('delblock/',delblock,name='delblock'),
	
	path('pupaction/',pupaction,name='pupaction'),
	
	path('profileimgaction/',profileimgaction,name='profileimgaction'),
	path('login/',TemplateView.as_view(template_name ='index.html')),
    path ('predict_emotions/',predict_emotions, name ='predict_emotions'),
    path('get_prediction_proba/',get_prediction_proba ,name ='get_prediction_proba'),
    path('care/',care ,name ='care'),
    path('caaction/',caaction,name ='caaction'),
    path('care/',care ,name ='care'),
    path('caaction/',caaction,name ='caaction'),
    path('assign/',assign,name ='assign'),
    path('assnCare/',assnCare,name ='assnCare'),
    path('chat/',chat,name ='chat'),
    path('chataction/',chataction,name ='chataction'),
    path('caretakerHome/',caretakerHome,name ='caretakerHome'),
    path('cVWork/',cVWork,name ='cVWork'),
    path('lchat/',lchat,name ='lchat'),
    path('lchataction/',lchataction,name ='lchataction'),
    path('mentalchatbot/',mentalchatbot,name ='mentalchatbot'),
    path('depression/',depression,name ='depression'),
    path('dpract/',dpract,name ='dpract'),
    path('vdeprs/',vdeprs,name ='vdeprs'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()

