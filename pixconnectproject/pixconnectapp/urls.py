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
    path('photographer/<int:photographer_id>/delete/', views.delete_photographer, name='delete_photographer'),
    path('admin-images/', views.admin_images_list, name='admin_images_list'),
    path('admin-delete_image/<int:image_id>/', views.admin_delete_image, name='admin_delete_image'),
    path('users/', views.user_list, name='user_list'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    # Photographer Section
    path('photographer-dashboard/',views.photographer_dashboard,name='photographer_dashboard'),
    path('complete_profile_photographer/', views.complete_profile_photographer, name='complete_profile_photographer'),
    path('add_image/', views.add_image, name='add_image'),
    path('view_images/', views.view_images, name='view_images'),
    path('edit_image/<int:image_id>/', views.edit_image, name='edit_image'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),

    # User Section
    path('user-dashboard/',views.user_dashboard,name='user_dashboard'),
    path('photographers/', views.photographers_view, name='photographers'),
    path('photographer-detail/<int:id>/', views.photographer_detail, name='photographer_detail'),
]