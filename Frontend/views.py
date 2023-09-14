from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from Backend.models import MovieDB, ShowTimeDB, TheatreDB
from Frontend.models import UserDB, ReviewDB,UserMessagesDB,SeatDB, UserBookingDB, CheckOutDB
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
import ast
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError



from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

# Create your views here
def index(request):
    today = datetime.today()
    next_three_days = [today + timedelta(days=i) for i in range(0, 4)]
    movies=MovieDB.objects.filter(MovieStatus="Now Showing")
    movieslist = MovieDB.objects.filter(MovieStatus="Coming Soon")
    now_movie=ShowTimeDB.objects.all().values_list('MovieName',flat=True).distinct()
    print(now_movie)
    return render(request, 'index.html', {'next_three_days': next_three_days, 'movies':movies, 'movieslist':movieslist, 'now_movie':now_movie})



def login_signup(request):
    username = request.session.get("UserName")
    if username:
        return render(request, 'index.html')
    else:
        return render(request, 'Login.html')

def nowshowing(request):
    lang=MovieDB.objects.filter(MovieStatus='Now Showing').values_list('MovieLanguage',flat=True).distinct()
    genr=MovieDB.objects.filter(MovieStatus='Now Showing').values_list('MovieGenre',flat=True).distinct()
    types=MovieDB.objects.filter(MovieStatus='Now Showing').values_list('MovieType',flat=True).distinct()
    movies=MovieDB.objects.filter(MovieStatus="Now Showing")
    languages = request.GET.getlist('langua')
    genres = request.GET.getlist('genre')
    print(genres)
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
    filtered_movies = filtered_movies.order_by('-MovieRelease')
    paginator = Paginator(filtered_movies, per_page=2)  # Display 5 items per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'NowShowing.html', {'lang': lang, 'genr':genr,'types':types, 'movies':movies,
                                               'filtered_movies': filtered_movies, 'page':page })

def comingsoon(request):
    lang=MovieDB.objects.filter(MovieStatus='Coming Soon').values_list('MovieLanguage',flat=True).distinct()
    genr=MovieDB.objects.filter(MovieStatus='Coming Soon').values_list('MovieGenre',flat=True).distinct()
    types=MovieDB.objects.filter(MovieStatus='Coming Soon').values_list('MovieType',flat=True).distinct()
    movies=MovieDB.objects.filter(MovieStatus="Coming Soon")
    languages = request.GET.getlist('langua')
    genres = request.GET.getlist('genre')
    modes = request.GET.getlist('mode')
    filtered_movies = MovieDB.objects.filter(MovieStatus="Coming Soon")

    if languages:
        filtered_movies = filtered_movies.filter(MovieLanguage__in=languages)

        # for i in filtered_movies:
        #     print(i.MovieName)
    if genres:
        filtered_movies = filtered_movies.filter(MovieGenre__in=genres)
    if modes:
        filtered_movies = filtered_movies.filter(MovieType__in=modes)
    filtered_movies = filtered_movies.order_by('-MovieRelease')
    paginator = Paginator(filtered_movies, per_page=2)  # Display 5 items per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'ComingSoon.html', {'lang': lang, 'genr':genr,'types':types, 'movies':movies,
                                               'filtered_movies': filtered_movies , 'page':page})

def movie_details(request, movie_id):
    movie=MovieDB.objects.get(id=movie_id)
    mn=movie.MovieName
    review=ReviewDB.objects.filter(MovieName=mn)
    review_count=review.count()
    username = request.session.get("UserName")
    if username:
        user_details=UserDB.objects.get(UserName=username)
        return render(request, 'MovieDetails.html',{'movie':movie, 'review':review,
                                                    'review_count':review_count,'user_details':user_details})
    else:
        return render(request, 'MovieDetails.html', {'movie': movie, 'review': review,
                                                     'review_count': review_count})

def contactus(request):
    theatredet=TheatreDB.objects.get(id=1)
    return render(request, 'ContactUs.html',{'theatredet':theatredet})

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
            messages.success(request, "Registration done successfully..! Login Now..")
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
        im = request.POST.get('image')
        obj=ReviewDB(UserName=username, Review=review,Date=date,MovieName=moviename, UserImage=im)
        obj.save()
        messages.success(request, "Review Posted Successfully...!")
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
        messages.success(request, "Thank you for Contacting Us..")
        return redirect(contactus)

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
    unpaid_bookings = UserBookingDB.objects.filter(PaymentStatus="UnderProcess")
    print(unpaid_bookings)
    for booking in unpaid_bookings:
        # Parse the SeatNumberOnly field as a literal list
        seat_numbers_str = ast.literal_eval(booking.SeatNumberOnly)
        print(seat_numbers_str)
        # Ensure that seat_numbers_str is a list
        if isinstance(seat_numbers_str, list):
            # Iterate over individual seat numbers
            for seat_number in seat_numbers_str:
                # Strip extra spaces and remove single quotes
                seat_number = seat_number.strip().strip("'")
                print(seat_number)

                # Retrieve the corresponding seat from the SeatDB model
                seat = SeatDB.objects.get(SeatNumber=seat_number, Date=booking.SelectedDate)

                # Check if the seat status is "booked" before updating
                if seat.SeatStatus == "selected":
                    # Update the seat status to "available"
                    seat.SeatStatus = "available"
                    seat.save()
    ShowTimeNames = ShowTimeDB.objects.filter(MovieName=selected_movie, Date=selected_date).values_list('ShowTimeName', flat= True)
    if ShowTimeNames:
        if 'UserName' in request.session:
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
            messages.error(request,"Please login first")
            return redirect(login_signup)
    else:
        messages.error(request, "Movie still not scheduled")
        return redirect(index)
def submit_booking(request):
    if request.method == 'POST':
        na = request.POST.get('screenName')
        shn = request.POST.get('showName')
        sht = request.POST.get('showStartTime')
        mn = request.POST.get('movieName')
        un = request.POST.get('userName')
        fp = request.POST.get('finalPrice')
        dt= request.POST.get('selectedDate')
        seats=request.POST.get('chosenSeats')
        types=request.POST.get('chosenTypes')
        seatim=request.POST.get('seat_img')
        current_datetime = datetime.now()
        types_list = types.split(',')
        premium_count = types_list.count('Premium')
        standard_count = types_list.count('Standard')
        count_types=len(types)

        # print(na,shn,mn,fp,un)
        selected_seats_data = request.POST.getlist('seats')
        # print(selected_seats_data)
        selected_seats = [seat.split(':')[0] for seat in selected_seats_data if seat.split(':')[1] == 'selected']
        count=len(selected_seats)

        if seats:
            SeatDB.objects.filter(SeatNumber__in=selected_seats).update(SeatStatus='selected')
            obj = UserBookingDB(UserName=un, MovieName=mn, ScreenName=na, ShowName=shn, SelectedDate=dt,StartTime=sht,AmountToBePaid=fp,
                                NoOfSeats=count, SeatNumbers=seats,SeatNumberOnly=selected_seats, PaymentStatus="UnderProcess", BookedDate=current_datetime)
            obj.save()

            url = reverse('movie_checkout') + f'?screenName={na}&selectedSeat={selected_seats}&showName={shn}&showStartTime={sht}&movieName={mn}&userName={un}&finalPrice={fp}&selectedDate={dt}&chosenSeats={seats}&chosenTypes={types}&count={count}'
            return redirect(url)
        else:
            messages.error(request, "Select atleast one Seat")
            return redirect('index') #enter error message

def movie_checkout(request):
    screenName = request.GET.get('screenName')
    showName = request.GET.get('showName')
    showStartTime = request.GET.get('showStartTime')
    movieName = request.GET.get('movieName')
    moviedet=MovieDB.objects.filter(MovieName=movieName)
    movieLang=moviedet[0].MovieLanguage
    movieType=moviedet[0].MovieType
    userName = request.GET.get('userName')
    userdet=UserDB.objects.filter(UserName=userName)
    userEmail=userdet[0].UserEmail
    print(userEmail)
    userContact=userdet[0].UserContact
    finalPrice = request.GET.get('finalPrice')
    selectedDate = request.GET.get('selectedDate')
    chosenSeats = request.GET.get('chosenSeats')
    chosenTypes = request.GET.get('chosenTypes')
    count = request.GET.get('count')
    selectedSeat=request.GET.get('selectedSeat')

    # Render the "MovieCheckOut.html" template with the retrieved data
    return render(request, 'MovieCheckOut.html', {
        'screenName': screenName,
        'showName': showName,
        'showStartTime': showStartTime,
        'movieName': movieName,
        'movieLang': movieLang,
        'movieType': movieType,
        'userName': userName,
        'userEmail': userEmail,
        'userContact': userContact,
        'finalPrice': finalPrice,
        'selectedDate': selectedDate,
        'chosenSeats': chosenSeats,
        'chosenTypes': chosenTypes,
        'count': count,
        'selectedSeat':selectedSeat,

    })
def ticket_booking(request, data_id):
    if request.method == 'POST':
        movie=MovieDB.objects.filter(id=data_id)
        today = datetime.today()
        next_three_days = [today + timedelta(days=i) for i in range(0, 4)]
        movie_name = movie[0].MovieName
        # now_movie = ShowTimeDB.objects.all()
        return render(request, 'TicketBooking.html',{'next_three_days': next_three_days, 'movie_name': movie_name})
    else:
        return redirect('index')


def confirm_booking(request):
    if request.method == 'POST':
        mn= request.POST.get('movieName')
        na= request.POST.get('screenName')
        dt= request.POST.get('selectedDate')
        shn= request.POST.get('showName')
        typee= request.POST.get('selected_type')
        selected_seats_data= request.POST.getlist('selected_seats')
        selected_seats_data_type= request.POST.getlist('selected_seats_type')
        newmail=request.POST.get('cemail')
        newmob=request.POST.get('mobile')
        cname=request.POST.get('cardname')
        exmonth=request.POST.get('expmonth')
        card=request.POST.get('carddet')

        cvvno=request.POST.get('cvv')
        uname=request.POST.get('username')
        print(selected_seats_data)
        print(selected_seats_data_type)
        if selected_seats_data:
            selected_seats_list = ast.literal_eval(selected_seats_data[0])
            # print(selected_seats_list)
            SeatDB.objects.filter(SeatNumber__in=selected_seats_list).update(SeatStatus='booked')
            UserBookingDB.objects.filter(SeatNumbers__in=selected_seats_data_type).update(PaymentStatus='PaymentDone')
            obj=CheckOutDB(UserName=uname,Email=newmail,Contact=newmob,CardName=cname,Expiry=exmonth, Cvv=cvvno,CardDetail=card)
            obj.save()
            types_list = typee.split(',')
            premium_count = types_list.count('Premium')
            standard_count = types_list.count('Standard')
            showtime = ShowTimeDB.objects.get(MovieName=mn, Date=dt, ScreenName=na, ShowTimeName=shn)
            showtime.AvailablePremiumTickets -= premium_count
            showtime.AvailableStandardTickets -= standard_count
            showtime.save()
            if (showtime.TotalPremiumTickets==showtime.AvailablePremiumTickets) and (showtime.TotalStandardTickets == showtime.AvailableStandardTickets):
                showtime.status="Closed"
            messages.success(request,"Booked successfully")
            return redirect('index')
        else:
            messages.error(request,"Booking Failed")
            return redirect('index')
    return redirect('index')


def booking_history(request):
    username=request.session['UserName']
    print(username)
    bookings = UserBookingDB.objects.filter(Q(UserName=username) & Q(PaymentStatus="PaymentDone"))
    return render(request, 'BookingHistory.html', {'bookings':bookings})
def download_booking_pdf(request, booking_id):
    booking = get_object_or_404(UserBookingDB, id=booking_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="booking_{booking.id}.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 750, f"Booking ID: {booking.id}")
    p.drawString(100, 730, f"User Name: {booking.UserName}")
    p.drawString(100, 710, f"Movie Name: {booking.MovieName}")
    p.drawString(100, 690, f"Screen Name: {booking.ScreenName}")
    p.drawString(100, 670, f"Show Name: {booking.ShowName}")
    p.drawString(100, 650, f"Selected Date: {booking.SelectedDate.strftime('%Y-%m-%d')}")
    p.drawString(100, 630, f"Start Time: {booking.StartTime}")
    p.drawString(100, 610, f"No. of Seats: {booking.NoOfSeats}")
    p.drawString(100, 590, f"Seat Numbers: {booking.SeatNumbers}")
    p.drawString(100, 570, f"Amount Paid: ₹{booking.AmountToBePaid}")
    p.drawString(100, 550, f"Payment Status: {booking.PaymentStatus}")
    p.drawString(100, 530, f"Booked Date: {booking.BookedDate.strftime('%Y-%m-%d')}")
    p.showPage()
    p.save()
    return response

def update_profile(request, dataid):
    if request.method == "POST":
        fn = request.POST.get('inputFirstName')
        ln = request.POST.get('inputLastName')
        em = request.POST.get('inputEmailAddress')
        ph = request.POST.get('inputPhone')
        ad = request.POST.get('inputAddress')
        pw=request.POST.get('password')
        try:
            im = request.FILES['img']
            fs = FileSystemStorage()
            file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            file = UserDB.objects.get(id=dataid).UserImage
        current_ph = UserDB.objects.get(id=dataid).UserContact
        current_em = UserDB.objects.get(id=dataid).UserEmail

        if ph != current_ph and UserDB.objects.filter(id=dataid, UserContact=ph).exclude(id=dataid).exists():
            messages.error(request, "MobileNumber already exists ")
            return redirect('my_profile')
        elif em != current_em and UserDB.objects.filter(id=dataid, UserEmail=em).exclude(id=dataid).exists():
            messages.error(request, "Email already exists ")
            return redirect('my_profile')
        else:
            UserDB.objects.filter(id=dataid).update(UserFirstName=fn, UserLastName=ln,
                                                UserAddress=ad, UserContact=ph,UserEmail=em,UserPassword=pw,UserImage=file)
            messages.success(request, "Profile  updated successfully")
            return redirect('my_profile')
    return redirect('my_profile')

