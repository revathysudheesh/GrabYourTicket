from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from Backend.models import CustomUser,TheatreDB, ScreenDB, MovieDB
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
                messages.success(request, "Signed up successfully")
                return redirect('login_reg')
            else:
                messages.error(request, "Password and Confirm Password are not same")
                return redirect('login_reg')
        else:
            messages.error(request, "Username already exists in the system")
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
                messages.success(request, "Logined successfully")
                return redirect(admin_home)
            else:
                messages.error(request, "Check the credentials")
                return redirect(login_reg)
        elif CustomUser.objects.filter(username=uname, password=pw).exists():
            request.session['username']=uname
            request.session['password']=pw
            messages.success(request, "Logined successfully")
            return redirect(admin_home)
        else:
            messages.error(request, "Check the credentials")
            return redirect(login_reg)

def admin_logout(request):
    del request.session['username']
    del request.session['password']
    messages.success(request, "Successfully Signed Out")
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
        messages.success(request, "Profile updated successfully")
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
            messages.error(request, "Password and Repeat Password are not same")
            return redirect(change_password)
        else:
            user.set_password(np)
            user.save()
            messages.success(request, "Successfully changed password")
            return redirect(admin_logout)
    return redirect(change_password)

def add_admin(request):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        return render(request, 'AddUser.html',{'first_name':first_name, 'profile_image':profile_image})
    else:
        return redirect('login_reg')

def list_admin(request):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        users=CustomUser.objects.all;
        return render(request, 'ListUser.html',{'first_name':first_name, 'profile_image':profile_image, 'users':users})
    else:
        return redirect('login_reg')

def edit_admin(request, dataid):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        profile_image = request.user.profile_image
        userr = CustomUser.objects.get(id=dataid)
        return render(request, 'EditUser.html',{'first_name': first_name, 'profile_image': profile_image, 'userr': userr})
    else:
        return redirect('login_reg')

def delete_admin(request, dataid):
    userr=CustomUser.objects.filter(id=dataid)
    userr.delete()
    messages.success(request, "User successfully removed from the system..!")
    return redirect('list_admin')

def change_password_admin(request, dataid):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        profile_image = request.user.profile_image
        userr = CustomUser.objects.get(id=dataid)
        return render(request, 'ChangePasswordStaffAdmin.html',
                      {'first_name': first_name, 'profile_image': profile_image, 'userr': userr})
    else:
        return redirect('login_reg')

def update_password_admin(request,dataid):
    if request.method == 'POST':
        np = request.POST.get('new-password')
        rnp = request.POST.get('repeat-password')
        if np != rnp:
            messages.error(request, "Password and Repeat Password are not same")
            return redirect(list_admin)
        else:
            staff_user=CustomUser.objects.get(id=dataid)
            staff_user.set_password(np)
            staff_user.save()
            messages.success(request, "Successfully changed password")
            return redirect(list_admin)
    return redirect(list_admin)

def theatre_details(request):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        theatre = TheatreDB.objects.all()
        return render(request, 'TheatreDetails.html', {'theatre': theatre, 'first_name': first_name, 'profile_image': profile_image,})
def edit_theatre(request, dataid):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        theatre = TheatreDB.objects.get(id=dataid)
        return render(request, 'EditTheatre.html',{'first_name':first_name, 'profile_image':profile_image, 'theatre':theatre})
    else:
        return redirect('login_reg')

def update_theatre(request, dataid):
    if request.method=="POST":
        na=request.POST.get("name")
        ad=request.POST.get("address")
        con=request.POST.get("contact")
        we=request.POST.get("website")
        em=request.POST.get("email")
        cp=request.POST.get("capacity")
        sc=request.POST.get("screen")
        sta=request.POST.get("status")
        try:
            im = request.FILES['img']
            fs = FileSystemStorage()
            file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            file = TheatreDB.objects.get(id=dataid).TheatreImage
        TheatreDB.objects.filter(id=dataid).update(TheatreName=na,TheatreAddress=ad,TheatreContact=con, TheatreWebsite=we, TheatreEmail=em,TheatreCapacity=cp,TheatreScreen=sc, TheatreStatus=sta,
                      TheatreImage=file)
        return redirect('theatre_details')

def add_screen(request):
    if request.user.is_authenticated:
        user=request.user
        return render(request, 'AddScreen.html',{'user':user})
    else:
        return redirect(login_reg)

def list_screen(request):
    if request.user.is_authenticated:
        user=request.user
        screen=ScreenDB.objects.all()
        return render(request, 'ListScreen.html',{'user':user, 'screen':screen})
    else:
        return redirect(login_reg)

def submit_screen(request):
    if request.method == "POST":
        sn=request.POST.get("screen-name")
        sc=request.POST.get("screen-capacity")
        sa=request.POST.get("available-seats")
        obj = ScreenDB(ScreenName=sn, ScreenCapacity=sc,SeatAvail=sa)
        obj.save()
        messages.success(request, "Screen Added")
        return redirect('list_screen')

def edit_screen(request, dataid):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        screen = ScreenDB.objects.get(id=dataid)
        return render(request, 'EditScreen.html',{'first_name':first_name, 'profile_image':profile_image, 'screen':screen})
    else:
        return redirect('list_screen')

def update_screen(request, dataid):
    if request.method=="POST":
        sn = request.POST.get("screen-name")
        sc = request.POST.get("screen-capacity")
        sa = request.POST.get("available-seats")
        ScreenDB.objects.filter(id=dataid).update(ScreenName=sn, ScreenCapacity=sc,SeatAvail=sa)
        return redirect('list_screen')

def add_movie(request):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        return render(request, 'AddMovie.html',{'first_name':first_name, 'profile_image':profile_image})
    else:
        return redirect('login_reg')

def submit_movie(request):
    if request.method=="POST":
        na=request.POST.get("name")
        sy=request.POST.get("synopsis")
        la=request.POST.get("lang")
        ge=request.POST.get("genre")
        pos=request.FILES['poster']
        ty=request.POST.get("type")
        da=request.POST.get("date")
        dur=request.POST.get("duration")
        act1na = request.POST.get("actor1name")
        act1im = request.FILES['actor1image']
        act2na = request.POST.get("actor2name")
        act2im = request.FILES['actor2image']
        act3na = request.POST.get("actor3name")
        act3im = request.FILES['actor3image']
        act4na = request.POST.get("actor4name")
        act4im = request.FILES['actor4image']
        act5na = request.POST.get("actor5name")
        act5im = request.FILES['actor5image']
        crew1na = request.POST.get("crew1name")
        crew1ro = request.POST.get("crew1role")
        crew1im = request.FILES['crew1image']
        crew2na = request.POST.get("crew2name")
        crew2ro = request.POST.get("crew2role")
        crew2im = request.FILES['crew2image']
        crew3na = request.POST.get("crew3name")
        crew3ro = request.POST.get("crew3role")
        crew3im = request.FILES['crew3image']
        crew4na = request.POST.get("crew4name")
        crew4ro = request.POST.get("crew4role")
        crew4im = request.FILES['crew4image']
        crew5na = request.POST.get("crew5name")
        crew5ro = request.POST.get("crew5role")
        crew5im = request.FILES['crew5image']
        obj=MovieDB(MovieName=na,MovieLanguage=la,MovieGenre=ge,MoviePoster=pos,MovieType=ty,MovieSynopsis=sy,
                    MovieDuration=dur,MovieRelease=da,MovieActor1Name=act1na, MovieActor1Image=act1im, MovieActor2Name=act2na,
                    MovieActor2Image=act2im, MovieActor3Name=act3na, MovieActor3Image=act3im, MovieActor4Name=act4na,
                    MovieActor4Image=act4im, MovieActor5Name=act5na, MovieActor5Image=act5im,MovieCrew1Name=crew1na, MovieCrew1Role=crew1ro,MovieCrew1Image=crew1im,
                    MovieCrew2Name=crew2na, MovieCrew2Role=crew2ro,MovieCrew2Image=crew2im,
                    MovieCrew3Name=crew3na, MovieCrew3Role=crew3ro, MovieCrew3Image=crew3im,
                    MovieCrew4Name=crew4na, MovieCrew4Role=crew4ro, MovieCrew4Image=crew4im,
                    MovieCrew5Name=crew5na, MovieCrew5Role=crew5ro, MovieCrew5Image=crew5im
                    )
        obj.save()
        return redirect('add_movie')
