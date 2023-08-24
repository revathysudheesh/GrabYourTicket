from django.shortcuts import render, redirect
from Backend.models import CustomUser,TheatreDB, ScreenDB, MovieDB, ShowTimeDB
from Frontend.models import UserMessagesDB, UserBookingDB, UserDB
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def admin_home(request):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        users=UserDB.objects.all()
        user_count = users.count()
        shows=ShowTimeDB.objects.all()
        show_count=shows.count()
        movies=MovieDB.objects.filter(MovieStatus="Now Showing")
        movie_count=movies.count()
        booking=UserBookingDB.objects.all()
        booking_count=booking.count()
        return render(request, 'Dashboard.html',{'first_name':first_name, 'profile_image':profile_image,
                                                 'user_count':user_count, 'show_count':show_count,
                                                 'movie_count':movie_count, 'booking_count':booking_count})
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

def admin_profile(request):
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
        user = CustomUser.objects.get(id=dataid)
        existing_user_with_phone = CustomUser.objects.filter(phone_number=pn).exclude(id=user.id).first()
        if existing_user_with_phone:
            messages.error(request, "Mobile Number already exists")
            return redirect(list_admin)
        else:
            CustomUser.objects.filter(id=dataid).update(first_name=fn,last_name=ln,email=em,phone_number=pn,profile_image=file)
            messages.success(request, "Admin details updated successfully")
            return redirect(list_admin)

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

def submit_admin(request):
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
        elif CustomUser.objects.filter(phone_number=mo).exists():
            flag = 2
        if(flag == 0):
            custom_user=CustomUser.objects.create_user(username=un, first_name=fn,last_name=ln,
                                                           email=em,password=pw,is_staff=False, is_active=True,
                                                           is_superuser=False,phone_number=mo,profile_image=im)
            messages.success(request, "Admin added successfully")
            return redirect('list_admin')
        elif(flag==1):
            messages.error(request, "Username already exists in the system")
            return redirect('add_admin')
        else:
            messages.error(request, "Phone number already exists in the system")
            return redirect('add_admin')

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
    return redirect('listF_admin')

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
        messages.success(request, "Theatre details updated successfully")
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
        sc=int(request.POST.get("screen-capacity"))
        ps=int(request.POST.get("premium-seats"))
        ss=int(request.POST.get("standard-seats"))
        if(sc==ss+ps):
            obj = ScreenDB(ScreenName=sn, ScreenCapacity=sc,PremiumCapacity=ps,StandardCapacity=ss, ScreenStatus="Active")
            obj.save()
            screens_count=ScreenDB.objects.count()
            TheatreDB.objects.filter(id=1).update(TheatreScreen=screens_count)
            theater = TheatreDB.objects.get(id=1)
            theater.TheatreCapacity += sc
            theater.save()
            messages.success(request, "Screen Added")
        else:
            messages.error(request, "Total Capacity and sum of premium and standard not same")
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
        sta = request.POST.get("status")
        ScreenDB.objects.filter(id=dataid).update(ScreenName=sn, ScreenStatus=sta)
        messages.success(request, "Successfully Updated Details")
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
        pos1 = request.FILES['poster1']
        pos2 = request.FILES['poster2']
        pos3 = request.FILES['poster3']
        ty=request.POST.get("type")
        da=request.POST.get("date")
        sta = request.POST.get("status")
        dur=request.POST.get("duration")
        lin=request.POST.get("link")
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
        obj=MovieDB(MovieName=na,MovieLanguage=la,MovieGenre=ge,MoviePoster=pos,MoviePoster1=pos1,MoviePoster2=pos2,
                    MoviePoster3=pos3, MovieType=ty,MovieSynopsis=sy,
                    MovieDuration=dur, MovieTrailer=lin, MovieStatus=sta, MovieRelease=da,MovieActor1Name=act1na, MovieActor1Image=act1im, MovieActor2Name=act2na,
                    MovieActor2Image=act2im, MovieActor3Name=act3na, MovieActor3Image=act3im, MovieActor4Name=act4na,
                    MovieActor4Image=act4im, MovieActor5Name=act5na, MovieActor5Image=act5im,MovieCrew1Name=crew1na, MovieCrew1Role=crew1ro,MovieCrew1Image=crew1im,
                    MovieCrew2Name=crew2na, MovieCrew2Role=crew2ro,MovieCrew2Image=crew2im,
                    MovieCrew3Name=crew3na, MovieCrew3Role=crew3ro, MovieCrew3Image=crew3im,
                    MovieCrew4Name=crew4na, MovieCrew4Role=crew4ro, MovieCrew4Image=crew4im,
                    MovieCrew5Name=crew5na, MovieCrew5Role=crew5ro, MovieCrew5Image=crew5im
                    )
        obj.save()
        messages.success(request, "New Movie Added")
        return redirect('list_movie')

def list_movie(request):
    if request.user.is_authenticated:
        user=request.user
        movie=MovieDB.objects.all()
        return render(request, 'ListMovies.html',{'user':user, 'movie':movie})
    else:
        return redirect(login_reg)

def edit_movie(request,dataid):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        movie = MovieDB.objects.get(id=dataid)
        return render(request, 'EditMovie.html',{'first_name':first_name, 'profile_image':profile_image, 'movie':movie})
    else:
        return redirect('login_reg')

def update_movie(request,dataid):
    if request.method=="POST":
        na=request.POST.get("name")
        sy=request.POST.get("synopsis")
        la=request.POST.get("lang")
        ge=request.POST.get("genre")
        ty=request.POST.get("type")
        da=request.POST.get("date")
        sta=request.POST.get("status")
        lin=request.POST.get("link")
        dur=request.POST.get("duration")
        act1na = request.POST.get("actor1name")
        act2na = request.POST.get("actor2name")
        act3na = request.POST.get("actor3name")
        act4na = request.POST.get("actor4name")
        act5na = request.POST.get("actor5name")
        crew1na = request.POST.get("Crew1name")
        crew1ro = request.POST.get("Crew1role")
        crew2na = request.POST.get("Crew2name")
        crew2ro = request.POST.get("Crew2role")
        crew3na = request.POST.get("Crew3name")
        crew3ro = request.POST.get("Crew3role")
        crew4na = request.POST.get("Crew4name")
        crew4ro = request.POST.get("Crew4role")
        crew5na = request.POST.get("Crew5name")
        crew5ro = request.POST.get("Crew5role")
        try:
            im = request.FILES['poster']
            fs = FileSystemStorage()
            file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            file = MovieDB.objects.get(id=dataid).MoviePoster
        try:
            im = request.FILES['poster1']
            fs = FileSystemStorage()
            poster_file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            poster_file = MovieDB.objects.get(id=dataid).MoviePoster1
        try:
            im = request.FILES['poster2']
            fs = FileSystemStorage()
            post_file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            post_file = MovieDB.objects.get(id=dataid).MoviePoster2
        try:
            im = request.FILES['poster3']
            fs = FileSystemStorage()
            poste_file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            poste_file = MovieDB.objects.get(id=dataid).MoviePoster3
        try:
            act1im = request.FILES['actor1image']
            fs = FileSystemStorage()
            act1im_file = fs.save(act1im.name, act1im)
        except MultiValueDictKeyError:
            act1im_file = MovieDB.objects.get(id=dataid).MovieActor1Image
        try:
            act2im = request.FILES['actor2image']
            fs = FileSystemStorage()
            act2im_file = fs.save(act2im.name, act2im)
        except MultiValueDictKeyError:
            act2im_file = MovieDB.objects.get(id=dataid).MovieActor2Image
        try:
            act3im = request.FILES['actor3image']
            fs = FileSystemStorage()
            act3im_file = fs.save(act3im.name, act3im)
        except MultiValueDictKeyError:
            act3im_file = MovieDB.objects.get(id=dataid).MovieActor3Image
        try:
            act4im = request.FILES['actor4image']
            fs = FileSystemStorage()
            act4im_file = fs.save(act4im.name, act4im)
        except MultiValueDictKeyError:
            act4im_file = MovieDB.objects.get(id=dataid).MovieActor4Image
        try:
            act5im = request.FILES['actor5image']
            fs = FileSystemStorage()
            act5im_file = fs.save(act5im.name, act5im)
        except MultiValueDictKeyError:
            act5im_file = MovieDB.objects.get(id=dataid).MovieActor5Image
        try:
            crew1im = request.FILES['Crew1image']
            crew1im = request.FILES['Crew1image']
            fs = FileSystemStorage()
            crew1im_file = fs.save(crew1im.name, crew1im)
        except MultiValueDictKeyError:
            crew1im_file = MovieDB.objects.get(id=dataid).MovieCrew1Image
        try:
            crew2im = request.FILES['Crew2image']
            fs = FileSystemStorage()
            crew2im_file = fs.save(crew2im.name, crew2im)
        except MultiValueDictKeyError:
            crew2im_file = MovieDB.objects.get(id=dataid).MovieCrew2Image
        try:
            crew3im = request.FILES['Crew3image']
            fs = FileSystemStorage()
            crew3im_file = fs.save(crew3im.name, crew3im)
        except MultiValueDictKeyError:
            crew3im_file = MovieDB.objects.get(id=dataid).MovieCrew3Image

        try:
            crew4im = request.FILES['Crew4image']
            fs = FileSystemStorage()
            crew4im_file = fs.save(crew4im.name, crew4im)
        except MultiValueDictKeyError:
            crew4im_file = MovieDB.objects.get(id=dataid).MovieCrew4Image

        try:
            crew5im = request.FILES['Crew5image']
            fs = FileSystemStorage()
            crew5im_file = fs.save(crew5im.name, crew5im)
        except MultiValueDictKeyError:
            crew5im_file = MovieDB.objects.get(id=dataid).MovieCrew5Image
        MovieDB.objects.filter(id=dataid).update(MovieName=na, MovieLanguage=la, MovieGenre=ge, MoviePoster=file,
                                                 MoviePoster1=poster_file,MoviePoster2=post_file,MoviePoster3=poste_file,MovieType=ty,
                                                 MovieSynopsis=sy,MovieDuration=dur, MovieStatus=sta,MovieRelease=da, MovieActor1Name=act1na,
                                                 MovieTrailer=lin, MovieActor1Image=act1im_file, MovieActor2Name=act2na,
                                                 MovieActor2Image=act2im_file, MovieActor3Name=act3na,
                                                 MovieActor3Image=act3im_file, MovieActor4Name=act4na,
                                                 MovieActor4Image=act4im_file, MovieActor5Name=act5na,
                                                 MovieActor5Image=act5im_file, MovieCrew1Name=crew1na,
                                                 MovieCrew1Role=crew1ro, MovieCrew1Image=crew1im_file,
                                                 MovieCrew2Name=crew2na, MovieCrew2Role=crew2ro, MovieCrew2Image=crew2im_file,
                                                 MovieCrew3Name=crew3na, MovieCrew3Role=crew3ro, MovieCrew3Image=crew3im_file,
                                                 MovieCrew4Name=crew4na, MovieCrew4Role=crew4ro, MovieCrew4Image=crew4im_file,
                                                 MovieCrew5Name=crew5na, MovieCrew5Role=crew5ro, MovieCrew5Image=crew5im_file,
                                                 )
        return redirect(list_movie)

def delete_movie(request, dataid):
   data=MovieDB.objects.filter(id=dataid)
   data.delete()
   messages.success(request, "Movie successfully removed from the system..!")

def add_show_time(request):
    if request.user.is_authenticated:
        user=request.user
        movies=MovieDB.objects.filter(MovieStatus="Now Showing")
        screens=ScreenDB.objects.all()
        return render(request, 'AddShowTime.html',{'user':user, 'movies':movies, 'screens':screens})
    else:
        return redirect(login_reg)

def submit_show_time(request):
    if request.method == "POST":
        na= request.POST.get("showtime-name")
        mn = request.POST.get("movie-name")
        sn = request.POST.get("screen-name")
        st = request.POST.get("start-time")
        et = request.POST.get("end-time")
        dt = request.POST.get("date")
        ps = request.POST.get("price-std")
        pp = request.POST.get("price-premium")
        # stat=request.POST.get("status")
        screen_det=ScreenDB.objects.filter(ScreenName=sn)
        premium_cap=screen_det[0].PremiumCapacity
        std_cap=screen_det[0].StandardCapacity
        existing_show = ShowTimeDB.objects.filter(ScreenName=sn, ShowTimeName=na, Date=dt)
        if existing_show.exists():
            messages.error(request, "Show already exists")
            return redirect('add_show_time')
        else:
            obj = ShowTimeDB(ShowTimeName=na,MovieName=mn,ScreenName=sn, StartTime=st, EndTime=et,Date=dt,
                         PriceStandard=ps, PricePremium=pp,TotalStandardTickets=std_cap,AvailableStandardTickets=std_cap,
                         TotalPremiumTickets=premium_cap,AvailablePremiumTickets=premium_cap, Status="Open")
            obj.save()
            return redirect('add_show_time')
    return redirect('add_show_time')


def list_showtime(request):
    if request.user.is_authenticated:
        user=request.user
        show=ShowTimeDB.objects.all()
        return render(request, 'ListShowTime.html',{'user':user, 'show':show})
    else:
        return redirect(login_reg)

def edit_showtime(request,dataid):
    if request.user.is_authenticated:
        first_name=request.user.first_name
        profile_image=request.user.profile_image
        movies = MovieDB.objects.all()
        screens = ScreenDB.objects.all()
        showtime = ShowTimeDB.objects.get(id=dataid)
        return render(request, 'EditShowTime.html',{'first_name':first_name, 'profile_image':profile_image, 'showtime':showtime, 'movies':movies, 'screens':screens})
    else:
        return redirect('login_reg')

def update_show_time(request, dataid):
    if request.method == "POST":
        na=request.POST.get("showtime-name")
        mn = request.POST.get("movie-name")
        sn = request.POST.get("screen-name")
        st = request.POST.get("start-time")
        et = request.POST.get("end-time")
        dt = request.POST.get("date")
        ps = request.POST.get("price-std")
        pp = request.POST.get("price-premium")
        ast= request.POST.get("available-standard")
        tst= request.POST.get("total-standard")
        ap = request.POST.get("available-premium")
        tp = request.POST.get("total-premium")
        stat=request.POST.get("status")
        existing_show = ShowTimeDB.objects.filter(ScreenName=sn, ShowTimeName=na, Date=dt)
        if existing_show.exists():
            messages.error(request, "Show already exists")
            return redirect('list_showtime')
        else:
            ShowTimeDB.objects.filter(id=dataid).update(ShowTimeName=na,MovieName=mn,ScreenName=sn, StartTime=st, EndTime=et,Date=dt,
                         PriceStandard=ps, PricePremium=pp,TotalStandardTickets=tst,AvailableStandardTickets=ast,
                         TotalPremiumTickets=tp,AvailablePremiumTickets=ap, Status=stat)
            return redirect('list_showtime')
    return redirect('list_showtime')

def delete_showtime(request,dataid):
    data = ShowTimeDB.objects.filter(id=dataid)
    data.delete()
    messages.success(request, "Showtime successfully removed from the system..!")
    return redirect('list_showtime')


# def add_seating(request):
#     if request.user.is_authenticated:
#         user=request.user
#         shows=ShowTimeDB.objects.all()
#         return render(request, 'AddSeating.html',{'user':user, 'shows':shows})
#     else:
#         return redirect(login_reg)

def delete_screen(request, dataid):
    data=ScreenDB.objects.filter(id=dataid)
    nam=data[0].ScreenName
    cap=data[0].ScreenCapacity
    theater = TheatreDB.objects.get(id=1)
    theater.TheatreCapacity -= cap
    theater.TheatreScreen -=1
    showtimes=ShowTimeDB.objects.filter(ScreenName=nam)

    showtimes.delete()
    theater.save()
    data.delete()
    messages.success(request, "Screen successfully removed from the system..!")
    return redirect(list_screen)

def view_messages(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        profile_image = request.user.profile_image
        msgs=UserMessagesDB.objects.all()
        return render(request, 'ViewMessages.html', {'first_name': first_name, 'profile_image': profile_image,'msgs': msgs})
    else:
        return redirect('login_reg')

def view_bookings(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        profile_image = request.user.profile_image
        current_datetime = timezone.now()

        bookings=UserBookingDB.objects.filter(SelectedDate__gte=current_datetime)
        return render(request, 'ViewBookings.html', {'first_name': first_name, 'profile_image': profile_image,'bookings': bookings})
    else:
        return redirect('login_reg')
def view_bookings_old(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        profile_image = request.user.profile_image
        current_datetime = timezone.now()

        bookings=UserBookingDB.objects.filter(SelectedDate__lt=current_datetime)
        return render(request, 'ViewBookings.html', {'first_name': first_name, 'profile_image': profile_image,'bookings': bookings})
    else:
        return redirect('login_reg')

def view_users(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        profile_image = request.user.profile_image
        users=UserDB.objects.all()
        print(users)
        return render(request, 'ViewUsers.html', {'first_name': first_name, 'profile_image': profile_image,
                                                  'users': users})
    else:
        return redirect('login_reg')