from django.shortcuts import render, redirect
from admin_pannel.models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
import random, uuid,json
import requests
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *
from num2words import num2words

def amount_to_words(amount):
    return num2words(amount, lang='en')


def new(request):
    types=package_Type.objects.all()
    user_package_details = package_details.objects.filter(
        package_type=types,
        package_details_status=True
    )
    context={"types":types,"user_package_details":user_package_details}
    return render(request,"new.html",context)


# views.py

def create_ticket(request, package_id):
    profile = request.session.get('user')

    if profile:
        try:
            user = Register.objects.get(id=profile)
        except Register.DoesNotExist:
            return redirect("login_userpannel")

    package_detail = package_details.objects.get(id=package_id)
    tickets = Ticket.objects.filter(user=user)
    user_contactus = contact_us.objects.filter(contact_status=True)
    if request.method == 'POST':
        # Process the main information
        first_name_main = request.POST.get('first_name', '')
        last_name_main = request.POST.get('last_name', '')
        age_main = request.POST.get('age', '')
        gender_main = request.POST.get('gender', '')

        # Save the main information to the database
        package_detail.first_name_main = first_name_main
        package_detail.last_name_main = last_name_main
        package_detail.age_main = age_main
        package_detail.gender_main = gender_main
        package_detail.save()

        # Process each dynamically generated ticket
        ticket_data_list = []
        num_tickets = int(request.POST['ticket'])
        for i in range(1, num_tickets + 1):
            first_name = request.POST.get('firstname_' + str(i))
            last_name = request.POST.get('lastname_' + str(i))
            age = request.POST.get('age_' + str(i))
            gender = request.POST.get('gender_' + str(i))

            # Create a dictionary for each set of details
            ticket_data = {
                'num_tickets':num_tickets,
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'gender': gender,
            }
            ticket_data_list.append(ticket_data)
        total_amount = package_detail.cost * num_tickets
        amount_in_words = amount_to_words(total_amount).title()


        # Display the summary page with the entered data
        return render(request, 'userpannel_summary.html', {"user_contactus":user_contactus,"num_tickets":num_tickets,"total_amount":total_amount,"amount_in_words":amount_in_words, 'package_detail': package_detail, 'tickets': ticket_data_list, 'user': user})

    context = {
        "package_detail": package_detail,
        "tickets": tickets,
        "user": user,
    }

    return render(request, 'userpannel_summary.html', context)




def booking(request, package_id):
    profile=request.session.get('user')
    if profile is not None:
        try:
            user=Register.objects.get(id=profile)
        except User.DoesNotExist:
           
            return redirect("login_userpannel")
        
    if request.method == 'POST':
        # Process booking logic
       
        booking_date = request.POST['booking-date']
        

        # Save booking information to the database
        # (Assuming you have a TourBooking model)
        booking = TourBooking(
            
            booking_date=booking_date,
           
        )
        booking.save()

        # Redirect after successful form submission
        return redirect('userpannel_payment', package_id=package_id)

    # Retrieve package details based on package_id
    package_detail = package_details.objects.get(id=package_id)
    user_contactus = contact_us.objects.filter(contact_status=True)

    context = {
        "package_detail": package_detail,
        "user":user,
        "user_contactus":user_contactus
        
    }

    return render(request, 'userpannel_payment.html', context)


def userpannel_payment(request,package_id):
    profile=request.session.get('user')
    if profile is not None:
        try:
            user=Register.objects.get(id=profile)
        except User.DoesNotExist:
           
            return redirect("login_userpannel")
        

    types=package_Type.objects.all()
    package_detail = package_details.objects.get(id=package_id)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    user_package_details = package_details.objects.filter(package_details_status=True)
    tickets=Ticket.objects.all()
    user_contactus = contact_us.objects.filter(contact_status=True)
    context={
        "package_detail":package_detail,
        "user_package_details":user_package_details,
        "all_hotels":all_hotels,
        "tickets":tickets,
        "types":types,
        'user_contactus':user_contactus,
        "user":user
    }
    return render(request, 'userpannel_payment.html',context)

    

def userpannel_summary(request, package_id):
    profile = request.session.get('user')
    
    if profile is not None:
        try:
            user = Register.objects.get(id=profile)
        except User.DoesNotExist:
            return redirect("login_userpannel")
    
    types = package_Type.objects.all()
    
    # Adjust the query based on your actual model structure
    package_detail = package_details.objects.select_related('hotel_name').get(id=package_id)
    
    user_package_details = package_details.objects.filter(package_details_status=True)
    
    # Modify the query to get only the tickets associated with the current package
    tickets = Ticket.objects.filter(user=user)
    about = about_us.objects.all()
    user_contactus = contact_us.objects.filter(contact_status=True)
    amount = 12345
    amount_in_words = amount_to_words(amount)

    context = {
        'user_package_details': user_package_details,
        'package_detail': package_detail,
        'user_contactus': user_contactus,
        'about': about,
        'types': types,
        'tickets': tickets,
        'user': user
    }

    return render(request, 'userpannel_summary.html', context)

# @login_required(login_url='login')
def userpannel_allpackage(request):
    all_countries = country.objects.filter(country_status=True)
    all_cities = city.objects.filter(city_status=True)
    all_package_types = package_Type.objects.filter(package_status=True)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    all_tour_places = tourplace.objects.filter(tour_status=True)
    about=about_us.objects.all()
    user_contactus = contact_us.objects.filter(contact_status=True)
    types=package_Type.objects.all()
    # selected_package_type = package_Type.objects.get(id=id)  package_type=selected_package_type,

    user_package_details = package_details.objects.filter(

        package_details_status=True
    )

    context = {
        'user_package_details': user_package_details,
        "all_countries": all_countries,
        "all_cities": all_cities,
        "all_package_types": all_package_types,
        "all_hotels":all_hotels,
        "vehicle_types":vehicle_types,
        "all_tour_places":all_tour_places,
        "about":about,"user_contactus":user_contactus,
        "types":types
        
    }

    return render(request, 'userpannel_all_packages.html', context)




def userpannel_packagetypes(request,pk):
    all_countries = country.objects.filter(country_status=True)
    all_states = state.objects.filter(state_status=True)
    all_cities = city.objects.filter(city_status=True)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    all_package_types = package_Type.objects.filter(package_status=True)
    about=about_us.objects.all()
    types=package_Type.objects.all()
    selected_package_type = package_Type.objects.get(id=pk)
    user_contactus = contact_us.objects.filter(contact_status=True)
   
    user_package_details = package_details.objects.filter(
        package_type=selected_package_type,
        package_details_status=True
    )
    context={
        # 'user_package_type':user_package_type,
        "user_package_details":user_package_details,
        "about":about,"user_contactus":user_contactus,
        "types":types,
        "all_countries":all_countries,
        "all_cities":all_cities,
        "all_hotels":all_hotels,
        "vehicle_types":vehicle_types,
        "all_package_types":all_package_types,
        "all_states":all_states

    }

    return render(request,'userpannel_packagetype.html',context) 


def userpannel_hotels(request):
    types=package_Type.objects.all()
    user_hotels = add_hotel.objects.filter(hotel_status=True)
    user_package_details = package_details.objects.filter(

        package_details_status=True
    )
    about=about_us.objects.all()
    user_contactus = contact_us.objects.filter(contact_status=True)
    context = {'user_hotels': user_hotels, "user_package_details": user_package_details,"about":about,"user_contactus":user_contactus,"types":types}
    return render(request, 'userpannel_hotel.html', context)

# @login_required(login_url='login_userpannel')
def hoteldetails(request, id):
    profile = request.session.get('user')
    
    if profile is not None:
        try:
            user = Register.objects.get(id=profile)
        except Register.DoesNotExist:
            return redirect("login_userpannel")
    else:
        # Redirect to login page if the user is not authenticated
        return redirect("login_userpannel")
    types = package_Type.objects.all()

    user_package_details = package_details.objects.select_related('hotel_name').get(
        hotel_name_id=id,
        package_details_status=True
    )
    about = about_us.objects.all()

    user_contactus = contact_us.objects.filter(contact_status=True)
    context = {
        "user_package_details": user_package_details,
        "user_contactus": user_contactus,
        "about": about,
        "types": types,
        "user": user
    }
    return render(request, "userpannel_hoteldetails.html", context)



def userpannel_bestpackages(request):
    types=package_Type.objects.all()
    all_countries = country.objects.filter(country_status=True)
    all_cities = city.objects.filter(city_status=True)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    all_package_types = package_Type.objects.filter(package_status=True)
    user_package_details = package_details.objects.filter(
        package_details_status=True
    )
    user_package_details = package_details.objects.order_by('-cost')
    about=about_us.objects.all()
    user_contactus = contact_us.objects.filter(contact_status=True)
    context = {
        'user_package_details': user_package_details,
        "all_countries": all_countries,
        "all_cities": all_cities,
        "all_package_types": all_package_types,
        "about":about,
        "all_hotels":all_hotels,
        "vehicle_types":vehicle_types,
        "user_contactus":user_contactus,
        "types":types
    }

    return render(request, 'userpannel_bestpackages.html', context)


def userpannel_contactus(request):
    types=package_Type.objects.all()
    user_contactus = contact_us.objects.filter(contact_status=True)
    user_package_details = package_details.objects.filter(package_details_status=True)

    if request.method == 'POST':
        name=request.POST.get("name")
        subject = request.POST.get('subject')
        desc = request.POST.get('message')
        email = request.POST.get('email')

        contactus = contact(
            name=name,
            subject=subject,
            message=desc,
            email=email,
            
        )
        contactus.save()
        return redirect('userpannel_contactus')
    contacts = contact.objects.all()

    context = {
        'user_contactus': user_contactus,
        'contacts': contacts,
        "user_package_details":user_package_details,
        "types":types
    }
    return render(request, 'userpannel_contactus.html', context)


def tourdetails(request,id):
    
    tour_detials=tour_detail.objects.get(id=id)
    types=package_Type.objects.all()
    
    # user_package_details = package_details.objects.select_related('hotel_name').get(
    #     hotel_name_id=id,
    #     package_details_status=True
    # )
    # userpannel_hotel_detials=add_hotel.objects.get(id=id)
    about=about_us.objects.all()
    
    user_contactus = contact_us.objects.filter(contact_status=True)
    context = {
               "user_contactus":user_contactus,"about":about,"types":types,"tour_detials":tour_detials}
    return render(request,"userpannel_tour_details.html",context)
from itertools import zip_longest
# @login_required(login_url='login_userpannel')
def userpannel_moredetail(request, package_id):
    profile = request.session.get('user')

    if profile is not None:
        try:
            user = Register.objects.get(id=profile)
        except Register.DoesNotExist:
            return redirect("login_userpannel")
    else:
        print("User not authenticated")  # Add this line for debugging
        return redirect("login_userpannel")
    tour_detials=tour_detail.objects.filter(tourcity_id=package_id)
    tour_detials_it=tour_detail.objects.filter(tourname_id =package_id)

    user_contactus = contact_us.objects.filter(contact_status=True)
    user_package_details = package_details.objects.select_related('guide_name','hotel_name').get(
        id=package_id,
        package_details_status=True
    )
    tour_cat=tourplace.objects.all()
    about=about_us.objects.all()
    itinerary_items = user_package_details.iternary.split('\n')
    num_days = int(user_package_details.duration)

    # Generate a range of days and zip it with the itinerary items
    days_and_itinerary = zip_longest(range(1, num_days + 1), itinerary_items, fillvalue='')
    user_contactus = contact_us.objects.all()
    types=package_Type.objects.all()
    context = {
        'user_package_details': user_package_details,
        "user_contactus":user_contactus,
         "about":about,
         "types":types,
         "tour_detials":tour_detials,
         "user":user,
         "tour_cat":tour_cat,
         "itinerary_items":itinerary_items,
         "days_and_itinerary":days_and_itinerary,
         "tour_detials_it":tour_detials_it

    }

    return render(request, 'userpannel_moredetails.html', context)


def search_results(request):
    all_countries = country.objects.filter(country_status=True)
    all_cities = city.objects.filter(city_status=True)
    all_package_types = package_Type.objects.filter(package_status=True)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    user_package_details = package_details.objects.filter(
    
        package_details_status=True
    )
    user_contactus = contact_us.objects.filter(contact_status=True)
    about=about_us.objects.all()
    types=package_Type.objects.all()
    if request.method == 'GET':
        country_id = request.GET.get('standard', '')
        city_id = request.GET.get('standard3', '')
        package_type_id = request.GET.get('standard4', '')
        hotel_name_id = request.GET.get('standard2', '')
        
        # Filter the queryset based on the search parameters
        queryset = package_details.objects.filter(package_details_status=True)  # Replace with the actual model name

        if country_id:
            queryset = queryset.filter(country_name_id=country_id)

        if city_id:
            queryset = queryset.filter(city_name_id=city_id)

        if package_type_id:
            queryset = queryset.filter(package_type_id=package_type_id)

        if hotel_name_id:
            queryset = queryset.filter(hotel_name_id=hotel_name_id)
        context = {
            'results': queryset,
            'selected_country': country_id,
            'selected_city': city_id,
            'selected_package_type': package_type_id,
            "all_countries": all_countries,
            "all_cities": all_cities,
            "all_package_types": all_package_types,
            "all_hotels":all_hotels,
            "user_package_details": user_package_details,
            "about":about,
            "vehicle_types":vehicle_types,
            "user_contactus":user_contactus,
            "types":types

        }

        return render(request, 'search_results.html', context)
    else:
        return render(request, 'search_results.html', {})

def tour_search_results(request):
    all_countries = country.objects.filter(country_status=True)
    all_cities = city.objects.filter(city_status=True)
    all_package_types = package_Type.objects.filter(package_status=True)
    all_tour_places = tourplace.objects.filter(tour_status=True)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    user_package_details = package_details.objects.filter(

        package_details_status=True
    )
    user_contactus = contact_us.objects.filter(contact_status=True)
    about=about_us.objects.all()
    types=package_Type.objects.all()
    if request.method == 'GET':
        country_id = request.GET.get('standard', '')
        city_id = request.GET.get('standard3', '')
        package_type_id = request.GET.get('standard4', '')
        tour_places_id = request.GET.get('standard2', '')
        
        # Filter the queryset based on the search parameters
        queryset = package_details.objects.filter(package_details_status=True)  # Replace with the actual model name

        if country_id:
            queryset = queryset.filter(country_name_id=country_id)

        if city_id:
            queryset = queryset.filter(city_name_id=city_id)

        if package_type_id:
            queryset = queryset.filter(package_type_id=package_type_id)

        if tour_places_id:
            queryset = queryset.filter(tour_places=tour_places_id)
        context = {
            'results': queryset,
            'selected_country': country_id,
            'selected_city': city_id,
            'selected_package_type': package_type_id,
            "all_countries": all_countries,
            "all_cities": all_cities,
            "all_hotels":all_hotels,
            "vehicle_types":vehicle_types,
            "all_package_types": all_package_types,
            "all_tour_places":all_tour_places,
            "user_package_details": user_package_details,
            "about":about,
            "user_contactus":user_contactus,
            "types":types

        }

        return render(request, 'tour_search_results.html', context)
    else:
        return render(request, 'tour_search_results.html', {})
    
def vehicles_search_results(request):
    all_countries = country.objects.filter(country_status=True)
    all_cities = city.objects.filter(city_status=True)
    all_package_types = package_Type.objects.filter(package_status=True)
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    user_package_details = package_details.objects.filter(

        package_details_status=True
    )
    user_contactus = contact_us.objects.filter(contact_status=True)
    types=package_Type.objects.all()
    about=about_us.objects.all()
    if request.method == 'GET':
        country_id = request.GET.get('standard', '')
        city_id = request.GET.get('standard3', '')
        package_type_id = request.GET.get('standard4', '')
        type_of_vehicle_id = request.GET.get('standard2', '')
        
        # Filter the queryset based on the search parameters
        queryset = package_details.objects.filter(package_details_status=True)  # Replace with the actual model name

        if country_id:
            queryset = queryset.filter(country_name_id=country_id)

        if city_id:
            queryset = queryset.filter(city_name_id=city_id)

        if package_type_id:
            queryset = queryset.filter(package_type_id=package_type_id)

        if type_of_vehicle_id:
            queryset = queryset.filter(type_of_vehicle_id=type_of_vehicle_id)
        context = {
            'results': queryset,
            'selected_country': country_id,
            'selected_city': city_id,
            'selected_package_type': package_type_id,
            "all_countries": all_countries,
            "all_cities": all_cities,
            "all_hotels":all_hotels,
            "all_package_types": all_package_types,
            "vehicle_types":vehicle_types,
            "user_package_details": user_package_details,
            "about":about,
            "user_contactus":user_contactus,
            "types":types

        }

        return render(request, 'vehicles_search_results.html', context)
    else:
        return render(request, 'vehicles_search_results.html', {})


# views.py

def packageduration(request, selected_duration):
    all_countries = country.objects.filter(country_status=True)
    all_cities = city.objects.filter(city_status=True)
    all_package_types = package_Type.objects.filter(package_status=True)
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    about=about_us.objects.all()
    user_package_details = package_details.objects.filter(

        package_details_status=True
    )
    user_contactus = contact_us.objects.filter(contact_status=True)
    types=package_Type.objects.all()
    try:
        # Convert the selected_duration to an integer
        duration = int(selected_duration)

        # Determine the appropriate duration category
        if duration < 7:
            selected_duration = '7'
        elif 7 <= duration <= 14:
            selected_duration = '14'
        elif 15 <= duration <= 21:
            selected_duration = '21'
        elif 22 <= duration <= 30:
            selected_duration = '30'
        else:
            raise ValueError("Invalid duration")

        # Fetch package details based on the selected duration
        packagedetails = package_details.objects.filter(duration__lte=duration)
        
        # Prepare the context for rendering the template
        context = {
            'packagedetails': packagedetails,
            'selected_duration': selected_duration,
            "about":about,
            "all_countries": all_countries,
            "all_cities": all_cities,
            "all_package_types": all_package_types,
            "vehicle_types":vehicle_types,
            "all_hotels":all_hotels,
            "user_package_details":user_package_details,
            "user_contactus":user_contactus,
            "types":types
        }

        # Render the template with the context
        return render(request, 'packageduration.html', context)

    except ValueError as e:
        # Handle the case where selected_duration is not a valid integer
        return render(request, 'error.html', {'error_message': str(e)})
    
def send_otp(phone_number, otp):
    api_key = '70d10669-9d83-11ee-8cbb-0200cd936042'
    url = f'https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}'
    response = requests.post(url)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['Status'] == 'Success':
            session_id = response_data['Details']
            return session_id
        return None

def login(request):
    user_contactus = contact_us.objects.filter(contact_status=True)
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username', username, ':', 'password', password)

        try:
            user = Register.objects.get(username=username, password=password)
            if user.password == password:
                request.session['user'] = user.id
                print(request.session['user'])
                return redirect('userpannel_allpackages')
            else:
                error_message = 'Username or Password invalid !!'
                print('Username or Password invalid !!!')
        except Register.DoesNotExist:
            error_message = 'Username or Password invalid !!'
            print('Username or Password invalid !!!')

    return render(request, 'userpannel_login.html', {'error': error_message,'user_contactus':user_contactus})


def validateuser(student_user):
    error_message = None
    if student_user.isExistsemail():
        error_message = 'Phone Number Already Registered..'
    elif student_user.isExistsphone():
        error_message = 'Phone Number Already Registered..'
    # saving
    return error_message

def register(request):
    user_contactus = contact_us.objects.filter(contact_status=True)
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        username = request.POST.get('username')
        phoneNo = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(full_name)

        existing_user = Register.objects.filter(username=username).first()

        if existing_user:
            error_message = f"User details already exists."
            return render(request, 'userpannel_register.html', {'error': error_message})
        # validation
        value = {
            'username': username,
            'phoneNo': phoneNo,
            'email': email,
        }
        error_message = None
        if password == confirm_password:
            error_message = "Password and Confirm Password Must be Same"
        userotp = random.randint(111111, 999999)
        user = Register(fullname=full_name,
                        username=username,
                        mobile=phoneNo,
                        email=email,
                        password=password,
                        otp=userotp,
                              )
        error_message = validateuser(user)
        print(error_message)
        if not error_message:
            user.save()
            send_otp(user.mobile, user.otp)
            form_url = reverse('otp', args=[user.id])
            return redirect(form_url)
        else:
            data = {
                'error': error_message,
                'values': value
            }
        return render(request, 'userpannel_register.html',data)
    else:
        return render(request, 'userpannel_register.html',{'user_contactus':user_contactus})

def otp_verification(request,pk):
    user = Register.objects.get(id=pk)
    if request.method == 'POST':
        otp = request.POST.get('number')
        if int(otp) == int(user.otp):
            return redirect('login_userpannel')
        else:
            return redirect('login_userpannel')
    last_three_numbers = user.mobile[-3:]
    print(last_three_numbers)
    context = {
        'user': user,
        'last_three_numbers':last_three_numbers,
    }
    return render(request, 'otp_verification.html', context)

def logout_userpannel(request):
    # Use Django's logout function to clear the user's session
    logout(request)
    return redirect('userpannel_allpackages')