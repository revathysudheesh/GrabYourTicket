from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from Backend.models import CustomUser
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

def admin_home(request):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        return render(request, 'Dashboard.html',{'first_name':first_name, 'profile_image':profile_image})
    else:
        return redirect('login_reg')


def login_reg(request):
    return render(request, 'LoginReg.html')

def signup(request):
    if request.method == "POST":
        un=request.POST.get("signup-username")
        fn=request.POST.get("signup-firstname")
        ln=request.POST.get("signup-lastname")
        em=request.POST.get("signup-email")
        mo=request.POST.get("signup-mobile")
        pw=request.POST.get("signup-password")
        cpw=request.POST.get("signup-repeat-password")
        im = request.FILES['signup-profile-photo']
        flag = 0
        if CustomUser.objects.filter(username=un).exists():
            flag = 1
        if (flag == 0):
            if (pw == cpw):
                custom_user=CustomUser.objects.create_user(username=un, first_name=fn,last_name=ln,
                                                           email=em,password=pw,is_staff=False, is_active=True,
                                                           is_superuser=False,phone_number=mo,profile_image=im)
                return redirect('login_reg')
            else:
                return redirect('login_reg')
        else:
            return redirect('login_reg')
def admin_login(request):
   if request.method=="POST":
      uname=request.POST.get('login-username')
      pw=request.POST.get('login-password')
      if CustomUser.objects.filter(username__contains=uname).exists():
         user = authenticate(username=uname, password=pw)
         if user is not None:
            login(request, user)
            request.session['username']=uname
            request.session['password']=pw
            return redirect(admin_home)
         else:
            return redirect(login_reg)
      elif CustomUser.objects.filter(username=uname, password=pw).exists():
            request.session['username']=uname
            request.session['password']=pw
            return redirect(admin_home)

      else:
         return redirect(signup)

def admin_logout(request):
   del request.session['username']
   del request.session['password']
   return redirect(login_reg)

def my_profile(request):
    if request.user.is_authenticated:
        user=request.user
        return render(request, 'MyProfile.html',{'user':user})
    else:
        return redirect(login_reg)
    # return render(request, 'MyProfile.html')

def update_user(request, dataid):
    if request.method == "POST":
        fn=request.POST.get("fname")
        ln=request.POST.get("lname")
        em=request.POST.get("email")
        pn=request.POST.get("contact")
        try:
            im = request.FILES['img']
            fs = FileSystemStorage()
            file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            file = CustomUser.objects.get(id=dataid).profile_image
        CustomUser.objects.filter(id=dataid).update(first_name=fn,last_name=ln,email=em,phone_number=pn,profile_image=file)
        return redirect(admin_home)

def change_password(request):
    if request.user.is_authenticated:
        user=request.user
        return render(request, 'ChangePassword.html',{'user':user})
    else:
        return redirect(login_reg)

def update_password(request):
    if request.method == 'POST':
        cp = request.POST.get('current-password')
        np = request.POST.get('new-password')
        rnp = request.POST.get('repeat-password')
        user = request.user
        if not user.check_password(cp):
            messages.error(request, "Current password not matches")
            return redirect(change_password)
        elif np != rnp:
            messages.error(request, "Password mismatches")
            return redirect(change_password)
        else:
            user.set_password(np)
            user.save()
            messages.success(request, "Success")
            return redirect(admin_logout)
    return redirect(change_password)

