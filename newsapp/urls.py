from django.urls import path
from newsapp import views

urlpatterns = [
    path('', views.home, name="Home_Page"),
    path('home', views.home, name="Main_Home_Page"),
    path('business', views.business_news, name="Business_Page"),
    path('entertainment', views.entertainment_news, name="Entertainment_Page"),
    path('sports', views.sports_news, name="Sports_Page"),
    path('general', views.general_news, name="General_Page"),
    path('technology', views.technology_news, name="Technology_Page"),
    path('health', views.health_news, name="Health_Page"),
    path('world', views.world_news, name="World_Page"),

    path('about', views.about_page, name="About_Page"),
    path('contactus', views.contactus_page, name="Contactus_Page"),
    path('search', views.search_news, name="search"),
    path('set/', views.set_local_storage_data, name='set_local_storage_data'),
]