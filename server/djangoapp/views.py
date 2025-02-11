from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

# from .models import related models
from .models import *

# from .restapis import related methods
from .restapis import *

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# ...


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method == "GET":
        URL = "https://us-south.functions.appdomain.cloud/api/v1/web/0f4069cb-e4a8-4bb4-8c9f-57ca55c8425a/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(URL)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', {"dealers":dealerships})

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
     if request.method == "GET":
        URL_REVIEW = "https://us-south.functions.appdomain.cloud/api/v1/web/0f4069cb-e4a8-4bb4-8c9f-57ca55c8425a/dealership-package/get-review"
        URL_DEALERSHIP = "https://us-south.functions.appdomain.cloud/api/v1/web/0f4069cb-e4a8-4bb4-8c9f-57ca55c8425a/dealership-package/get-dealership"
        reviews = get_dealer_reviews_from_cf(URL_REVIEW, dealer_id)
        dealership_info = get_dealers_from_cf(URL_DEALERSHIP, dealer_id=dealer_id)[0]
        # return HttpResponse(reviews)
        return render(request, 'djangoapp/dealer_details.html', {"reviews":reviews, "dealer":dealership_info})

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST" and request.user.is_authenticated:
        URL = "https://us-south.functions.appdomain.cloud/api/v1/web/0f4069cb-e4a8-4bb4-8c9f-57ca55c8425a/dealership-package/post-review"
        form = request.POST
        review = {
            "id": 0,
            "name": f"{request.user.first_name} {request.user.last_name}",
            "dealership": dealer_id,
            "review": form["content"],
            "purchase": False,
            }
        if form.get("purchasecheck"): 
            review["purchase"] = True
            review["purchase_date"] = form["purchasedate"]
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.carMake.name
            review["car_model"] = car.name
            review["car_year"]= car.year.strftime("%Y")
        json_payload = {"review": review}

        post_request(URL, json_payload, dealerId=dealer_id)
        
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    
    elif request.method == "GET":
        print("USER")
        print(request.user.first_name)
        URL = "https://us-south.functions.appdomain.cloud/api/v1/web/0f4069cb-e4a8-4bb4-8c9f-57ca55c8425a/dealership-package/get-dealership"
        dealership_info = get_dealers_from_cf(URL, dealer_id=dealer_id)[0]

        context = {
            "dealer":dealership_info,
            "cars": CarModel.objects.all()
        }

        return render(request, 'djangoapp/add_review.html', context)


