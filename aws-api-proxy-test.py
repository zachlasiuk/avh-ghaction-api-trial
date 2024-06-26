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

    api_endpoint = "https://m7qcvig326.execute-api.us-east-1.amazonaws.com/test-1/helloworld"
    headers = {"Authorization": auth_token}
    body = {"greeter": "Zach"}

    # Call the API
    response = requests.post(api_endpoint, headers=headers, json=body)
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
