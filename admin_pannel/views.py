from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count


# Create your views here.

def settings(request):
    coun_count = country.objects.filter(country_status=True).count()
    package_Type_count=package_Type.objects.filter(package_status=True).count()
    hoteldetails_count=add_hotel.objects.filter(hotel_status=True).count()
    tour_details=tour_detail.objects.filter(tourstatus=True).count()
    profiles = UserProfile.objects.all()
    return render(request, 'settings.html',{"profiles":profiles,"coun_count":coun_count,"package_Type_count":package_Type_count,
        "hoteldetails_count":hoteldetails_count, "tour_details":tour_details})
def base(request):
    profiles = UserProfile.objects.all()

    # Assuming you want to display the details of the first contact (if it exists)

    context={
        "profiles":profiles,
    }
    return render(request,"base.html",context)

def mode_of_transport(request):
    profiles = UserProfile.objects.all()
    vehicletype_count = add_vehicle_type.objects.filter(mode_status=True).count()
    vehiclename_count = add_vehicle_name.objects.filter(mode_status=True).count()
    vehicldetails_count = add_vehicle_details.objects.filter(vehicle_details_status=True).count()
    context={"profiles":profiles,
             "vehicletype_count":vehicletype_count,
             "vehiclename_count":vehiclename_count,
             "vehicldetails_count":vehicldetails_count
             }
    return render(request, 'mode_of_transport.html',context)


# @login_required(login_url='login')
def dashboard(request):
    profiles = UserProfile.objects.all()
    return render(request, 'dashboard.html',{"profiles":profiles})


def hoteldetails(request):
    profiles = UserProfile.objects.all()
    hoteldetails_count=add_hotel.objects.filter(hotel_status=True).count()
    return render(request, 'hotel_details.html',{"profiles":profiles,"hoteldetails_count":hoteldetails_count})


def navigation(request):
    coun_count = country.objects.filter(country_status=True).count()
    city_count = city.objects.filter(city_status=True).count()
    state_count = state.objects.filter(state_status=True).count()
    tour_count = tourplace.objects.filter(tour_status=True).count()
    package_Type_count=package_Type.objects.filter(package_status=True).count()
    hoteldetails_count=add_hotel.objects.filter(hotel_status=True).count()
    profiles = UserProfile.objects.all()
    context={
        "profiles":profiles,
        "coun_count":coun_count,
        "city_count":city_count,
        "state_count":state_count,
        "tour_count":tour_count,
        "package_Type_count":package_Type_count,
        "hoteldetails_count":hoteldetails_count
        }
    return render(request, 'navigationlocation.html',context)

def addguide(request):
    profiles = UserProfile.objects.all()
    guidedetails_count=add_guide.objects.filter(guide_status=True).count()
    return render(request, 'add_guide.html', {"profiles": profiles,"guidedetails_count":guidedetails_count})


def addtourpackage(request):
    profiles = UserProfile.objects.all()
    package_details_count=package_details.objects.filter(package_details_status=True).count()
    return render(request, 'add_tour_package.html', {"profiles": profiles,"package_details_count":package_details_count})


def managebooking(request):
    profiles = UserProfile.objects.all()
    return render(request, "manage_booking.html", {"profiles": profiles})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            auth.login(request, user)
            print('Login is Successful...!')
            return redirect('dashboard')
        else:
            print("Invalid Details")
            return redirect('login_adminpannel')
    else:
        return render(request, 'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        print("Logout Successfull from website...")
        return redirect('login')


def create_countries(request):
    error_message_countryname = ""
    error_message_shortcode = ""
    profiles = UserProfile.objects.all()
    if request.method == 'POST':
        countryimage = request.FILES.get('co_image')
        countryname = request.POST.get('country_name')
        shortcode = request.POST.get('shortcode')
        countrydescription = request.POST.get('countrydescription')

        if country.objects.filter(country_name=countryname).exists():
            error_message_countryname = "Country Name already exists."
        if country.objects.filter(country_short_code=shortcode).exists():
            error_message_shortcode = "Country short code already exists."

        if not error_message_countryname and not error_message_shortcode:
            data = country(
                country_image=countryimage,
                country_name=countryname,
                country_short_code=shortcode,
                country_description=countrydescription
            )
            data.save()
        else:
            # If there are errors, retrieve the existing data and render the page
            display = country.objects.all()

            context = {
                "display": display,
                "error_message_countryname": error_message_countryname,
                "error_message_shortcode": error_message_shortcode,
                "profiles": profiles
            }
            return render(request, 'create_countries.html', context)

    display = country.objects.all()

    context = {
        "display": display,
        "error_message_countryname": error_message_countryname,
        "error_message_shortcode": error_message_shortcode,
        "profiles": profiles

    }
    return render(request, 'create_countries.html', context)


def count(request):
    coun_count = country.objects.filter(country_status=True).count()
    city_count = city.objects.count()
    context = {
        "coun_count": coun_count,
        "city_count": city_count
    }
    return render(request, 'navigationlocation.html', context)


def edit_countries(request):
    display = country.objects.all()

    context = {"display": display}

    return redirect(request, "create_countries.html", context)


def update_countries(request, id):
    if request.method == 'POST':
        e_countryimage = request.FILES.get('edit_image')
        e_countryname = request.POST.get('edit_name')
        e_shortcode = request.POST.get('edit_shortcode')
        e_countrydescription = request.POST.get('edit_description')

        display = country(
            id=id,
            country_image=e_countryimage,
            country_name=e_countryname,
            country_short_code=e_shortcode,
            country_description=e_countrydescription
        )
        display.save()
        return redirect('create_countries')

    return render(request, 'create_countries.html')


def delete_countries(request, pk):
    # Assuming your model is named 'Country'
    dele = country.objects.filter(id=pk)

    if dele.exists():
        dele.delete()
        messages.success(request, 'Record deleted successfully.')
    else:
        messages.error(request, 'Error deleting record.')

    return redirect('create_countries')


def deactivecountry(request, id):
    display = country.objects.get(id=id)
    display.country_status = False
    display.save()
    return redirect('create_countries')


def activecountry(request, id):
    display = country.objects.get(id=id)
    display.country_status = True
    display.save()
    return redirect('create_countries')


def create_states(request):
    profiles = UserProfile.objects.all()
    country_cat = country.objects.filter(country_status=True)
    error_message_countryname = ""
    error_message_shortcode = ""

    if request.method == 'POST':
        cou_name = request.POST.get('countryname')
        stateimage = request.FILES.get('co_image')
        statename = request.POST.get('country_name')
        shortcode = request.POST.get('shortcode')
        statedescription = request.POST.get('countrydescription')

        if state.objects.filter(state_name=statename).exists():
            error_message_countryname = "State Name already exists."
        if state.objects.filter(state_short_code=shortcode).exists():
            error_message_shortcode = "Country short code already exists."

        if not error_message_countryname and not error_message_shortcode:
            data = state(
                state_country_id=cou_name,
                state_image=stateimage,
                state_name=statename,
                state_short_code=shortcode,
                state_description=statedescription
            )
            data.save()
        else:
            # If there are errors, retrieve the existing data and render the page
            display = state.objects.all()

            context = {
                "display": display,
                "country_cat": country_cat,
                "error_message_countryname": error_message_countryname,
                "error_message_shortcode": error_message_shortcode,
                "profiles": profiles
            }
            return render(request, 'create_state.html', context)

    display = state.objects.all()

    context = {
        "display": display,
        "country_cat": country_cat,
        "error_message_countryname": error_message_countryname,
        "error_message_shortcode": error_message_shortcode,
        "profiles": profiles

    }
    return render(request, 'create_state.html', context)


def count_admin(request):
    coun_count = country.objects.Count()
    city_count = city.objects.Count()
    context = {
        "coun_count": coun_count,
        "city_count": city_count
    }
    return render(request, 'navigationlocation.html', context)


def edit_states(request):
    display = state.objects.all()

    context = {"display": display}

    return redirect(request, "create_state.html", context)


def update_states(request, id):
    if request.method == 'POST':
        cou_name = request.POST.get('countryname')
        e_stateimage = request.FILES.get('edit_image')
        e_statename = request.POST.get('edit_name')
        e_shortcode = request.POST.get('edit_shortcode')
        e_statedescription = request.POST.get('edit_description')

        display = state(
            id=id,
            state_country_id=cou_name,
            state_image=e_stateimage,
            state_name=e_statename,
            state_short_code=e_shortcode,
            state_description=e_statedescription
        )
        display.save()
        return redirect('create_states')

    return render(request, 'create_state.html')


def delete_states(request, pk):
    # Assuming your model is named 'Country'
    dele = state.objects.filter(id=pk)

    if dele.exists():
        dele.delete()
        messages.success(request, 'Record deleted successfully.')
    else:
        messages.error(request, 'Error deleting record.')

    return redirect('create_states')


def deactivestate(request, id):
    display = state.objects.get(id=id)
    display.state_status = False
    display.save()
    return redirect('create_states')


def activestate(request, id):
    display = state.objects.get(id=id)
    display.state_status = True
    display.save()
    return redirect('create_states')


def create_cities(request):
    profiles = UserProfile.objects.all()
    country_cat = country.objects.filter(country_status=True)
    state_cat = state.objects.filter(state_status=True)
    error_message_cityname = ""
    error_message_cityshortcode = ""

    if request.method == 'POST':
        cou_name = request.POST.get('countryname')
        state_name = request.POST.get("statename")
        cityname = request.POST.get('c_name')
        cityshortcode = request.POST.get('c_shortcode')
        cityimage = request.FILES.get('c_image')
        citydescription = request.POST.get('c_description')

        if city.objects.filter(city_name=cityname).exists():
            error_message_cityname = "City Name already exists."
        if city.objects.filter(city_short_code=cityshortcode).exists():
            error_message_cityshortcode = "City short code already exists."

        if not error_message_cityname and not error_message_cityshortcode:
            data = city(
                city_country_id=cou_name,
                city_state_id=state_name,
                city_name=cityname,
                city_short_code=cityshortcode,
                city_image=cityimage,
                city_description=citydescription
            )
            data.save()
        else:
            # If there are errors, retrieve the existing data and render the page
            display_city = city.objects.all()
            context = {
                'display_city': display_city,
                'country_cat': country_cat,
                "state_cat": state_cat,
                'error_message_cityname': error_message_cityname,
                'error_message_cityshortcode': error_message_cityshortcode,
                "profiles": profiles
            }
            return render(request, 'create_cities.html', context)

    display_city = city.objects.all()
    context = {
        'display_city': display_city,
        'country_cat': country_cat,
        "state_cat": state_cat,
        'error_message_cityname': error_message_cityname,
        'error_message_cityshortcode': error_message_cityshortcode,
        "profiles": profiles
    }
    return render(request, 'create_cities.html', context)


def edit_cities(request):
    display_city = city.objects.all()

    context = {"display_city": display_city}

    return redirect(request, "create_cities.html", context)


def update_cities(request, id):
    if request.method == 'POST':
        e_cityimage = request.FILES.get('edit_image')
        cou_name = request.POST.get('countryname')
        state_name = request.POST.get("statename")
        e_cityname = request.POST.get('edit_name')
        e_cityshortcode = request.POST.get('edit_shortcode')
        e_citydescription = request.POST.get('edit_description')

        display_city = city(
            id=id,
            city_country_id=cou_name,
            city_state_id=state_name,
            city_image=e_cityimage,
            city_name=e_cityname,
            city_short_code=e_cityshortcode,
            city_description=e_citydescription,

        )
        display_city.save()
        return redirect('create_cities')

    return render(request, 'create_cities.html')


def delete_cities(requset, pk):
    display_city = city.objects.filter(id=pk)
    display_city.delete()
    return redirect('create_cities')


def deactivate_city(request, id):
    display_city = city.objects.get(id=id)
    display_city.city_status = False
    display_city.save()
    return redirect('create_cities')


def activate_city(request, id):
    display_city = city.objects.get(id=id)
    display_city.city_status = True
    display_city.save()
    return redirect('create_cities')


def create_tour(request):
    profiles = UserProfile.objects.all()
    country_cat = country.objects.filter(country_status=True)
    city_cat = city.objects.filter(city_status=True)
    state_cat = state.objects.filter(state_status=True)
    error_message_tourname = ""

    if request.method == "POST":
        cou_name = request.POST.get('countryname')
        state_name = request.POST.get("statename")
        cityname = request.POST.get('city_name')
        tourname = request.POST.get('t_name')
        tourshortcode = request.POST.get('t_shortcode')
        tourimage = request.FILES.get('t_image')
        tourdescription = request.POST.get('t_description')

        if tourplace.objects.filter(tour_name=tourname).exists():
            error_message_tourname = "Tour Name already exists."

        if not error_message_tourname:
            data = tourplace(
                tour_country_id=cou_name, tour_state_id=state_name, tour_city_id=cityname, tour_name=tourname,
                tour_short_code=tourshortcode, tour_image=tourimage, tour_description=tourdescription
            )
            data.save()
        else:
            # If there are errors, retrieve the existing data and render the page
            display_tour = tourplace.objects.all()

            context = {
                "display_tour": display_tour,
                "country_cat": country_cat,
                "city_cat": city_cat,
                "state_cat": state_cat,
                "error_message_tourname": error_message_tourname,
                "profiles": profiles
            }
            return render(request, "create_tour.html", context)

    display_tour = tourplace.objects.all()
    context = {
        "display_tour": display_tour,
        "country_cat": country_cat,
        "city_cat": city_cat,
        "state_cat": state_cat,
        "error_message_tourname": error_message_tourname,
        "profiles": profiles
    }
    return render(request, "create_tour.html", context)


def edit_tour(request):
    display_tour = tourplace.objects.all()

    context = {"display_tour": display_tour}

    return redirect(request, "create_tour.html", context)


def update_tour(request, id):
    if request.method == 'POST':
        cou_name = request.POST.get('countryname')
        state_name = request.POST.get("statename")
        cityname = request.POST.get('city_name')
        e_tourimage = request.FILES.get('edit_image')
        e_tourname = request.POST.get('edit_name')
        e_tourshortcode = request.POST.get('edit_shortcode')
        e_tourdescription = request.POST.get('edit_description')

        display_tour = tourplace(
            id=id,
            tour_country_id=cou_name,
            tour_state_id=state_name,
            tour_city_id=cityname,
            tour_image=e_tourimage,
            tour_name=e_tourname,
            tour_short_code=e_tourshortcode,
            tour_description=e_tourdescription,
        )
        display_tour.save()
        return redirect('create_tour')

    return render(request, 'create_tour.html')

   
def delete_tour(requset, pk):
    display_tour = tourplace.objects.filter(id=pk)
    display_tour.delete()
    return redirect('create_tour')


def deactivate_tour(request, id):
    display_tour = tourplace.objects.get(id=id)
    display_tour.tour_status = False
    display_tour.save()
    return redirect('create_tour')


def activate_tour(request, id):
    display_tour = tourplace.objects.get(id=id)
    display_tour.tour_status = True
    display_tour.save()
    return redirect('create_tour')

def tour_Details(request):
    profiles = UserProfile.objects.all()
    country_cat = country.objects.filter(country_status=True)
    city_cat = city.objects.filter(city_status=True)
    state_cat=state.objects.filter(state_status=True)
    tour_cat=tourplace.objects.filter(tour_status=True)
    hotel_cat=add_hotel.objects.filter(hotel_status=True)
    vehicle_cat=add_vehicle_type.objects.filter(mode_status=True)


    if request.method == "POST":
        cou_name = request.POST.get('countryname')
        state_name=request.POST.get("statename")
        hotel_name=request.POST.get("hotelname")
        vehicle_name=request.POST.get("vehiclename")
        cityname = request.POST.get('city_name')
        tourname = request.POST.get('t_name')
        tourshortcode = request.POST.get('t_shortcode')
        tourimage1 = request.FILES.get('t_image1')
        tourimage2= request.FILES.get('t_image2')
        tourimage3 = request.FILES.get('t_image3')
        open_time=request.POST.get("open")
        close_time=request.POST.get("close")
        tourdescription = request.POST.get('t_description')


        data = tour_detail(
                tourcountry_id=cou_name,hotel_name_id=hotel_name,type_of_vehicle_id=vehicle_name,tourstate_id=state_name, tourcity_id=cityname, tourname_id=tourname,
                tourshort_code=tourshortcode, tourimage1=tourimage1,tourimage2=tourimage2,tourimage3=tourimage3,
                tourdescription=tourdescription,closed_time=close_time,open_time=open_time
            )
        data.save()


    display_tour_detials = tour_detail.objects.all()
    context = {
        "display_tour_detials": display_tour_detials,
        "country_cat": country_cat,
        "city_cat": city_cat,
        "state_cat":state_cat,
        "profiles":profiles,
        "tour_cat":tour_cat,
        "hotel_cat":hotel_cat,
        "vehicle_cat":vehicle_cat

    }
    return render(request,"tour_details.html",context)

def edit_tour_Details(request):
    display_tour_detials = tour_detail.objects.all()

    context = {"display_tour_detials": display_tour_detials}

    return redirect(request, "tour_details.html", context)


def update_tour_Details(request, id):
    if request.method == 'POST':
        cou_name = request.POST.get('countryname')
        state_name=request.POST.get("statename")
        cityname = request.POST.get('city_name')
        tourname = request.POST.get('t_name')
        hotel_name=request.POST.get("hotelname")
        vehicle_name=request.POST.get("vehiclename")
        tourshortcode = request.POST.get('t_shortcode')
        tourimage1 = request.FILES.get('t_image1')
        tourimage2= request.FILES.get('t_image2')
        tourimage3 = request.FILES.get('t_image3')
        open_time=request.POST.get("open")
        close_time=request.POST.get("close")
        tourdescription = request.POST.get('t_description')

        display_tour_detials = tour_detail(
              id=id,tourcountry_id=cou_name,tourstate_id=state_name,hotel_name_id=hotel_name,type_of_vehicle_id=vehicle_name, tourcity_id=cityname, tourname_id=tourname,
                tourshort_code=tourshortcode, tourimage1=tourimage1,tourimage2=tourimage2,tourimage3=tourimage3,
                tourdescription=tourdescription,closed_time=close_time,open_time=open_time
            )
        display_tour_detials.save()
        return redirect('tour_Details')

    return render(request, 'tour_details.html')



def delete_tour_Details(requset, pk):
    display_tour_detials = tour_detail.objects.filter(id=pk)
    display_tour_detials.delete()
    return redirect('tour_Details')


def deactivate_tour_Details(request, id):
    display_tour_detials = tour_detail.objects.get(id=id)
    display_tour_detials.tourstatus = False
    display_tour_detials.save()
    return redirect('tour_Details')


def activate_tour_Details(request, id):
    display_tour_detials = tour_detail.objects.get(id=id)
    display_tour_detials.tourstatus = True
    display_tour_detials.save()
    return redirect('tour_Details')
from django.http import JsonResponse


def ajax_load_cities(request):
    country_id = request.GET.get('country_id')
    state_id = request.GET.get('state_id')
    cities = city.objects.filter(city_country_id=country_id, city_state_id=state_id).values('id', 'city_name')
    return JsonResponse(list(cities), safe=False)


def load_states(request):
    country_id = request.GET.get('country_id')
    states = state.objects.filter(state_country_id=country_id).values('id', 'state_name')
    return JsonResponse(list(states), safe=False)


def ajax_load_tourplaces(request):
    country_id = request.GET.get('country_id')
    state_id = request.GET.get('state_id')
    city_id = request.GET.get('city_id')
    tourplaces = tourplace.objects.filter(tour_country_id=country_id, tour_state_id=state_id,
                                          tour_city_id=city_id).values('id', 'tour_name')
    return JsonResponse(list(tourplaces), safe=False)


def load_hotels(request):
    country_id = request.GET.get('country_id')
    city_id = request.GET.get('city_id')
    state_id = request.GET.get('state_id')
    hotels = add_hotel.objects.filter(country_name_id=country_id, state_name_id=state_id, city_name_id=city_id).values(
        'id', 'hotel_name')
    return JsonResponse(list(hotels), safe=False)


def ajax_load_names_of_vehicle(request):
    type_of_vehicle_id = request.GET.get('type_of_vehicle_id')
    names_of_vehicle = add_vehicle_details.objects.filter(type_of_vehicle_id=type_of_vehicle_id).values('id',
                                                                                                        'name_of_vehicle')
    return JsonResponse(list(names_of_vehicle), safe=False)


def packagetype(request):
    profiles = UserProfile.objects.all()
    if request.method == 'POST':
        pa_type = request.POST.get('packagetype')

        # Check if the package type already exists
        if not package_Type.objects.filter(package_type=pa_type).exists():
            p_type = package_Type(package_type=pa_type)
            p_type.save()
        else:
            # Display an error message
            messages.error(request, f'Package type "{pa_type}" already exists.')

        return redirect('packagetype')

    type = package_Type.objects.all()

    context = {
        'type': type,
        "profiles": profiles
    }
    return render(request, 'package_type.html', context)


def editpackagetype(request, pk):
    type = package_Type.objects.all()
    context = {
        'type': type
    }
    return render(request, 'package_type.html', context)


def updatepackagetype(request, id):
    if request.method == 'POST':
        pa_type = request.POST.get('packagetype')

        type = package_Type(
            id=id,
            package_type=pa_type
        )
        type.save()
        return redirect('packagetype')

    return render(request, 'package_type.html')


def deletepackagetype(request, pk):
    de = package_Type.objects.get(id=pk)
    de.delete()

    return redirect('packagetype')


def deactive_package_type(request, id):
    type = package_Type.objects.get(id=id)
    type.package_status = False
    type.save()
    return redirect('packagetype')


def active_package_type(request, id):
    type = package_Type.objects.get(id=id)
    type.package_status = True
    type.save()
    return redirect('packagetype')


def vehicletype(request):
    profiles = UserProfile.objects.all()
    veh = add_vehicle_type.objects.all()

    if request.method == 'POST':
        veh_type = request.POST.get('vehicletype')

        v_type = add_vehicle_type(
            type_of_vehicle=veh_type,

        )
        v_type.save()
        return redirect('vehicletype')

    context = {
        'veh': veh,
        "profiles": profiles
    }
    return render(request, 'add_vehicle_type.html', context)


def editvehicletype(request, pk):
    veh = add_vehicle_type.objects.all()
    context = {
        'veh': veh
    }
    return render(request, 'add_vehicle_type.html', context)


def updatevehicletype(request, id):
    if request.method == 'POST':
        veh_type = request.POST.get('vehicletype')

        veh = add_vehicle_type(
            id=id,
            type_of_vehicle=veh_type,

        )
        veh.save()
        return redirect('vehicletype')

    return render(request, 'add_vehicle_type.html')


def deletevehicletype(request, pk):
    de = add_vehicle_type.objects.get(id=pk)
    de.delete()

    return redirect('vehicletype')


def deactive_vehicletype(request, id):
    veh = add_vehicle_type.objects.get(id=id)
    veh.mode_status = False
    veh.save()
    return redirect('vehicletype')


def active_vehicletype(request, id):
    veh = add_vehicle_type.objects.get(id=id)
    veh.mode_status = True
    veh.save()
    return redirect('vehicletype')


def vehiclename(request):
    profiles = UserProfile.objects.all()
    veh_name = add_vehicle_name.objects.all()

    if request.method == 'POST':
        veh_name = request.POST.get('vehiclename')

        v_name = add_vehicle_name(
            name_of_vehicle=veh_name,

        )
        v_name.save()
        return redirect('vehiclename')

    context = {
        'veh_name': veh_name,
        "profiles": profiles
    }
    return render(request, 'add_vehicle_name.html', context)


def editvehiclename(request, pk):
    veh_name = add_vehicle_name.objects.all()
    context = {
        'veh_name': veh_name
    }
    return render(request, 'add_vehicle_name.html', context)


def updatevehiclename(request, id):
    if request.method == 'POST':
        # veh_type = request.POST.get('vehicletype')
        v_name = request.POST.get('vehiclename')

        veh_name = add_vehicle_name(
            id=id,
            # type_of_vehicle=veh_type,
            name_of_vehicle=v_name
        )
        veh_name.save()
        return redirect('vehiclename')

    return render(request, 'add_vehicle_name.html')


def deletevehiclename(request, pk):
    de = add_vehicle_name.objects.get(id=pk)
    de.delete()

    return redirect('vehiclename')


def active_vehiclename(request, id):
    veh = add_vehicle_name.objects.get(id=id)
    veh.mode_status = True
    veh.save()
    return redirect('vehiclename')


def deactive_vehiclename(request, id):
    veh = add_vehicle_name.objects.get(id=id)
    veh.mode_status = False
    veh.save()
    return redirect('vehiclename')


def vehicledetails(request):
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    vehicle_names = add_vehicle_name.objects.filter(mode_status=True)
    error_message_vehiclenumber = ""
    profiles = UserProfile.objects.all()
    if request.method == 'POST':
        vehicle_type_id = request.POST.get('vehicletype')
        vehicle_name_id = request.POST.get('vehiclename')
        vehicle_number = request.POST.get('vehiclenumber')
        seating_capacity = request.POST.get("seatingcapacity")
        tot = request.POST.get('tot')
        type_of_vehicle = add_vehicle_type.objects.get(id=vehicle_type_id)
        name_of_vehicle = add_vehicle_name.objects.get(id=vehicle_name_id)

        # Check if the vehicle number already exists
        if add_vehicle_details.objects.filter(vehicle_number=vehicle_number).exists():
            error_message_vehiclenumber = "Vehicle number already exists."
        else:
            # Vehicle number is unique, proceed with creating the add_vehicle_details instance
            vehicle_details = add_vehicle_details(
                type_of_vehicle=type_of_vehicle,
                name_of_vehicle=name_of_vehicle,
                vehicle_number=vehicle_number,
                seating_capacity=seating_capacity,
                type_of_transport=tot,
            )
            vehicle_details.save()

    # Retrieve the existing vehicle details
    det = add_vehicle_details.objects.all().select_related('type_of_vehicle', 'name_of_vehicle')

    # Include 'vehicle_names' in the context to ensure the dropdown is populated
    context = {
        'vehicle_types': vehicle_types,
        'vehicle_names': vehicle_names,
        'det': det,
        'error_message_vehiclenumber': error_message_vehiclenumber,
        "profiles": profiles
    }

    return render(request, 'add_vehicle_details.html', context)


def editvehicledetails(request, pk):
    det = add_vehicle_details.objects.all()
    context = {
        'det': det
    }
    return render(request, 'add_vehicle_details.html', context)


def updatevehicledetails(request, id):
    if request.method == 'POST':
        vehicle_type_id = request.POST.get('vehicletype')
        vehicle_name_id = request.POST.get('vehiclename')
        vehicle_number = request.POST.get('vehiclenumber')
        seating_capacity = request.POST.get("seatingcapacity")
        tot = request.POST.get('tot')
        type_of_vehicle_instance = add_vehicle_type.objects.filter(id=vehicle_type_id).first()
        name_of_vehicle_instance = add_vehicle_name.objects.filter(id=vehicle_name_id).first()
        vehicle_details = add_vehicle_details(
            id=id,
            type_of_vehicle=type_of_vehicle_instance,
            name_of_vehicle=name_of_vehicle_instance,
            vehicle_number=vehicle_number,
            seating_capacity=seating_capacity,
            type_of_transport=tot,
        )
        vehicle_details.save()
        return redirect('vehicledetails')
    return render(request, 'add_vehicle_details.html')


def deletevehicledetails(request, pk):
    vehi = add_vehicle_details.objects.get(id=pk)
    vehi.delete()
    return redirect('vehicledetails')


def deactive_vehicledetails(request, id):
    veh = add_vehicle_details.objects.get(id=id)
    veh.vehicle_details_status = False
    veh.save()
    return redirect('vehicledetails')


def active_vehicledetails(request, id):
    veh = add_vehicle_details.objects.get(id=id)
    veh.vehicle_details_status = True
    veh.save()
    return redirect('vehicledetails')


def addhotels(request):
    countries = country.objects.filter(country_status=True)
    types = package_Type.objects.filter(package_status=True)
    city_cat = city.objects.filter(city_status=True)
    state_cat = state.objects.filter(state_status=True)
    profiles = UserProfile.objects.all()
    if request.method == 'POST':
        h_name = request.POST.get('hotel_name')
        type_hotel = request.POST.get('type_of_hotel')
        t_rooms = request.POST.get('total_rooms')
        type_rooms = request.POST.get('type_of_rooms')
        loc = request.POST.get('location')
        add = request.POST.get('address')
        h_image = request.FILES.get('h_image')
        h_image1 = request.FILES.get('h_image1')
        h_image2 = request.FILES.get('h_image2')
        cityname = request.POST.get('city_name')
        country_name = request.POST.get('country')
        state_name = request.POST.get("statename")
        display = country.objects.get(id=country_name)
        type_name = request.POST.get('package_type')
        type_instance = package_Type.objects.get(id=type_name)

        a_hotels = add_hotel(
            hotel_name=h_name,
            type_of_hotel=type_hotel,
            total_rooms=t_rooms,
            type_of_rooms=type_rooms,
            location=loc,
            Address=add,
            country_name=display,
            city_name_id=cityname,
            package_type=type_instance,
            image1=h_image,
            image2=h_image1,
            image3=h_image2,
            state_name_id=state_name
        )
        a_hotels.save()
        return redirect('addhotels')  # Adjust the URL name accordingly

    hotels = add_hotel.objects.all().select_related('country_name', 'city_name', 'package_type')
    # hoteldetail = add_hotel.objects.get(id=a_hotels.id)
    context = {
        'hotels': hotels,
        'countries': countries,
        'types': types,
        'city_cat': city_cat,
        "state_cat": state_cat,
        "profiles": profiles
        # 'hoteldetail': hoteldetail,

    }

    return render(request, 'add_hotels.html', context)


def editaddhotels(request, pk):
    hotels = add_hotel.objects.all()
    context = {
        'hotels': hotels
    }
    return render(request, 'add_hotels.html', context)


def updateaddhotels(request, id):
    if request.method == 'POST':
        h_name = request.POST.get('hotel_name')
        type_hotel = request.POST.get('type_of_hotel')
        t_rooms = request.POST.get('total_rooms')
        add = request.POST.get('address')
        h_image = request.FILES.get('h_image')
        h_image1 = request.FILES.get('h_image1')
        h_image2 = request.FILES.get('h_image2')
        loc = request.POST.get('location')
        type_rooms = request.POST.get('type_of_rooms')
        city_name = request.POST.get('city')
        country_name = request.POST.get('country')
        state_name = request.POST.get("statename")  # Assuming 'country' contains the name of the country
        display = country.objects.get(id=country_name)
        type_name = request.POST.get('package_type')
        # Assuming type_name contains the value of the package type
        package_type = package_Type.objects.get(id=type_name)
        # Retrieve the first matching package type

        hotel = add_hotel(
            id=id,
            hotel_name=h_name,
            type_of_hotel=type_hotel,
            total_rooms=t_rooms,
            Address=add,
            location=loc,
            type_of_rooms=type_rooms,
            city_name_id=city_name,
            image1=h_image,
            image2=h_image1,
            image3=h_image2,
            country_name=display,
            state_name_id=state_name,
            package_type=package_type

        )
        hotel.save()
        return redirect('addhotels')

    return render(request, 'add_hotels.html')


def deleteaddhotels(request, pk):
    de = add_hotel.objects.get(id=pk)
    de.delete()

    return redirect('addhotels')


def deactive_addhotels(request, id):
    veh = add_hotel.objects.get(id=id)
    veh.hotel_status = False
    veh.save()
    return redirect('addhotels')


def active_addhotels(request, id):
    veh = add_hotel.objects.get(id=id)
    veh.hotel_status = True
    veh.save()
    return redirect('addhotels')


def manage_user(request):
    profiles = UserProfile.objects.all()
    packagecode = package_details.objects.filter(package_details_status=True)
    if request.method == "POST":
        username = request.POST.get("user")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        profile = request.POST.get("profile")
        code = request.POST.get("code")

        # Check for duplicate email
        if manage_users.objects.filter(email=email).exists():
            error_message_email = "Email already exists. Please use a different email."
        else:
            error_message_email = ""

        # Check for duplicate contact
        if manage_users.objects.filter(contact=contact).exists():
            error_message_contact = "Contact number already exists. Please use a different contact number."
        else:
            error_message_contact = ""

        if manage_users.objects.filter(profile=profile).exists():
            error_message_proof = "Proof ID Number  already exists. Please use a different ID number."
        else:
            error_message_proof = ""

        # If there are errors, display them
        if error_message_email or error_message_contact or error_message_proof:
            display_user = manage_users.objects.all()
            context = {
                "error_message_email": error_message_email,
                "error_message_contact": error_message_contact,
                "error_message_proof": error_message_proof,
                "display_user": display_user,
                "packagecode": packagecode,
                "profiles": profiles
            }
            return render(request, "manage_users.html", context)
        else:
            # If no errors, save the data
            data = manage_users(
                username=username,
                email=email,
                contact=contact,
                age=age,
                gender=gender,
                profile=profile,
                package_code_id=code
            )
            data.save()

    # If it's a GET request or after successfully saving the data, display the form
    display_user = manage_users.objects.all()
    context = {"display_user": display_user, "packagecode": packagecode, "profiles": profiles}
    return render(request, "manage_users.html", context)


def edit_user(request):
    display_user = manage_users.objects.all()

    context = {"display_user": display_user}

    return redirect(request, "manage_users.html", context)


def update_user(request, id):
    if request.method == "POST":
        e_username = request.POST.get("edit_username")
        e_email = request.POST.get("edit_email")
        e_contact = request.POST.get("edit_contact")
        e_age = request.POST.get("edit_age")
        e_gender = request.POST.get("edit_gender")
        e_profile = request.POST.get("edit_profile")
        code = request.POST.get("code")
        display_user = manage_users(
            id=id,
            username=e_username,
            email=e_email,
            contact=e_contact,
            age=e_age,
            gender=e_gender,
            profile=e_profile,
            package_code_id=code
        )
        display_user.save()
        return redirect("manageuser")

    return render(request, "manage_users.html")


def delete_user(requset, pk):
    display_user = manage_users.objects.filter(id=pk)
    display_user.delete()
    return redirect("manageuser")


def guidedetails(request):
    error_message_guide_name = error_message_contact_number = error_message_aadhar_number = ''
    display = add_guide.objects.all()  # Assuming you want to display all guides initially
    profiles = UserProfile.objects.all()
    if request.method == 'POST':
        g_name = request.POST.get('guidename')
        g_age = request.POST.get('age')
        num = request.POST.get('number')
        aa_num = request.POST.get('aa_number')
        exp = request.POST.get('expe')
        aa_image = request.FILES.get('aadhaar_image')
        tem_add = request.POST.get('tem_address')
        per_add = request.POST.get('per_address')
        lan = request.POST.getlist('languages')
        gui_gender = request.POST.get('gender')

        # Check if guide_name, guide_contact_number, and guide_aadhar_number already exist
        if add_guide.objects.filter(guide_name=g_name).exists():
            error_message_guide_name = "Guide Name already exists."
        if add_guide.objects.filter(guide_contact_number=num).exists():
            error_message_contact_number = "Contact number already exists."
        if add_guide.objects.filter(guide_aadhar_number=aa_num).exists():
            error_message_aadhar_number = "Aadhar number already exists."

        # If there are no errors, save the details
        if not error_message_guide_name and not error_message_contact_number and not error_message_aadhar_number:
            details = add_guide(
                guide_name=g_name,
                guide_age=g_age,
                guide_contact_number=num,
                guide_aadhar_number=aa_num,
                guide_experience=exp,
                guide_aadhar=aa_image,
                guide_tem_add=tem_add,
                guide_permanent_add=per_add,
                guide_languages_known=lan,
                gender=gui_gender,
            )
            details.save()
        else:
            # If there are errors, retrieve the existing data and render the page
            display = add_guide.objects.all()

    context = {
        "display": display,
        "error_message_guide_name": error_message_guide_name,
        "error_message_aadhar_number": error_message_aadhar_number,
        "error_message_contact_number": error_message_contact_number,
        "profiles": profiles
    }
    return render(request, 'guide_details.html', context)


def editguidedetails(request, pk):
    details = add_guide.objects.all()
    context = {
        'details': details
    }
    return render(request, 'add_hotels.html', context)


def updateguidedetails(request, id):
    if request.method == 'POST':
        g_name = request.POST.get('guidename')
        g_age = request.POST.get('age')
        num = request.POST.get('number')
        aa_num = request.POST.get('aa_number')
        exp = request.POST.get('expe')
        aa_image = request.FILES.get('aadhaar_image')
        tem_add = request.POST.get('tem_address')
        per_add = request.POST.get('per_address')
        lan = request.POST.getlist('languages')
        gui_gender = request.POST.get('gender')

        details = add_guide(
            id=id,
            guide_name=g_name,
            guide_age=g_age,
            guide_contact_number=num,
            guide_aadhar_number=aa_num,
            guide_experience=exp,
            guide_aadhar=aa_image,
            guide_tem_add=tem_add,
            guide_permanent_add=per_add,
            guide_languages_known=lan,
            gender=gui_gender,
        )
        details.save()
        return redirect('guidedetails')

    return render(request, 'guide_details.html')


def deleteguidedetails(request, pk):
    gui = add_guide.objects.get(id=pk)
    gui.delete()

    return redirect('guidedetails')


def deactive_guidedetails(request, id):
    guide = add_guide.objects.get(id=id)
    guide.guide_status = False
    guide.save()
    return redirect('guidedetails')


def active_guidedetails(request, id):
    guide = add_guide.objects.get(id=id)
    guide.guide_status = True
    guide.save()
    return redirect('guidedetails')


def packagedetails(request):
    profiles = UserProfile.objects.all()
    all_package_types = package_Type.objects.filter(package_status=True)
    all_hotels = add_hotel.objects.filter(hotel_status=True)
    all_countries = country.objects.filter(country_status=True)
    all_states = state.objects.filter(state_status=True)
    all_cities = city.objects.filter(city_status=True)
    all_tour_places = tourplace.objects.filter(tour_status=True)
    vehicle_types = add_vehicle_type.objects.filter(mode_status=True)
    guides = add_guide.objects.filter(guide_status=True)
    if request.method == 'POST':
        country_name = request.POST.get('country_name')
        city_name = request.POST.get('city_name')
        state_name = request.POST.get('statename')
        tour_places_ids = request.POST.getlist('languages')
        tour_places_objs = tourplace.objects.filter(id__in=tour_places_ids)
        package_type = request.POST.get('package_type')
        vehicle_type = request.POST.get('vehicle_type')
        number_of_persons = request.POST.get('number_of_persons')
        package_code = request.POST.get('package_code')
        duration = int(request.POST.get('duration'))
        image = request.FILES.get('image')
        title = request.POST.get('title')
        hotel_name = request.POST.get('hotel_name')
        cost = request.POST.get('cost')
        itinerary = request.POST.get('itinerary')
        description = request.POST.get('description')
        guide = request.POST.get("guide")

        itinerary_items = itinerary.split('\n')
        limited_itinerary_items = itinerary_items[:duration]
        limited_itinerary = '\n'.join(limited_itinerary_items)
        # Check if a package with the same code already exists
        if package_details.objects.filter(package_code=package_code).exists():
            error_message_package_code = "Package with this code already exists."
        else:
            error_message_package_code = ""

        if not error_message_package_code:
            package_details_obj = package_details(
                country_name_id=country_name,
                city_name_id=city_name,
                package_type_id=package_type,
                type_of_vehicle_id=vehicle_type,
                number_of_persons=number_of_persons,
                package_code=package_code,
                duration=duration,
                image=image,
                title=title,
                hotel_name_id=hotel_name,
                cost=cost,
                state_name_id=state_name,
                description=description,
                iternary=limited_itinerary,
                guide_name_id=guide,

            )
            package_details_obj.save()
            # Add the tour places to the package details
            package_details_obj.tour_places.set(tour_places_objs)
            package_details_obj.save()
        else:
            # If there is an error, retrieve the list of package details and render the page
            display_package = package_details.objects.all()
            context = {
                'display_package': display_package,
                'all_tour_places': all_tour_places,
                'all_countries': all_countries,
                'all_cities': all_cities,
                'all_package_types': all_package_types,
                'all_hotels': all_hotels,
                'vehicle_types': vehicle_types,
                "guides": guides,
                "all_states": all_states,
                'error_message_package_code': error_message_package_code,
                "profiles": profiles
            }
            return render(request, 'package_details.html', context)

    # Retrieve the list of package details
    display_package = package_details.objects.all()
    context = {
        'display_package': display_package,
        'all_tour_places': all_tour_places,
        'all_countries': all_countries,
        'all_cities': all_cities,
        'all_package_types': all_package_types,
        'all_hotels': all_hotels,
        'vehicle_types': vehicle_types,
        "guides": guides,
        "all_states": all_states,
        "profiles": profiles
    }
    return render(request, 'package_details.html', context)


def editpackage(request):
    display_package = package_details.objects.all()
    context = {
        "display_package": display_package
    }
    return render(request, "package_details.html", context)


def editpackage(request):
    display_package = package_details.objects.all()
    context = {
        "display_package": display_package
    }
    return render(request, "package_details.html", context)


def updatepackage(request, id):
    if request.method == 'POST':
        e_country_name = request.POST.get('edit_country_name')
        e_city_name = request.POST.get('edit_city_name')
        e_state_name = request.POST.get('statename')
        e_tour_places_ids = request.POST.getlist('languages')
        e_tour_places_objs = tourplace.objects.filter(id__in=e_tour_places_ids)
        e_package_type = request.POST.get('edit_package_type')
        e_vehicle_type = request.POST.get('edit_vehicle_type')
        e_number_of_persons = request.POST.get('edit_number_of_persons')
        e_package_code = request.POST.get('edit_package_code')
        e_duration = int(request.POST.get('edit_duration'))
        e_image = request.FILES.get('edit_image')
        e_title = request.POST.get('edit_title')
        e_hotel_name = request.POST.get('edit_hotel_name')
        e_cost = request.POST.get('edit_cost')
        e_itinerary = request.POST.get('edit_itinerary')
        e_description = request.POST.get('edit_description')
        guide = request.POST.get("guide")
         # Split itinerary into a list of items
        e_itinerary_items = e_itinerary.split('\n')

        # Limit the itinerary items based on the specified duration
        limited_e_itinerary_items = e_itinerary_items[:e_duration]

        # Join the limited itinerary items back into a string
        limited_e_itinerary = '\n'.join(limited_e_itinerary_items)
        # Get the existing package_details object
        
        display_package = package_details.objects.get(id=id)

        # Update the fields of the existing object
        display_package.country_name_id = e_country_name
        display_package.city_name_id = e_city_name
        display_package.state_name_id = e_state_name
        display_package.tour_places.set(e_tour_places_objs)
        display_package.package_type_id = e_package_type
        display_package.type_of_vehicle_id = e_vehicle_type
        display_package.number_of_persons = e_number_of_persons
        display_package.package_code = e_package_code
        display_package.duration = e_duration
        display_package.image = e_image
        display_package.title = e_title
        display_package.hotel_name_id = e_hotel_name
        display_package.cost = e_cost
        display_package.description = e_description
        display_package.iternary = limited_e_itinerary
        display_package.guide_name_id = guide

        # Save the updated package_details object
        display_package.save()

        return redirect('packagedetails')

    return render(request, 'package_details.html')


def deletepackage(request, pk):
    display_package = package_details.objects.get(id=pk)
    display_package.delete()
    return redirect('packagedetails')


def deactivate_package(request, id):
    deactivate_package = package_details.objects.get(id=id)
    deactivate_package.package_details_status = False
    deactivate_package.save()
    return redirect('packagedetails')


def activate_package(request, id):
    activate_package = package_details.objects.get(id=id)
    activate_package.package_details_status = True
    activate_package.save()
    return redirect('packagedetails')


def aboutus(request):
    about = about_us.objects.all()
    contact_count = about.count()
    profiles = UserProfile.objects.all()
    existing_contact = about.first() if contact_count >= 1 else None
    if request.method == 'POST':
        if contact_count >= 1:
            return render(request, "contact_us.html", {'about': about, 'existing_contact': existing_contact})
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get("image4")
        sub = request.POST.get('subject')
        desc = request.POST.get('description')

        aboutus = about_us(
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            subject=sub,
            description=desc
        )
        aboutus.save()
        return redirect('aboutus')

    context = {
        'about': about,
        'existing_contact': existing_contact,
        "profiles": profiles
    }
    return render(request, "about_us.html", context)


def edit_aboutus(request):
    about = about_us.objects.all()

    context = {
        "about": about
    }

    return redirect(request, "about_us.html", context)


def update_aboutus(request, id):
    about = about_us.objects.get(id=id)
    if request.method == 'POST':
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get("image4")
        sub = request.POST.get('subject')
        desc = request.POST.get('description')

        aboutus = about_us(
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            subject=sub,
            description=desc
        )
        aboutus.save()
        return redirect('aboutus')

    return render(request, 'about_us.html')


def delete_aboutus(request, pk):
    delete = about_us.objects.filter(id=pk)
    delete.delete()

    return redirect('aboutus')


def deactivate_aboutus(request, id):
    about_u = about_us.objects.get(id=id)
    about_u.about_status = False
    about_u.save()
    return redirect('aboutus')


def activate_aboutus(request, id):
    ac_us = about_us.objects.get(id=id)
    ac_us.about_status = True
    ac_us.save()
    return redirect('aboutus')


def contactus(request):
    contact = contact_us.objects.all()
    profiles = UserProfile.objects.all()
    # Initialize error messages
    error_message_mobile = ''
    error_message_email = ''
    contact_count = contact.count()
    existing_contact = contact.first() if contact_count >= 1 else None
    if request.method == 'POST':
        if contact_count >= 1:
            return render(request, "contact_us.html", {'contact': contact, 'existing_contact': existing_contact})
        b_image = request.FILES.get('image')
        subject = request.POST.get('subject')
        desc = request.POST.get('description')
        add = request.POST.get('address')
        mobile = request.POST.get('mobile_num')
        email = request.POST.get('email_id')
        websites = request.POST.get('website')

        # Check for duplicate mobile number
        if contact_us.objects.filter(mobile_num=mobile).exists():
            error_message_mobile = 'Mobile number already exists.'
            return render(request, "contact_us.html",
                          {'contact': contact, 'error_message_mobile': error_message_mobile})

        # Check for duplicate email
        if contact_us.objects.filter(email=email).exists():
            error_message_email = 'Email already exists.'
            return render(request, "contact_us.html", {'contact': contact, 'error_message_email': error_message_email})

        contactus = contact_us(
            banner_image=b_image,
            subject=subject,
            description=desc,
            address=add,
            mobile_num=mobile,
            email=email,
            website=websites
        )

        # If no errors, save the data
        contactus.save()
        return redirect('contactus')

    context = {
        'contact': contact,
        'error_message_mobile': error_message_mobile,
        'error_message_email': error_message_email,
        'existing_contact': existing_contact,
        "profiles": profiles
    }
    return render(request, "contact_us.html", context)


def edit_contactus(request):
    contact = contact_us.objects.all()

    context = {
        "contact": contact
    }

    return redirect(request, "contact_us.html", context)


def update_contactus(request, id):
    if request.method == 'POST':
        b_image = request.FILES.get('image')
        sub = request.POST.get('subject')
        desc = request.POST.get('description')
        add = request.POST.get('address')
        mobile = request.POST.get('mobile_num')
        email = request.POST.get('email_id')
        website = request.POST.get('website')

        contact = contact_us(
            id=id,
            banner_image=b_image,
            subject=sub,
            description=desc,
            address=add,
            mobile_num=mobile,
            email=email,
            website=website
        )
        contact.save()
        return redirect('contactus')

    return render(request, 'about_us.html')


def delete_contactus(request, pk):
    delet = contact_us.objects.filter(id=pk)
    delet.delete()

    return redirect('contactus')


def deactivate_contactus(request, id):
    deactivate_contactus = contact_us.objects.get(id=id)
    deactivate_contactus.contact_status = False
    deactivate_contactus.save()
    return redirect('contactus')


def activate_contactus(request, id):
    activate_contactus = contact_us.objects.get(id=id)
    activate_contactus.contact_status = True
    activate_contactus.save()
    return redirect('contactus')


def user_profile(request):
    profiles = UserProfile.objects.all()

    # Assuming you want to display the details of the first contact (if it exists)

    context = {

        "profiles": profiles,
    }
    return render(request, "user_profile.html", context)


def create_profile(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        name = request.POST.get("name")
        mobile = request.POST.get("mobile_num")
        email = request.POST.get("email")

        profile = UserProfile(
            image=image,
            name=name,
            mobile=mobile,
            email=email
        )
        profile.save()
        return redirect("userprofile")
    profiles = UserProfile.objects.all()
    context = {
        "profiles": profiles
    }
    return render(request, "create_profile.html", context)


def edit_profile(request):
    profiles = UserProfile.objects.all()

    context = {
        "profiles": profiles
    }

    return redirect(request, "user_profile.html", context)


def update_profile(request, profile_id):
    if request.method == "POST":
        image = request.FILES.get("image")
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        profiles = UserProfile(
            id=profile_id,
            image=image,
            name=name,
            mobile=mobile,
            email=email

        )
        profiles.save()
        return redirect("userprofile")

    return render(request, "user_profile.html")

# def delete_profile(request, profile_id):
#     user = UserProfile.objects.get(id=profile_id)


#     user.delete()
#     return redirect("create_profile")


# def activate_profile(request, profile_id):
#     user = UserProfile.objects.get(id=profile_id)
#     user.user_status = True
#     user.save()
#     return redirect("create_profile")

# def deactivate_profile(request, profile_id):
#     user = UserProfile.objects.get(id=profile_id)
#     user.user_status = False
#     user.save()
#     return redirect("create_profile")