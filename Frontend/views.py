from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from Backend.models import MovieDB, ShowTimeDB
from Frontend.models import UserDB, ReviewDB,UserMessagesDB,SeatDB, UserBookingDB
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

# Create your views here
def index(request):
    today = datetime.today()
    next_three_days = [today + timedelta(days=i) for i in range(0, 4)]
    movies=MovieDB.objects.filter(MovieStatus="Now Showing")
    movieslist = MovieDB.objects.filter(MovieStatus="Coming Soon")
    now_movie=ShowTimeDB.objects.all()
    return render(request, 'index.html', {'next_three_days': next_three_days, 'movies':movies, 'movieslist':movieslist, 'now_movie':now_movie})



def login_signup(request):
    return render(request, 'Login.html')

def nowshowing(request):
    lang=MovieDB.objects.filter(MovieStatus='Now Showing').values_list('MovieLanguage',flat=True).distinct()
    genr=MovieDB.objects.filter(MovieStatus='Now Showing').values_list('MovieGenre',flat=True).distinct()
    types=MovieDB.objects.filter(MovieStatus='Now Showing').values_list('MovieType',flat=True).distinct()
    movies=MovieDB.objects.filter(MovieStatus="Now Showing")
    languages = request.GET.getlist('langua')
    genres = request.GET.getlist('genre')
    modes = request.GET.getlist('mode')
    filtered_movies = MovieDB.objects.filter(MovieStatus="Now Showing")
    #print("ffdaDA", languages)
    if languages:
        filtered_movies = filtered_movies.filter(MovieLanguage__in=languages)

        # for i in filtered_movies:
        #     print(i.MovieName)
    if genres:
        filtered_movies = filtered_movies.filter(MovieGenre__in=genres)


    if modes:
        filtered_movies = filtered_movies.filter(MovieType__in=modes)

    return render(request, 'NowShowing.html', {'lang': lang, 'genr':genr,'types':types, 'movies':movies,
                                               'filtered_movies': filtered_movies })

def comingsoon(request):
    lang=MovieDB.objects.filter(MovieStatus='Coming Soon').values_list('MovieLanguage',flat=True).distinct()
    genr=MovieDB.objects.filter(MovieStatus='Coming Soon').values_list('MovieGenre',flat=True).distinct()
    types=MovieDB.objects.filter(MovieStatus='Coming Soon').values_list('MovieType',flat=True).distinct()
    movies=MovieDB.objects.filter(MovieStatus="Coming Soon")
    languages = request.GET.getlist('langua')
    genres = request.GET.getlist('genre')
    modes = request.GET.getlist('mode')
    filtered_movies = MovieDB.objects.filter(MovieStatus="Coming Soon")
    #print("ffdaDA", languages)
    if languages:
        filtered_movies = filtered_movies.filter(MovieLanguage__in=languages)

        # for i in filtered_movies:
        #     print(i.MovieName)
    if genres:
        filtered_movies = filtered_movies.filter(MovieGenre__in=genres)
    if modes:
        filtered_movies = filtered_movies.filter(MovieType__in=modes)

    return render(request, 'NowShowing.html', {'lang': lang, 'genr':genr,'types':types, 'movies':movies,
                                               'filtered_movies': filtered_movies })

def movie_details(request, movie_id):
    movie=MovieDB.objects.get(id=movie_id)
    mn=movie.MovieName
    review=ReviewDB.objects.filter(MovieName=mn)
    review_count=review.count()
    print(review_count)
    return render(request, 'MovieDetails.html',{'movie':movie, 'review':review, 'review_count':review_count})

def contactus(request):
    return render(request, 'ContactUs.html')

def saveuser(request):
    if request.method=="POST":
        un = request.POST.get("username")
        em=request.POST.get("email")
        mo=request.POST.get("contact")
        pw=request.POST.get("password")
        cpw=request.POST.get("cpassword")
        if (pw == cpw):
            # hashed_password = make_password(pw)
            obj = UserDB(UserName=un,UserEmail=em, UserContact=mo, UserPassword=pw)
            obj.save()
            # messages.success(request, "Registration done successfully..! Login Now..")
            return redirect('index')
        else:
            # messages.error(request,"Password and Confirm password are not matching")
            return redirect('login')

def user_login(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        pw=request.POST.get('password')
        # password_matches = check_password(pw, UserPassword)
        print(uname,pw)
        if UserDB.objects.filter(UserName=uname, UserPassword=pw).exists():
            request.session['UserName'] = uname
            request.session['UserPassword'] = pw
            return redirect(index)
        else:
            return redirect(login_signup)
    return redirect(login_signup)

def user_logout(request):
    del request.session['UserName']
    del request.session['UserPassword']
    # messages.success(request, "Successfully logged out..!")
    return redirect(login_signup)

def post_review(request, movie_id):
    if request.method=="POST":
        movie=MovieDB.objects.get(id=movie_id)
        moviename=movie.MovieName
        review=request.POST.get('review')
        date=datetime.now().date()
        username=request.session['UserName']
        # print(moviename,review,date,username)
        obj=ReviewDB(UserName=username, Review=review,Date=date,MovieName=moviename)
        obj.save()
        return redirect(nowshowing)

def save_message(request):
    if request.method == "POST":
        na=request.POST.get('name')
        em=request.POST.get('email')
        sub=request.POST.get('subject')
        msg=request.POST.get('message')
        dat=datetime.now().date()
        obj=UserMessagesDB(Name=na,Email=em,Subject=sub,Message=msg,PostDate=dat)
        obj.save()
        return redirect(contactus)

@login_required
def my_profile(request):
    username = request.session.get("UserName")
    user_details = UserDB.objects.get(UserName=username)
    return render(request, 'UserProfile.html',{'user_details':user_details})


def initialize_seat_statuses(selected_date, show_name):
    if not SeatDB.objects.filter(Date=selected_date, ShowTimeName=show_name).exists():
        row_to_seat_type = {
            'A': 'Premium',
            'B': 'Premium',
            'C': 'Premium',
            'D': 'Premium',
            'E': 'Premium',
            'F': 'Premium',
            'G': 'Premium',
            'H': 'Premium',
            'I': 'Premium',
            'J': 'Premium',
        }
        for row in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K','L', 'M', 'N']:
            for seat_number in range(1, 18):
                seat_number_str = f'{row}{seat_number}'
                seat_type = row_to_seat_type.get(row, 'Standard')
                if not SeatDB.objects.filter(Date=selected_date, ShowTimeName=show_name, SeatNumber=seat_number_str).exists():
                    seat = SeatDB(SeatNumber=seat_number_str, RowNumber=row,SeatStatus='available',SeatType=seat_type, Date=selected_date, ShowTimeName=show_name)
                    seat.save()
def seating_plan(request):
    selected_date = request.POST.get('selected_date')
    selected_movie = request.POST.get('selected_movie')
    ShowTimeNames = ShowTimeDB.objects.filter(MovieName=selected_movie, Date=selected_date).values_list('ShowTimeName', flat= True)
    for show_name in ShowTimeNames:
        initialize_seat_statuses(selected_date, show_name)
    seat_data = SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames)
    seat_data_A=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="A")
    seat_data_B=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="B")
    seat_data_C=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="C")
    seat_data_D=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="D")
    seat_data_E=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="E")
    seat_data_F=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="F")
    seat_data_G=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="G")
    seat_data_H=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="H")
    seat_data_I=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="I")
    seat_data_J=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium", RowNumber="J")
    seat_data_K=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Standard", RowNumber="K")
    seat_data_L=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Standard", RowNumber="L")
    seat_data_M=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Standard", RowNumber="M")
    seat_data_N=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Standard", RowNumber="N")
    seat_data_pre=SeatDB.objects.filter(Date=selected_date, ShowTimeName__in=ShowTimeNames, SeatType="Premium")
    if selected_date:
        if request.session.get("UserName"):
            show=ShowTimeDB.objects.filter(MovieName=selected_movie, Date=selected_date)
            context={'selected_date':selected_date,
                     'selected_movie':selected_movie,
                     'show':show,
                     'seat_data':seat_data,
                     'seat_data_A':seat_data_A,
                     'seat_data_B':seat_data_B,
                     'seat_data_C':seat_data_C,
                     'seat_data_D':seat_data_D,
                     'seat_data_E':seat_data_E,
                     'seat_data_F':seat_data_F,
                     'seat_data_G':seat_data_G,
                     'seat_data_H':seat_data_H,
                     'seat_data_I':seat_data_I,
                     'seat_data_J':seat_data_J,
                     'seat_data_K':seat_data_K,
                     'seat_data_L':seat_data_L,
                     'seat_data_M':seat_data_M,
                     'seat_data_N': seat_data_N,
                     'seat_data_pre':seat_data_pre}
            return render(request, 'Seating.html', context)
    else:
        return render(request, 'Login.html')

def submit_booking(request):
    if request.method == 'POST':
        na = request.POST.get('screenName')
        shn = request.POST.get('showName')
        sht = request.POST.get('showStartTime')
        mn = request.POST.get('movieName')
        un = request.POST.get('userName')
        fp = request.POST.get('finalPrice')
        print(na,shn,mn,fp,un)
        selected_seats_data = request.POST.getlist('seats')
        # print(selected_seats_data)
        selected_seats = [seat.split(':')[0] for seat in selected_seats_data if seat.split(':')[1] == 'selected']
        if selected_seats:
            SeatDB.objects.filter(SeatNumber__in=selected_seats).update(SeatStatus='booked')
            return redirect('movie_checkout')
        else:
            return redirect('index') #enter error message

def movie_checkout(request):
    return render(request, 'MovieCheckOut.html')



