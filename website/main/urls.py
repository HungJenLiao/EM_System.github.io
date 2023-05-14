from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('dashboard', views.dashboard, name='dashboard'), 
    path('upload', views.upload, name='upload'), 
    path('list', views.list, name='list'), 
    path('list/Edit', views.listEdit, name='listEdit'), 
    path('list/update/<int:Em_id>', views.listUpdate, name='listUpdate'),
    path('list/delete/<int:Em_id>', views.listDelete, name='listDelete'),
    path('user', views.user, name='user'), 
    path('record', views.record, name='record'), 
]