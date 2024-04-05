import requests

# Replace these variables with your actual endpoint and token
api_endpoint = "https://m7qcvig326.execute-api.us-east-1.amazonaws.com/test-1/helloworld"
# Manual token testing not published to github
with open('token.txt', 'r') as file:
    token = file.read()

headers = {
    "Authorization": token,
}

response = requests.post(api_endpoint, headers=headers, json={"greeter": "Zach"})

print("Status Code:", response.status_code)
print("Response Body:", response.text)
