import secrets
secure_token = secrets.token_hex(64*2)
print(secure_token)
