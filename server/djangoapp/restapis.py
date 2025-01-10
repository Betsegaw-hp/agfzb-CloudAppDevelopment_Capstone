import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
load_dotenv()
   

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # no idea what is happening below
        # Call get method of requests library with URL and parameters
        if True:
            print(os.getenv('IBM_NLU_API_KEY'))
            # params = dict()
            # params["text"] = kwargs["text"]
            # params["version"] = kwargs["version"]
            # params["features"] = kwargs["features"]
            # params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            # params["id"] = kwargs["id"]
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', os.getenv('IBM_NLU_API_KEY')))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
# def post_request(url, json_payload, **kwargs):
 

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
            # Get its content in `doc` object
            dealer_doc = dealer
            # print("Dealer",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id_from_cf(url,dealer_id,  **kwargs):
    result = {}
    json_result = get_request(url, dealer_id=dealer_id)
    if json_result:
        dealer_doc = json_result
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
        result = dealer_obj
    return result


def get_dealer_reviews_from_cf(url,dealer_id,  **kwargs):
    results = []
    print()
    json_result = get_request(url,id=dealer_id, auth=True)
    if json_result:
        # Get the row list in JSON as dealers
        dealer_review = json_result

        for review in json_result:
            dealer_review_obj = DealerReview(id=review["id"],dealership=review["dealership"], name=review["name"],purchase=review["purchase"],
                                            review=review["review"],purchase_date=review["purchase_date"],car_make=review["car_make"],
                                            car_model=review["car_model"],car_year=review["car_year"])
        
            dealer_review_obj.sentiment = analyze_review_sentiments(dealer_review_obj.review)
            results.append(dealer_review_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    authenticator = IAMAuthenticator(os.getenv('IBM_NLU_API_KEY'))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(os.getenv('IBM_NLU_URL'))

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,
                                    limit=2))).get_result()

    # print(json.dumps(response, indent=2)) 
    return response["keywords"][0]["sentiment"]["label"]