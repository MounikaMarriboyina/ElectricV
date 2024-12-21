from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about',views.about,name='about'),
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('upload', views.upload, name='upload'),
    path('split', views.split, name='split'),
    path('train', views.train, name='train'),
    path('prediction', views.prediction, name='prediction')
    
]