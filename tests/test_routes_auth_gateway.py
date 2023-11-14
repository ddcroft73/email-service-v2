#from file_handler import filesys
import requests
import json
from jose import jwt
from pydantic import BaseModel, EmailStr, ValidationError
from datetime import datetime
from typing import Optional, Union, Any

#BASE_URL: str = 'http://web:8000/api/v1/' # Must use this address from within containers.

BASE_URL: str = 'http://localhost:8015/api/v1/'

current_time: str = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

# The foowing classes represent the way the endpoints expect the request to be prepared.
class UserCreate(BaseModel):
    email: EmailStr = "croftdavid73@gmail.com"
    password: str = "password.testing"
    is_superuser: bool = True
    full_name: Optional[str]  = "Danny Account Tester 2"
    phone_number: Optional[str] = "8439260677"
    cell_provider: Optional[str] = "AT&T"

class AccountCreate(BaseModel):
    creation_date:  Union[datetime, str, None] = current_time
    subscription_type: str = 'premium'
    last_login_date:  Union[datetime, str, None] = None
    # Used to get acces to the endpoints that can be used to alter any user on the system.
    admin_PIN: Optional[str] = "111111"  

    bill_renew_date:  Union[datetime, str, None] = current_time
    auto_bill_renewal: bool = False

    cancellation_date:  Union[datetime, str, None] = None
    cancellation_reason: Optional[str] = None

    last_update_date: Union[datetime, str, None] = current_time
    preferred_contact_method: Optional[str] = 'email'
    account_locked: Optional[bool] = False
    account_locked_reason: Optional[str] = None 
    timezone: Optional[str] = "Eastern Standard"
    
    use_2FA: bool = True
    contact_method_2FA: Optional[str] = "email"
    cell_provider_2FA: Optional[str] = "AT&T"


class UserAccount(BaseModel):
    user_in: UserCreate
    account_in: AccountCreate

class CreateUser(BaseModel):
    email: str = None
    password: str = None
    full_name: str = None
    phone_number: str = None
    is_verified: bool = True



class UpdateUserMe(BaseModel):
    email: str = None
    password: str = None
    full_name: str = None
    phone_number: str = None
    is_verified: bool = True
    account_locked: bool = False
    failed_attempts: int = 0    


#Login and get token
def login(user_id: str, password: str, verbose: bool=True):
    url = f"{BASE_URL}auth/login/access-token"

    payload = {
        "username": user_id,
        "password": password,
    }
    response = requests.post(url, data=payload)


    if response.status_code == 200:

        token_info = response.json()
        
        # handle 2FA response
        if "code" in token_info:
            print(f'2FA Code: {token_info["code"]} \n2FA Timed Token: {token_info["token"]}')
            
        elif 'access_token' in token_info:
            access_token = token_info['access_token']
            if verbose: 
                print("Access token:", access_token)
            return access_token
    else:
       if verbose: print("Failed to authenticate:", response.text)
    
def create_user():
    url = f"{BASE_URL}users/registration"

    user_instance = UserCreate()
    account_instance = AccountCreate()
    user_account_instance = UserAccount(user_in=user_instance, account_in=account_instance)

    response = requests.post(url, json=user_account_instance.dict())

    if response.status_code == 200:
        print("\nUser registered successfully!\n")
        print(response.json())

    else:
        print(f"Failed to register user. Status code: {response.status_code}")
        print(response.text)


def update_user(user_id: int, superuser_token: str):
    '''
     SuperUser function to update a user.
    '''
    url = f"{BASE_URL}users/update/{user_id}"
    headers = {
        'Authorization': f'Bearer {superuser_token}',  # SuperUser Bearer Token
        'Content-Type': 'application/json'
    }

    update_data_dict = {
        "user_in": {
            "phone_number": "800-556-1212",
            "cell_provider": "AT&T"
        },
        "account_in": {
            "user_id": user_id,
            "cell_provider_2FA" : "REdundant, delete this field",
            "contact_method_2FA": "cell",
            "use_2FA": False
        },
        "admin_token": "admin_token"
    }


    response = requests.put(url, headers=headers, json=update_data_dict)

    return response.json()


def get_user(user_id: int, superuser_token):

    url = f"{BASE_URL}users/{user_id}"
    headers = {
        'Authorization': f'Bearer {superuser_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    return response.json()

def delete_user(user_id: int, superuser_token):
    '''
     Delete a user by id. Must be a superuser to do this.
    '''
    url = f"{BASE_URL}users/delete/{user_id}"
    headers = {
        'Authorization': f'Bearer {superuser_token}',  # SuperUser Bearer Token
        'Content-Type': 'application/json'
    }

    admin_token = {
        "admin_token": "Token"
    }

    response = requests.delete(url, headers=headers, json=admin_token)

    return response.json()

def logout_user(user_id: int): 
    url = f"{BASE_URL}auth/logout/{user_id}"

    headers = {
        'Authorization': f'Bearer {login(user_id="ddc.dev.python@gmail.com", password="password", verbose=False)}',  # SuperUser Bearer Token
        'Content-Type': 'application/json'
    }
    
    admin_token = {
        "admin_token": "Token"
    }
    response = requests.put(url, headers=headers, json=admin_token)

    return response.json()


def get_all_users(superuser_token: str):
    '''
    Superuser to get all users

    '''
    url = f"{BASE_URL}users"

    headers = {
        'Authorization': f'Bearer {superuser_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    return response.json()



def get_me(username: str="ddc.dev.python@gmail.com", password: str="password"):
    url = f"{BASE_URL}users/me"

    headers = {
        'Authorization': f'Bearer {login(user_id=username, password=password, verbose=False)}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    return response.json()

def update_me(my_token: str) -> dict:
    url = f"{BASE_URL}users/me"

    update_data = {        
        "full_name": "David D Croft, Jr.",
        "phone_number": "843-926-0677",
        "cell_provider": "AT&T",
        "cell_provider_2FA": "AT&T",
        "use_2FA": False
    }

    headers = {
        'Authorization': f'Bearer {my_token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, json=update_data)  
    return response.json()



def get_2FA_code():
    '''
       hits the endpoint that ges the code, retiurns code. 
    '''
    url = f"{BASE_URL}auth/2FA/get-2FA-code/" 
    payload = {
        "email_account": "email@account.com"
    }
    response = requests.get(url+payload["email_account"])
    return response.json()

def is_superuser(email: EmailStr):

    pass

def verify_2FA(user_input_code: str, code_2FA: str, email: EmailStr, timed_token: str):

    url = f"{BASE_URL}auth/2FA/verify-2FA-code/" 
    payload = {
        "code_2FA": code_2FA,
        "code_user": user_input_code,
        "email_account": email,
        "timed_token": timed_token
    }    
    response = requests.put(url, json=payload)
    # response will be a token if all is good!
    return response.json()
    
def get_by_email(email: str, token: str, superuser_token) -> UserAccount:
    
    url = f"{BASE_URL}users/user-by/{email}"
    
    headers = {
        'Authorization': f'Bearer {superuser_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "admin_token" : token
    }
    
    response = requests.get(url, headers=headers,json=payload)
    if 'detail' in response.json():
        msg = f"HTTPException raised: {response.json()['detail']}"
        return msg
    
    return response.json()

user_instance = UserCreate()
account_instance = AccountCreate()
user_account_instance = UserAccount(user_in=user_instance, account_in=account_instance).dict()

#print(user_account_instance)
token_super: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDAzNDgzOTEsInN1YiI6IjEwIiwidXNlcl9yb2xlIjoiYWRtaW4iLCJjcmVhdGlvbl9kYXRlIjoiMTEvMTEvMjAyMyJ9.rD9MMA7lIIYtKrnTJRA9LmBopSgdsnbt6vdAxGmyC9g'
token_DANNY_super: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDAzNDg0ODgsInN1YiI6IjIiLCJ1c2VyX3JvbGUiOiJhZG1pbiIsImNyZWF0aW9uX2RhdGUiOiIxMS8xMS8yMDIzIn0.N5Cv4htSk_9YgXl2wkM0h0R4f6zzC2R5iR5-QHzJSZI'
timed_DAVID_10minutes: str = ''

'''Write a request to get a timed token for a particular person.'''
#print(get_by_email(email="croftdavid73@gmail.com", token="eat a dick", superuser_token=token_DANNY_super))
#print(update_me(token_DANNY_super))

#create_user()

#print(len(get_all_users(token_super)))
#print(update_user(8, token_DANNY_super))
#print(get_me("user_number_06@email.com", "password"))
#print(get_user(4, token_DANNY_super))
print(login(user_id="life.package.web@gmail.com", password="password.testing", verbose=True))
#print(delete_user(4, token_super))
#print(logout_user(4))

#print(is_superuser())
#print(verify_2FA("VZM-IZJ"))  