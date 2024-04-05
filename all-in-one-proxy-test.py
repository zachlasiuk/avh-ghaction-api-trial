import os,sys
import requests

def get_token():
    token = os.environ.get("AVH_TOKEN")
    if token is None:
        print("ERROR: AVH_TOKEN environmental var isn't set. Please set it and try again.")
        sys.exit(1)
    else:
        print("INFO: Token found.")
    return token


def lambda_connect(auth_token):
    print('INFO: Connecting to avh-proxy-hello-world function')

    api_endpoint = "https://gseyg7w2noryoser43ofo7cexu0wwiqb.lambda-url.us-east-1.on.aws/"
    headers = {'AVH_AUTHORIZATION_TOKEN': auth_token, 'Content-type': 'application/json'}
    querystring = {'myCustomParameter': 'squirrel'}
    body = {"greeter": "Zach"}

    # Call the API
    response = requests.post(url=api_endpoint, params=querystring, data=body, headers=headers)
    return response.status_code, response.headers, response.text


if __name__ == "__main__":
    
    auth_token = get_token()
    status, headers, body = lambda_connect(auth_token)

    if status == 200:
        print('INFO: 200 response from server')
        print('INFO: Server reply: ')
        print(headers)
        print(body)
    else:
        print('ERROR: Non-200 response from server. See below for details.')
        print(status)
        print(headers)
        print(body)
        sys.exit(1)


    print('')
