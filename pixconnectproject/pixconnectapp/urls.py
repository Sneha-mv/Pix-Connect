from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('gallery/',views.gallery,name='gallery'), 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Admin Section
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('photographers-list/', views.photographers_list, name='photographers_list'),
    path('approve/<int:photographer_id>/', views.approve_photographer, name='approve_photographer'),
    path('reject/<int:photographer_id>/', views.reject_photographer, name='reject_photographer'),

    # Photographer Section
    path('photographer-dashboard/',views.photographer_dashboard,name='photographer_dashboard'),
    path('complete_profile_photographer/', views.complete_profile_photographer, name='complete_profile_photographer'),
    path('add_image/', views.add_image, name='add_image'),
    path('view_images/', views.view_images, name='view_images'),

    # User Section
    path('user-dashboard/',views.user_dashboard,name='user_dashboard'),
]