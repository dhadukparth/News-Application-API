from django.shortcuts import render, redirect
from .imageslist import *
from dotenv import load_dotenv
from django.http import JsonResponse
load_dotenv()

import random, requests, datetime, os



news_category = ["general","business","entertainment","health","science","sports","technology"]

default_language = "en"
default_country = "in"
today = datetime.datetime.now().strftime("%Y-%m-%d")

api_key = os.environ.get('NEWS_API_KEY')

url = f"http://api.mediastack.com/v1/news?access_key={api_key}"


all_languages = {
    "ar" : "Arabic",
    "de" : "German",
    "en" : "English",
    "es" : "Spanish",
    "fr" : "French",
    "he" : "Hebrew",
    "it" : "Italian",
    "nl" : "Dutch",
    "no" : "Norwegian",
    "pt" : "Portuguese",
    "ru" : "Russian",
    "se" : "Swedish",
    "zh" : "Chinese"
}

all_country = {
    "ar":"Argentina",
    "au":"Australia",
    "at":"Austria",
    "be":"Belgium",
    "br":"Brazil",
    "bg":"Bulgaria",
    "ca":"Canada",
    "cn":"China",
    "co":"Colombia",
    "cz":"Czech Republic",
    "eg":"Egypt",
    "ce":"Fran",
    "de":"Germany",
    "gr":"Greece",
    "hk":"Hong Kong",
    "hu":"Hungary",
    "in":"India",
    "id":"Indonesia",
    "ie":"Ireland",
    "il":"Israel",
    "it":"Italy",
    "jp":"Japan",
    "lv":"Latvia",
    "lt":"Lithuania",
    "my":"Malaysia",
    "mx":"Mexico",
    "ma":"Morocco",
    "nl":"Netherlands",
    "nz":"New Zealand",
    "ng":"Nigeria",
    "no":"Norway",
    "ph":"Philippines",
    "pl":"Poland",
    "pt":"Portugal",
    "ro":"Romania",
    "sa":"Saudi Arabia",
    "rs":"Serbia",
    "sg":"Singapore",
    "sk":"Slovakia",
    "si":"Slovenia",
    "za":"South Africa",
    "kr":"South Korea",
    "se":"Sweden",
    "ch":"Switzerland",
    "tw":"Taiwan",
    "th":"Thailand",
    "tr":"Turkey",
    "ae":"UAE",
    "ua":"Ukraine",
    "gb":"United Kingdom",
    "us":"United States",
    "ve":"Venezuela"
}



def set_local_storage_data(request):
    if request.method == 'GET':
        storageCountry = request.GET['country']
        storageLanguage = request.GET['language']

        request.session['storage_country'] = storageCountry
        request.session['storage_language'] = storageLanguage

        response_data = {'message': 'Data received and processed'}
        return JsonResponse(response_data)


# Get Categories wise data fetch
def get_category_news(req, category, page):
    if 'storage_country' in req.session:
        country = req.session["storage_country"]
        language = req.session["storage_language"]
    else:
        country = random.choice(list(all_country.items()))
        language = random.choice(list(all_languages.items()))

    fetch_data = requests.get(url, params={
                                'categories': category,
                                'limit': 10,
                                'countries': country,
                                'languages': [language, "en"],
                                'offset': page,
                            }).json()
    if(len(fetch_data["data"]) == 0):
        fetch_data = requests.get(url, params={
                                'categories': category,
                                'limit': 10,
                                'languages': [language, "en"],
                                'offset': page,
                            }).json()

    return fetch_data


def home(request):
    try:
        if request.method == "GET":
            try:
                active_page = request.GET['page']
            except:
                active_page = 0

        if 'storage_country' in request.session:
            urlCountry = request.session["storage_country"]
            urlLanguage = request.session["storage_language"]
        else:
            urlCountry = random.choice(list(all_country.items()))
            urlLanguage = random.choice(list(all_languages.items()))

        random_category = random.choice(news_category)
        banner_panel = requests.get(url, params={
                                            'category': random_category,
                                            'limit': 6,
                                            'date': today,
                                            'countries': urlCountry,
                                            'languages': [urlLanguage,"en"],
                                    }).json()
        
        news_panel = requests.get(url, params={
                                            'category': random_category,
                                            'limit': 10,
                                            'date': today,
                                            'offset': active_page,
                                            'countries': urlCountry,
                                            'languages': [urlLanguage, "en"],
                                    }).json()
        get_all_news = requests.get(url, params={
                                            'limit': 5,
                                            'offset': active_page,
                                            'countries': urlCountry,
                                            'languages': [urlLanguage, "en"],
                                    }).json()

        response_data = {
            'banner_panel': banner_panel['data'],
            'news_panel': news_panel['data'],
            'all_news': get_all_news['data'],
            'all_news_pagination': get_all_news['pagination'],
            'page_active': active_page,
            'images': all_images,
            'languages': all_languages,
            'languages': all_languages,
            'country': all_country,
            'user_country': request.session['storage_country'],
            'user_language': request.session['storage_language'],
        }
        return render(request, 'index.html', response_data)
    except:
        return render(request, '404.html')


def business_news(request):
    try:
        if request.method == "GET":
            try:
                active_page = request.GET['page']
            except:
                active_page = 0

        fetch_business = get_category_news(request, "business",active_page)
        bdata = {
            'businessNews': fetch_business["data"],
            'all_news_pagination': fetch_business['pagination'],
            'page_active': active_page,
            'images': business_images,
            'languages': all_languages,
            'country': all_country,
            'user_country': request.session['storage_country'],
            'user_language': request.session['storage_language'],
        }
        return render(request, 'Pages/Business/business.html', bdata)
    except:
        return render(request, '404.html')


def entertainment_news(request):
    try:
        if request.method == "GET":
            try:
                active_page = request.GET['page']
            except:
                active_page = 0
        fetch_entertainment = get_category_news(request, "entertainment", active_page)
        data = {
            'entertainmentNews': fetch_entertainment["data"],
            'all_news_pagination': fetch_entertainment['pagination'],
            'page_active': active_page,
            'images': entertainment_images,
            'languages': all_languages,
            'country': all_country,
            'user_country': request.session['storage_country'],
            'user_language': request.session['storage_language'],
        }
        return render(request, 'Pages/Entertainment/entertainment.html', data)
    except:
        return render(request, '404.html')


def sports_news(request):
    try:
        if request.method == "GET":
            try:
                active_page = request.GET['page']
            except:
                active_page = 0

        fetch_sports = get_category_news(request, "sports", active_page)
        data = {
            'sportsNews': fetch_sports["data"],
            'all_news_pagination': fetch_sports['pagination'],
            'page_active': active_page,
            'images': sports_images,
        }
        return render(request, 'Pages/Sports/sports.html', data)
    except:
        return render(request, '404.html')


def general_news(request):
    try:
        if request.method == "GET":
            try:
                active_page = request.GET['page']
            except:
                active_page = 0
        fetch_general = get_category_news(request, "general", active_page)
        data = {
            'generalNews': fetch_general["data"],
            'all_news_pagination': fetch_general['pagination'],
            'page_active': active_page,
            # 'images': general_images,
            'languages': all_languages,
            'country': all_country,
            'user_country': request.session['storage_country'],
            'user_language': request.session['storage_language'],
        }
        return render(request, 'Pages/General/general.html', data)
    except:
        return render(request, '404.html')


def technology_news(request):
    # try:
        if request.method == "GET":
            try:
                active_page = request.GET['page']
            except:
                active_page = 0

        fetch_technology = get_category_news(request, "technology", active_page)
        data = {
            'technologyNews': fetch_technology["data"],
            'all_news_pagination': fetch_technology['pagination'],
            'page_active': active_page,
            'images': technology_images,
            'languages': all_languages,
            'country': all_country,
            'user_country': request.session['storage_country'],
            'user_language': request.session['storage_language'],
        }
        return render(request, 'Pages/Technology/technology.html', data)
    # except:
    #     return render(request, '404.html')


def health_news(request):
    try:
        if request.method == "GET":
            try:
                active_page = request.GET['page']
            except:
                active_page = 0
        fetch_health = get_category_news(request, "health", active_page)
        data = {
            'healthNews': fetch_health["data"],
            'all_news_pagination': fetch_health['pagination'],
            'page_active': active_page,
            'images': health_images,
            'languages': all_languages,
            'country': all_country,
            'user_country': request.session['storage_country'],
            'user_language': request.session['storage_language'],
        }
        return render(request, 'Pages/Health/health.html', data)
    except:
        return render(request, '404.html')


def world_news(request):
    try:
        if request.method == "GET":
            try:
                active_page = request.GET['page']
            except:
                active_page = 0

            fetch_world = requests.get(url, params={
                                    'limit': 24,
                                    'offset': active_page
                                }).json()

            data = {
                'worldNews': fetch_world["data"],
                'all_news_pagination': fetch_world['pagination'],
                'page_active': active_page,
                'images': world_images,
                'languages': all_languages,
                'country': all_country,
                'user_country': request.session['storage_country'],
                'user_language': request.session['storage_language'],
            }

            return render(request, 'Pages/World/world.html', data)
    except:
        return render(request, '404.html')


def about_page(request):
    try:
        data = {
            'languages': all_languages,
            'country': all_country,
        }

        if 'storage_country' in request.session:
            session_country = request.session['storage_country']
            session_language = request.session['storage_language']
            data.update(
                {
                    'user_country': session_country,
                    'user_language': session_language,
                }
            )

        else:
            request.session['storage_country'] = "in"
            request.session['storage_language'] = "en"


        return render(request, 'Pages/other/aboutPage.html', data)
    except:
            return render(request, '404.html')


def contactus_page(request):
    try:
        data = {
            'languages': all_languages,
            'country': all_country,
            'user_country': request.session['storage_country'],
            'user_language': request.session['storage_language'],
        }
        return render(request, 'Pages/other/contactus.html', data)
    except:     
        return render(request, '404.html')


def search_news(request):
    try:
        if request.method == "GET":
            try:
                search_query = request.GET['pq']
            except:
                search_query = ''

        fetch_search = requests.get(url, params={
                                            'keywords': search_query,
                                            'limit': 24
                                        }).json()


        data = {
            'searchNews': fetch_search["data"],
            'all_news_pagination': fetch_search['pagination'],
            'images': all_images,
            'languages': all_languages,
            'country': all_country,
            'user_country': request.session['storage_country'],
            'user_language': request.session['storage_language'],
        }
        return render(request, 'Pages/Search/search.html', data)

    except:
        return render(request, '404.html')