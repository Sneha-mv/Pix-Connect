from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, PhotomanDetails, PhotographyImages
# Create your views here.

def index(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about.html")


def gallery(request):
    return render(request,"gallery.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)
        user.save()
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

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
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)  
    return redirect('index')

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


# Photographer Section
from django.shortcuts import render
from .models import PhotomanDetails

def photographer_dashboard(request):
    # Handle the case when PhotomanDetails is not found for the user
    try:
        photographer_details = PhotomanDetails.objects.get(user=request.user)
    except PhotomanDetails.DoesNotExist:
        photographer_details = None  # Set photographer_details to None if not found
        # Optionally, redirect the user to a profile completion page
        # return redirect('profile_completion_url')  # Uncomment if you want to redirect
    is_profile_approved = photographer_details.status == 'approved' if photographer_details else False
    return render(request, "photographer_dashboard.html", {
        'user': request.user,
        'photographer_details': photographer_details,
        'is_profile_approved': is_profile_approved
    })



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


# User Section
def user_dashboard(request):
    return render(request,"user_dashboard.html")
