import requests
import time
import re

def generate_random_email():
    url = "https://www.1secmail.com/api/v1/"
    params = {
        "action": "genRandomMailbox",
        "count": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()[0]
    else:
        print("Failed to generate email")
        return None

def save_email(email):
    with open("acc.txt", "a") as file:
        file.write(email + "\n")

def get_inbox(login, domain):
    url = f"https://www.1secmail.com/api/v1/"
    params = {
        "action": "getMessages",
        "login": login,
        "domain": domain
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get inbox. Status code: {response.status_code}")
        return None

def read_message(login, domain, message_id):
    url = f"https://www.1secmail.com/api/v1/"
    params = {
        "action": "readMessage",
        "login": login,
        "domain": domain,
        "id": message_id
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to read message. Status code: {response.status_code}")
        return None

def auto_register(email, ref):
    url = "https://api.attarius.com/auth/sendBlockchainUserOTP"
    
    payload = {
        "email": email
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        print("OTP sent successfully!")
        return response.json()
    elif response.status_code == 400:
        error_response = response.json()
        if "errors" in error_response and "email" in error_response["errors"]:
            print("Error:", error_response["errors"]["email"])
        else:
            print("Failed to send OTP. Status code: 400")
        return error_response
    else:
        print(f"Failed to send OTP. Status code: {response.status_code}")
        return response.text

def verify_account(email, otp, ref):
    url = "https://api.attarius.com/auth/verifyBlockchainUserOTP"
    
    payload = {
        "email": email,
        "otp": otp,
        "ref": ref
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        print("Account verified successfully!")
        return response.json()
    else:
        print(f"Failed to verify account. Status code: {response.status_code}")
        return response.text

if __name__ == "__main__":
    num_accounts = int(input("Bearapa Akun?: "))
    ref_code = input("Reff code: ")
    
    for _ in range(num_accounts):
        email = generate_random_email()
        if email:
            print(f"Generated email: {email}")
            save_email(email)
            
            # Register using the generated email
            register_response = auto_register(email, ref_code)
            print(register_response)
            
            # Extract login and domain from the email
            login, domain = email.split('@')
            
            # Give some time for the email to arrive
            time.sleep(10)
            
            # Retrieve the inbox for the generated email
            inbox = get_inbox(login, domain)
            print("Inbox messages:", inbox)
            
            if inbox and len(inbox) > 0:
                # Get the ID of the first message in the inbox
                message_id = inbox[0]['id']
                
                # Read the first message
                message = read_message(login, domain, message_id)
                # print("Message details:", message)
                
                # Extract OTP from the message body (assuming OTP format is CGV-JJ0)
                otp_match = re.search(r'\b[A-Z0-9]{3}-[A-Z0-9]{3}\b', message['body'])
                if otp_match:
                    otp = otp_match.group(0)
                    
                    # Verify the account using the extracted OTP
                    verify_response = verify_account(email, otp, ref_code)
                    print("Verification response:", verify_response)
                else:
                    print("OTP not found in the email.")
            else:
                print("Inbox is empty.")
        else:
            print("Could not generate a random email")
