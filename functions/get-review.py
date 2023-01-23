
"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """
    DB_NAME = 'reviews'
    ALLOWED_FILTER = {"dealerId": "dealership", "rev": "_rev"} 
    reviewsList = []
    
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        
        for document in client[DB_NAME]:
            # reviewsList.append(document)
            for filter in ALLOWED_FILTER:
                db_field = ALLOWED_FILTER[filter]
                
                if filter in param_dict and db_field in document and param_dict[filter] == str(document[db_field]):
                    return {"body": document}
                    del document['_id']
                    del document['_rev']
                    reviewsList.append(document)
            
        # print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"body": reviewsList}
