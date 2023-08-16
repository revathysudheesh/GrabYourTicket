from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from Backend.models import MovieDB
from Frontend.models import UserDB, ReviewDB,UserMessagesDB
# Create your views here
def index(request):
    today = datetime.today()
    next_three_days = [today + timedelta(days=i) for i in range(1, 4)]
    movies=MovieDB.objects.filter(MovieStatus="Now Showing")
    movieslist = MovieDB.objects.filter(MovieStatus="Coming Soon")
    return render(request, 'index.html', {'next_three_days': next_three_days, 'movies':movies, 'movieslist':movieslist})

def seating_plan(request):
    return render(request, 'Seating.html')

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

def my_profile(request):
    return render(request, 'MyProfile.html')




