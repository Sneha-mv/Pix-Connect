from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('gallery/',views.gallery,name='gallery'), 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('photographer-dashboard/',views.photographer_dashboard,name='photographer_dashboard'),
    path('user-dashboard/',views.user_dashboard,name='user_dashboard'),
]