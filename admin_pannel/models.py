
from django.db import models
from datetime import datetime

# Create your models here.
class country(models.Model):
    country_image = models.ImageField(null=False, blank=False)
    country_name = models.CharField(max_length=20, null=False, blank=False,unique=True)
    country_short_code = models.CharField(max_length=8, null=False, blank=False,unique=True)
    country_description = models.TextField()
    country_created_at = models.DateTimeField(default=datetime.now, blank=True)
    country_status = models.BooleanField(default=False)
    def __str__(self):
        return self.country_name

class state(models.Model):
    state_image = models.ImageField(null=False, blank=False)
    state_name = models.CharField(max_length=20, null=False, blank=False,unique=True)
    state_short_code = models.CharField(max_length=8, null=False, blank=False,unique=True)
    state_description = models.TextField()
    state_created_at = models.DateTimeField(default=datetime.now, blank=True)
    state_status = models.BooleanField(default=False)
    state_country = models.ForeignKey(country, on_delete=models.CASCADE, null=True,blank=False)
    def __str__(self):
        return self.country_name


class city(models.Model):
    city_image = models.ImageField(null=False, blank=False)
    city_name = models.CharField(max_length=20, null=False, blank=False,unique=True)
    city_description = models.TextField()
    city_created_at = models.DateTimeField(default=datetime.now, blank=True)
    city_status = models.BooleanField(default=False)
    city_short_code = models.CharField(max_length=8, null=False, blank=False,unique=True)
    city_country = models.ForeignKey(country, on_delete=models.CASCADE, null=True,blank=False)
    city_state = models.ForeignKey(state, on_delete=models.CASCADE, null=True,blank=False)
    def __str__(self):
        return self.city_name

class tourplace(models.Model):
    tour_image = models.ImageField(null=False, blank=False)
    tour_name = models.CharField(max_length=20, null=False, blank=False,unique=True)
    tour_description = models.TextField(null=True, blank=True)
    tour_created_at = models.DateTimeField(default=datetime.now, blank=True)
    tour_status = models.BooleanField(default=False)
    tour_short_code = models.CharField(max_length=8, null=False, blank=False)
    tour_city = models.ForeignKey(city, on_delete=models.CASCADE,  null=True,blank=False)
    tour_country = models.ForeignKey(country, on_delete=models.CASCADE, null=True,blank=False)
    tour_state = models.ForeignKey(state, on_delete=models.CASCADE, null=True,blank=False)
    def __str__(self):
        return self.tour_name
    
class package_Type(models.Model):
    package_type = models.CharField(max_length=100, null=True, blank=False,unique=True)
    package_created_at = models.DateTimeField(default=datetime.now, blank=True)
    package_status = models.BooleanField(default=False)
    def _str_(self):
        return self.package_type
    
class add_vehicle_type(models.Model):
    type_of_vehicle = models.CharField(max_length=100, null=False, blank=False)
    mode_created_at = models.DateTimeField(default=datetime.now, blank=True)
    mode_status = models.BooleanField(default=False)
    def __str__(self):
        return self.type_of_vehicle
    
class add_hotel(models.Model):
    country_name = models.ForeignKey(country, on_delete=models.CASCADE, null=True, blank=False)
    city_name = models.ForeignKey(city, on_delete=models.CASCADE, null=True, blank=False)
    state_name = models.ForeignKey(state, on_delete=models.CASCADE, null=True,blank=False)
    hotel_name = models.CharField(max_length=20, null=False, blank=False)
    type_of_hotel = models.CharField(max_length=20, null=False, blank=False)
    image1 = models.ImageField(null=False, blank=False)
    image2 = models.ImageField(null=False, blank=False)
    image3 = models.ImageField(null=False, blank=False)
    total_rooms = models.IntegerField(null=False, blank=False)
    type_of_rooms = models.CharField(max_length=10, null=False, blank=False)
    location = models.URLField(null=False, blank=False)
    package_type = models.ForeignKey(package_Type, on_delete=models.CASCADE, null=True, blank=False)
    Address = models.TextField(null=False, blank=True)
    # hotel_description=models.TextField(null=False, blank=True)
    hotel_created_at = models.DateTimeField(default=datetime.now, blank=True)
    hotel_status = models.BooleanField(default=False)
    def __str__(self):
        return self.hotel_name

    
class tour_detail(models.Model):
    tourimage1 = models.ImageField(null=False, blank=False)
    tourimage2= models.ImageField(null=False, blank=False)
    tourimage3 = models.ImageField(null=False, blank=False)
    open_time=models.CharField(max_length=20, null=False, blank=False)
    closed_time=models.CharField(max_length=20, null=False, blank=False)
    tourname = models.CharField(max_length=20, null=False, blank=False,unique=True)
    tourdescription = models.TextField(null=True, blank=True)
    tourcreated_at = models.DateTimeField(default=datetime.now, blank=True)
    tourstatus = models.BooleanField(default=False)
    tourshort_code = models.CharField(max_length=8, null=False, blank=False)
    tourcity = models.ForeignKey(city, on_delete=models.CASCADE,  null=True,blank=False)
    tourname = models.ForeignKey(tourplace, on_delete=models.CASCADE,  null=True,blank=False)
    type_of_vehicle=models.ForeignKey(add_vehicle_type,on_delete=models.CASCADE,null=False,blank=False,default=True)
    hotel_name = models.ForeignKey(add_hotel, on_delete=models.CASCADE,null=True,blank=False)
    tourcountry = models.ForeignKey(country, on_delete=models.CASCADE, null=True,blank=False)
    tourstate = models.ForeignKey(state, on_delete=models.CASCADE, null=True,blank=False)
    def __str__(self):
            return self.tourname


class add_vehicle_name(models.Model):
    name_of_vehicle = models.CharField(max_length=100, null=False, blank=False)
    mode_created_at = models.DateTimeField(default=datetime.now, blank=True)
    mode_status = models.BooleanField(default=False)
    def __str__(self):
        return self.name_of_vehicle

class add_vehicle_details(models.Model):
    type_of_vehicle = models.ForeignKey(add_vehicle_type, on_delete=models.CASCADE, null=True, blank=False,)
    name_of_vehicle = models.ForeignKey(add_vehicle_name, on_delete=models.CASCADE, null=True, blank=False,)
    vehicle_number = models.CharField(max_length=100, null=True, blank=False ,unique=True)
    seating_capacity = models.IntegerField(null=False, blank=False)
    vehicle_details_created_at = models.DateTimeField(default=datetime.now, blank=True)
    type_of_transport = models.CharField(max_length=20, null=False, blank=False)
    vehicle_details_status = models.BooleanField(default=False)
    def __str__(self):
        return self.name_of_vehicle.type_of_vehicle






class add_guide(models.Model):
    guide_name = models.CharField(max_length=50, null=False, blank=False,unique=True)
    guide_age = models.IntegerField(null=False, blank=False,unique=True)
    guide_contact_number = models.CharField(max_length=100, null=False, blank=False)
    guide_aadhar_number = models.CharField(max_length=100,null=False, blank=False,unique=True)
    guide_experience = models.FloatField(null=False, blank=False)
    guide_aadhar = models.ImageField(null=False, blank=False)
    guide_tem_add = models.TextField()
    guide_permanent_add = models.TextField()
    guide_languages_known = models.CharField(max_length=100, null=False, blank=False)
    gender = models.CharField(max_length=10,default=False)
    guide_created_at = models.DateTimeField(default=datetime.now, blank=True)
    guide_status = models.BooleanField(default=False)
    def __str__(self):
        return self.guide_languages_known
    

class package_details(models.Model):
    country_name = models.ForeignKey(country, on_delete=models.CASCADE,null=False,blank=False,default=True)
    state_name = models.ForeignKey(state, on_delete=models.CASCADE, null=True,blank=False)
    guide_name = models.ForeignKey(add_guide, on_delete=models.CASCADE,null=False,blank=False,default=True)
    city_name = models.ForeignKey(city, on_delete=models.CASCADE,null=False,blank=False,default=True)
    tour_places = tour_places = models.ManyToManyField(tourplace)
    package_type = models.ForeignKey(package_Type, on_delete=models.CASCADE,null=False,blank=False,default=True)
    number_of_persons = models.IntegerField(null=False, blank=True)
    package_code = models.CharField(max_length=10, null=False, blank=False,unique=True)
    duration = models.CharField(max_length=20,null=False, blank=False)
    image = models.ImageField(null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    type_of_vehicle=models.ForeignKey(add_vehicle_type,on_delete=models.CASCADE,null=False,blank=False,default=True)
    hotel_name = models.ForeignKey(add_hotel, on_delete=models.CASCADE,null=True,blank=False)
    cost = models.DecimalField(max_digits=12,decimal_places=2,null=False, blank=False)
    description = models.TextField()
    package_details_created_at = models.DateTimeField(default=datetime.now, blank=True)
    package_details_status = models.BooleanField(default=False)
    iternary=models.TextField()
    def _str_(self):
        return self.city_name
    
class manage_users(models.Model):
    username = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=20,unique=True)
    contact = models.BigIntegerField(unique=True, null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    gender = models.CharField(max_length=10,default=False)
    profile = models.ImageField(max_length=12,null=False, blank=False,unique=True)
    users_created_at = models.DateTimeField(default=datetime.now, blank=True)
    user_status = models.BooleanField(default=False)
    package_code=models.ForeignKey(package_details,on_delete=models.CASCADE,null=False,blank=True)
    def _str_(self):
        return self.username
class iterinary(models.Model):
    mode_of_transport = models.ForeignKey(add_vehicle_details, on_delete=models.CASCADE,null=False,blank=False)
    package_tour_name = models.ForeignKey(package_details, on_delete=models.CASCADE,null=False,blank=False)
    iternary_status = models.BooleanField(default=False)
    iterinary_created_at = models.DateTimeField(default=datetime.now, blank=True)
    def _str_(self):
        return self.package_tour_name
class contact_us(models.Model):
    banner_image = models.ImageField(null=False,blank=False)
    subject = models.TextField()
    description = models.TextField()
    address = models.TextField()
    mobile_num = models.CharField(max_length=100, null=False, blank=False,unique=True)
    email = models.CharField(max_length=100,null=False,blank=False,unique=True)
    contact_status = models.BooleanField(default=False)
    website=models.CharField(max_length=200,null=False,blank=False)
    def __str__(self):
        return self.mobile_num

class about_us(models.Model):
    image1 = models.ImageField(null=True, blank=False)
    image2 = models.ImageField(null=True, blank=False)
    image3 = models.ImageField(null=True, blank=False)
    image4=models.ImageField(null=True, blank=False)
    subject = models.CharField(max_length=100,null=True, blank=False)
    description = models.TextField()
    about_status = models.BooleanField(default=False)
    def __str__(self):
        return self.description

class UserProfile(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50,null=False,blank=False)
    email=models.EmailField(null=True,blank=False)
    users_created_at = models.DateTimeField(default=datetime.now, blank=True)
    user_status = models.BooleanField(default=False)

    def _str_(self):
        return self.name