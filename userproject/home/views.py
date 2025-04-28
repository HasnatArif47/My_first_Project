
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SuperUserSignUpForm
from django.contrib.auth import login
from .forms import UserInfoForm
from django.contrib import messages
from .models import UserInfo





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
        action = request.POST.get('action')  # Check which button was clicked

        # Safely get the UserInfo object
        if user_id:
            user_info = get_object_or_404(UserInfo, id=user_id)
        else:
            user_info = None

        if action == 'delete' and user_info:
            # If action is delete, delete the user_info from DB
            print("delete", action)
            user_info.delete()
            messages.success(request, "User information deleted.")
            return redirect('/adminpanel')

        if user_id:
            # If user_info exists (update mode)
            form = UserInfoForm(request.POST, instance=user_info)
        else:
            # If user_info does not exist (create mode), assuming you want to create a new UserInfo object
            form = UserInfoForm(request.POST)

        # Process the form (save or show error)
        if form.is_valid():
            form.save()
            if user_info:
                messages.success(request, "User information updated.")
            else:
                messages.success(request, "New user information created.")
        else:
            messages.error(request, "There was an error processing the form.")

    return redirect('/adminpanel')



def dashboard(request):
    form = UserInfoForm()
    return render(request, 'dashboard.html', {'form': form})
def dashboard(request): 
    return render(request,'dashboard.html')
def success(request):
    return render(request, 'success.html')







