/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
// function main(params) {
//     console.log("test function");
// 	return { message: 'Hello World' };
// }


const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const DB_NAME = 'dealerships';
      const ALLOWED_FILTERS = ["city", "state"];
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });

      cloudant.setServiceUrl(params.COUCH_URL);
      try {
        let queryResult = await cloudant.postAllDocs({db: DB_NAME, includeDocs: true});
        let dealershipsList = queryResult.result.rows.map(row => { 
                delete row.doc._id;
                delete row.doc._rev;
                return row.doc;
            });
            
        ALLOWED_FILTERS.forEach(
            filter => {
                if (filter in params) {
                    let filteredDealershipsList = dealershipsList.filter(
                        dealership => dealership[filter] == params[filter]
                    );
                    dealershipsList = filteredDealershipsList;
                }
            });


        return { body: dealershipsList };
        // return { "dealerships": dealershipsList.result };
      } catch (error) {
          return { error: error.description };
      }
}
