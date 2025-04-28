
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SuperUserSignUpForm
from django.contrib.auth import login
from .forms import UserInfoForm
from django.contrib import messages
from .models import UserInfo
import base64




def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    elif request.user.is_superuser:
        return redirect('/adminpanel')
    print(request.user.is_superuser,"is superuser")
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request, 'contact.html')

from .models import UserInfo  # import your model if not done

def admin(request):
    if request.user.is_anonymous:
        return redirect('/login')
    print(request.user.is_superuser, "is superuser")
    user_data = UserInfo.objects.all()  # assuming model name is UserInfo
    return render(request, 'admin.html', {'user_data': user_data})



def loginuser(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user.is_superuser,"is superuser 1")
        if username == 'admin' and password == 'admin':
            request.session['username'] = username
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request,'login.html')
    return render(request,'login.html')

def logoutuser(request):
    auth_logout(request)
    request.session.flush()  # This clears all session data
    response = redirect('/login') # Redirect after logout
    response.delete_cookie('sessionid')   # Just to be safe, manually delete cookie
    response.delete_cookie('csrftoken')   # Just to be safe, manually delete cookie
    return response
def signupuser(request):
    if request.method == 'POST':
        form = SuperUserSignUpForm(request.POST)
        # print(form,"form")
        role = request.POST.get('role')
        print(role,"role") 
        if role == 'superuser':
         if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            login(request, user)
            print("superuser")
            return redirect('/adminpanel')  # or 'admin:index' to go to admin dashboard
        else:
         if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = False
            user.is_staff = False
            user.is_active = False
            user.save()
            login(request, user)
            print("NORMAL USER")
            return redirect('/')
            print("not admin") 
        
    else:
        form = SuperUserSignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib import messages  # Add this if not already there

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserInfoForm

def save_user_info(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        user_info = get_object_or_404(UserInfo, id=user_id) if user_id else None

        # Handle delete
        if action == 'delete' and user_info:
            user_info.delete()
            messages.success(request, "User information deleted.")
            return redirect('/adminpanel')

        # Create or update form
        form = UserInfoForm(request.POST, request.FILES, instance=user_info)

        if form.is_valid():
            image_file = request.FILES.get('image_base64')
            print("Image file:", image_file)  # Debugging line
            if image_file:
                # Convert and save new image
                file_content = image_file.read()
                base64_string = base64.b64encode(file_content).decode()
                form.instance.image_base64 = base64_string
                print("New image uploaded and saved.")
            elif user_info:
                # Keep existing image if no new image uploaded
                form.instance.image_base64 = user_info.image_base64
                print("No new image uploaded. Keeping the old one.")

            form.save()

            if user_info:
                messages.success(request, "User information updated.")
            else:
                messages.success(request, "New user information created.")
        else:
            messages.error(request, "There was an error processing the form.")
            print(form.errors)

    return redirect('/adminpanel')
def admin_panel(request):
    # Retrieve all user information (if you want to display them on the admin panel)
    user_info_list = UserInfo.objects.all()
    return render(request, 'adminpanel.html', {'user_info_list': user_info_list})


def dashboard(request):
    form = UserInfoForm()
    return render(request, 'dashboard.html', {'form': form})
def dashboard(request): 
    return render(request,'dashboard.html')
def success(request):
    return render(request, 'success.html')







