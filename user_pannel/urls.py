from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name="login_userpannel"),
    path('logout_userpannel/', views.logout_userpannel, name='logout_userpannel'),
    path('register/',views.register,name="register_userpannel"),
    path("otp/<int:pk>/",views.otp_verification,name="otp"),
    path('', views.userpannel_allpackage, name='userpannel_allpackages'),
    path('userpannel_packagetype<int:pk>/', views.userpannel_packagetypes, name='userpannel_packagetype'),
    path('userpannel_hotels/', views.userpannel_hotels, name='userpannel_hotels'),
    path('userpannel_bestpackages/', views.userpannel_bestpackages, name='userpannel_bestpackages'),
    path('booking<int:package_id>/', views.booking, name='booking'),
    path('create_ticket<int:package_id>/', views.create_ticket, name='create_ticket'),
    path('userpannel_payment<int:package_id>/', views.userpannel_payment, name='userpannel_payment'),
    path('userpannel_summary<int:package_id>/', views.userpannel_summary, name='userpannel_summary'),
    path('userpannel_contactus/', views.userpannel_contactus, name='userpannel_contactus'),
    path('userpannelmoredetails<int:package_id>/', views.userpannel_moredetail, name='userpannel_moredetails'),
    path('search_results/', views.search_results, name='search_results'),
    path('tour_search_results/', views.tour_search_results, name='tour_search_results'),
    path('vehicles_search_results/', views.vehicles_search_results, name='vehicles_search_results'),
    path('packageduration<str:selected_duration>/', views.packageduration, name='packageduration'),
    path('hoteldetails<int:id>', views.hoteldetails, name='hoteldetails'),
    path('tourdetails<int:id>', views.tourdetails, name='tourdetails'),
    path('userpannel_hotels/', views.userpannel_hotels, name='userpannel_hotels'),
    path("new/",views.new,name="new"),

   
]
