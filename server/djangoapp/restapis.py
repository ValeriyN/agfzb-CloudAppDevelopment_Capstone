import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                       auth=HTTPBasicAuth('apikey', kwargs["api_key"]), params=kwargs)
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(json_payload)
    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], state=dealer["state"], 
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result

        # For each review object
        for review in reviews:
            # Create a DealerReview object
            id = review["id"]
            name = review["name"]
            dealership = review["dealership"]
            review_txt = review["review"]
            purchase = review["purchase"]          
            purchase_date = review.get("purchase_date", "-")
            car_make = review.get("car_make", "-")
            car_model = review.get("car_model", "-")
            car_year = review.get("car_year", "-")
            sentiment = review.get("sentiment", "-")
            
            review_obj = DealerReview(id = id, name = name, dealership = dealership, review = review_txt, purchase = purchase, 
                                    purchase_date = purchase_date, car_make = car_make, car_model = car_model, 
                                    car_year = car_year, sentiment = sentiment )
            
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    URL = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/6a1c95c1-da4f-4be6-a614-aec3b2c127f2"
    API_KEY = "UTb1ILtigmwGs3YKJtl6cETnUBKSdR1xGyMzecIMPGH9"
    
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(URL)
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    return(label)


