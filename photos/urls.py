from django.urls import path
from . import views

urlpatterns=[
    path('',views.gallery,name='gallery'),
    path('add/',views.addPhoto,name='add'),
    path('photo/<str:pk>/',views.viewPhoto,name='photo'),
    path('delete_photo/<str:pk>/',views.suppPhoto,name='delete_photo'),
    path('edit/<str:pk>/',views.editPhoto,name='edit_photo'),
    path('diaporama/<str:pk>/',views.diaporamaPhoto,name='diaporama'),
    path('share/',views.sharePhoto,name="share"),
    path('getSharePhoto',views.getSharePhoto,name="getSharePhoto"),
    path('postSharePhoto',views.postSharePhoto,name="postSharePhoto")
]