from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from dotenv import load_dotenv
import logging
import json
import os
import random
load_dotenv()

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/login.html', context)
    else: 
        return render(request, 'djangoapp/login.html', context)



# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == "GET":
        logout(request)
        return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):

    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context )

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['psw']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user_exist = False

        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))

        if not user_exist:
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                            password=password)

            login(request, user)

            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context )

        

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "{}/dealerships/get".format(os.getenv("DEALERSHIP_URL"))
        dealerships = get_dealers_from_cf(url)
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['dealerships'] = dealerships
        return render(request,'djangoapp/index.html' ,context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "{}/api/get_reviews".format(os.getenv("REVIEW_URL"))
        dealerships = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context['dealer_details'] = dealerships
        return render(request,'djangoapp/dealer_details.html' ,context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            car_id = request.POST.get("car")
            car = CarModel.objects.get(id=car_id)
            review = {
                "id": random.randint(1, 10000),
                "time": datetime.utcnow().isoformat(),
                "dealership": dealer_id,
                "review": request.POST.get('review', ''),
                "name": request.user.username,
                "dealership": dealer_id,
                "purchase": True if request.POST.get('purchase', '')== 'on' else False,
                "purchase_date": request.POST.get('purchase_date', ''),
                "car_make": car.make.name,
                "car_model": car.name,
                "car_year": car.year.strftime("%Y") 
            }
            print(review)
            url = "{}/api/post_review".format(os.getenv("REVIEW_URL"))
            try:
                res = post_request(url, json_payload=review, dealerId=dealer_id)
                print(res)
                return HttpResponse(res) 
            except:
                print("Error occured.")
                return HttpResponse("Unexpected Error occured.") 
        else:
            return render(request, 'djangoapp/login.html', context)
    else:
        url = "{}/dealerships/get".format(os.getenv("DEALERSHIP_URL"))
        context["dealer"] = get_dealer_by_id_from_cf(url, dealer_id=dealer_id)
        context["cars"] = CarModel.objects.all()
        return render(request, 'djangoapp/add_review.html', context)
