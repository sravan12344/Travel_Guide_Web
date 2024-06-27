from django.contrib import admin
from .models import *

class admin_sideAdmin(admin.ModelAdmin):
    list_display = ('id','country_name','city_name','tour_places','package_name','package_type','package_duration','add_vehicle_type')
    list_display_links = ('id','package_name')
    list_filter = ('package_type','package_duration')
    list_editable = ('package_duration')
    search_fields = ('country_name','city_name','package_name','tour_places','package_duration','add_vehicle_type')
    ordering = ('id')

admin.site.register(country)
admin.site.register(city)
admin.site.register(tourplace)
admin.site.register(package_Type)
admin.site.register(add_vehicle_type)
admin.site.register(add_vehicle_details)
admin.site.register(add_hotel)
admin.site.register(package_details)
admin.site.register(iterinary)
admin.site.register(manage_users)
admin.site.register(add_guide)
admin.site.register(about_us)
admin.site.register(contact_us)
