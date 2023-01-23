from cloudant.client import Cloudant
from cloudant.error import CloudantException

def main(param_dict):
    DB_NAME = 'reviews'
    DOC_NAME = 'review'

    if DOC_NAME in param_dict:
        try:
            client = Cloudant.iam(
                account_name=param_dict["COUCH_USERNAME"],
                api_key=param_dict["IAM_API_KEY"],
                connect=True,
            )
            
            new_review = client[DB_NAME].create_document(param_dict[DOC_NAME])

            return {"body": new_review}
                
        except CloudantException as cloudant_exception:
            print("unable to connect")
            return {"error": cloudant_exception}
            
    return {
        'statusCode': 404,
        'message': 'Review is missing'
    }
