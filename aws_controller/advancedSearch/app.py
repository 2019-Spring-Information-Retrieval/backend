import json

from DatabaseDAO import DatabaseDAO, dao
from JSONEncoder import JSONEncoder

count = -1

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


    # Globasl conn
    global dao
    # global count
    global count

    count = count + 1
    body = json.loads(event["body"])
    dao.connectToDatabase()
    movies = []
    output = ""
  
    try:
        input = body["text"]
        movies = dao.advancedSearch(input)
    except:
        output = "error"

    movies = JSONEncoder().encode(movies)




    return {
        "statusCode": 200,
        "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": "true"
                    },
        "body": json.dumps({
            # "message": "hello world",
            "input": input,
            "movies": movies,
            "output": output,
            # "event": parameters["type"],
            "count": count
            # "location": ip.text.replace("\n", "")
        }),
    }