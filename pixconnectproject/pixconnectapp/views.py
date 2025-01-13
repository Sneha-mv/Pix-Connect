from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, PhotomanDetails, PhotographyImages, UserProfile
from django.core.files.storage import FileSystemStorage
import re
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def index(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about.html")


def gallery(request):
    return render(request,"gallery.html")


def is_strong_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not re.search(r'[A-Za-z]', password):
        return "Password must contain at least one albhabet."
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one digit."
    if not re.search(r'[@$!%*?&#]', password):
        return "Password must contain at least one special character."
    return None


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exits.")
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exits.")
            return redirect('register')
        password_error = is_strong_password(password)
        if password_error:
            messages.error(request, password_error)
            return redirect('register')

        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)
        user.save()
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, "Both username and password fields are required.")
            return redirect("login")
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.role == 'photographer':
                return redirect('photographer_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("login")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)  
    return redirect('index')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if len(new_password) < 8:
            messages.error(request, "Your password must be at least 8 characters long.")
            return redirect('quizapp:forgot_password')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('forgot_password')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No user found with that email address.")
            return redirect('forgot_password')

        user.set_password(new_password)
        user.save()
        # Update session auth hash to avoid the user getting logged out
        update_session_auth_hash(request, user)
        messages.success(request, "Your password has been successfully updated!")
        return redirect('login')  
    return render(request,'forgot_password.html')  

  
# Admin Section
def admin_dashboard(request):
    return render(request,"admin_dashboard.html")


def photographers_list(request):
    photographers_list = PhotomanDetails.objects.all()  
    return render(request, 'photographers_list.html', {'photographers_list': photographers_list})


def approve_photographer(request, photographer_id):
    photographer = PhotomanDetails.objects.get(id=photographer_id)
    photographer.status = 'approved'
    photographer.save()
    return redirect('photographers_list') 


def reject_photographer(request, photographer_id):
    photographer = PhotomanDetails.objects.get(id=photographer_id)
    photographer.status = 'rejected'
    photographer.save()
    return redirect('photographers_list') 


def delete_photographer(request, photographer_id):
    photographer = get_object_or_404(PhotomanDetails, id=photographer_id)
    photographer.delete()
    return redirect('photographers_list')


def admin_images_list(request):
    images = PhotographyImages.objects.all().select_related('photographer')  
    return render(request, 'admin_images_list.html', {'images': images})


def admin_delete_image(request, image_id):
    image = get_object_or_404(PhotographyImages, id=image_id)
    if request.method == 'POST':
        image.delete()
        return redirect('admin_images_list')  
    return redirect('admin_images_list')


def user_list(request):
    users = UserProfile.objects.all()  
    return render(request, 'user_list.html', {'users': users})


def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)  
    user.user.is_active = False
    user.user.save()
    # Optionally, delete the user profile (you can skip this if you want to keep the profile data)
    user.delete()
    return redirect('user_list') 


# Photographer Section
def photographer_dashboard(request):
    try:
        photographer_details = PhotomanDetails.objects.get(user=request.user)
    except PhotomanDetails.DoesNotExist:
        photographer_details = None  
    is_profile_approved = photographer_details.status == 'approved' if photographer_details else False
    return render(request, "photographer_dashboard.html", {
        'user': request.user,
        'photographer_details': photographer_details,
        'is_profile_approved': is_profile_approved })


@login_required
def complete_profile_photographer(request):
    user = request.user
    if user.role != 'photographer':
        return redirect("login")  

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        place = request.POST.get("place")
        aadhar_image = request.FILES.get("aadhar_image")  
        
        photoman_details, created = PhotomanDetails.objects.update_or_create(
            user=user,  
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number,
                "place": place,
                "aadhar_image": aadhar_image if aadhar_image else None, },)

        return redirect("photographer_dashboard")

    try:
        photoman_details = PhotomanDetails.objects.get(user=user)
        context = {
            "first_name": photoman_details.first_name,
            "last_name": photoman_details.last_name,
            "email": photoman_details.email,
            "phone_number": photoman_details.phone_number,
            "place": photoman_details.place,
        }
    except PhotomanDetails.DoesNotExist:
        context = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "phone_number": "",
            "place": "", }
    return render(request, "complete_profile_photographer.html", context)


@login_required
def add_image(request):
    if not hasattr(request.user, 'photomandetails'):
        return render(request, 'error.html', {'message': 'You must be a registered photographer to upload images.'})
    photographer = request.user.photomandetails

    if request.method == 'POST':
        spot = request.POST.get('spot')
        description = request.POST.get('desc')  
        uploaded_file = request.FILES.get('image')

        if spot and uploaded_file and description:  
            fs = FileSystemStorage()
            filename = fs.save(f'working_images/{uploaded_file.name}', uploaded_file)

            PhotographyImages.objects.create(
                photographer=photographer,
                image=filename,
                spot=spot,
                description=description )
            return redirect('photographer_dashboard')
        else:
            return render(request, 'add_image.html', {'error_message': 'Spot, image, and description are required.'})
    return render(request, 'add_image.html')


@login_required
def view_images(request):
    try:
        photographer = request.user.photomandetails  
    except AttributeError:
        return render(request, 'error.html', {'message': 'You do not have permission to view images.'})
    images = PhotographyImages.objects.filter(photographer=photographer)
    return render(request, 'view_image.html', {'images': images})


@login_required
def edit_image(request, image_id):
    try:
        image = PhotographyImages.objects.get(id=image_id, photographer=request.user.photomandetails)
    except (PhotographyImages.DoesNotExist, AttributeError):
        return render(request, 'error.html', {'message': 'Image not found or access denied.'})

    if request.method == 'POST':
        image.spot = request.POST.get('spot')
        image.description = request.POST.get('desc')
        if 'image' in request.FILES:
            image.image = request.FILES['image']
        image.save()
        return redirect('view_images')
    return render(request, 'edit_image.html', {'image': image})


@login_required
def delete_image(request, image_id):
    try:
        image = PhotographyImages.objects.get(id=image_id, photographer=request.user.photomandetails)
    except (PhotographyImages.DoesNotExist, AttributeError):
        return render(request, 'error.html', {'message': 'Image not found or access denied.'})

    if request.method == 'POST':
        image.delete()
        return redirect('view_images')
    return render(request, 'confirm_delete.html', {'image': image})


# User Section
@login_required
def user_dashboard(request):
    if request.user.role != "user":
        return redirect('index') 
    profile = None
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.email = request.POST.get('email')
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')
        profile.save()
        return redirect('user_dashboard')
    profile_filled = all([profile.first_name, profile.last_name, profile.phone_number, profile.address])
    return render(request, 'user_dashboard.html', {'user': request.user, 'profile': profile, 'profile_filled': profile_filled})


def photographers_view(request):
    photographers = PhotomanDetails.objects.filter(status='approved')  
    return render(request, 'photographers.html', {'photographers': photographers})


def photographer_detail(request, id):
    photographer = get_object_or_404(PhotomanDetails, id=id)
    images = PhotographyImages.objects.filter(photographer=photographer)
    return render(request, 'photographer_detail.html', {
        'photographer': photographer,
        'images': images, })


def index1(request):
    return render(request,"index1.html")
















