import json


from DatabaseDAO import DatabaseDAO, dao
from JSONEncoder import JSONEncoder


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    # context["callbackWaitsForEmptyEventLoop"] = "false"

    global dao
    # global count

    body = json.loads(event["body"])

    dao.connectToDatabase()
    count = -1

    try:
        input = body["text"]
    except:
        input = "error"





    return {
        "statusCode": 200,
        "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": "true"
                    },
        "body": json.dumps({
            # "message": "hello world",
            "input": input,
            # "event": parameters["type"],
            "count": count
            # "location": ip.text.replace("\n", "")
        }),
    }