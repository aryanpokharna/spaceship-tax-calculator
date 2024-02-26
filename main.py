from requests_handler import post
from request import request_json, header_json, update_request, update_header
from credentials import Credentials
from calculator import report

import json

# File Path
response_file = 'response.json'

# Credentials
EMAIL = "email@email.com" # add username here
PASSWORD = "password" # add password here

def login():
    # Instantiate Credentials
    credentials = Credentials(EMAIL, PASSWORD)
    update_request(credentials)

    # Pre MFA Login
    response_pre_mfa = post(payload=request_json("login_pre_mfa"))
    id = response_pre_mfa["data"]["login"]["mfaChallenge"]["id"]
    credentials.update_user_id(id)
    update_request(credentials)

    # Post MFA Login
    mfa = input("Enter MFA Code: ")
    credentials.update_mfa_code(mfa)
    update_request(credentials)
    response_post_mfa = post(payload=request_json("login_post_mfa"))
    auth_token = response_post_mfa["data"]["login"]["auth"]["authToken"]
    credentials.update_auth_token(auth_token)

    # Transaction Data
    update_header(credentials)
    transaction_data = post(payload=request_json("transaction"), headers=header_json("header"))
    with open(response_file, 'w') as f:
        json.dump(transaction_data, f, indent=4)
    
    # Logout
    response_post_logout = post(payload=request_json("logout"))
    

def tax_calculate():
    report()

def main():
    log = input("Would you like to login and pull fresh data? [Y/N] ").upper()
    if log == "Y":
        login()
    tax = input("Would you like to calculate taxes? [Y/N] ").upper()
    if tax == "Y":
        tax_calculate()
    print("Exited")

main()