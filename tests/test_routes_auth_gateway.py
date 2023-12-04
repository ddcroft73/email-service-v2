#from file_handler import filesys
import requests
import json
from jose import jwt
from pydantic import BaseModel, EmailStr, ValidationError
from datetime import datetime
from typing import Optional, Union, Any
from time import sleep
from tabulate import tabulate
from rich import print

API_KEY: str="9c45916c4f693993bca945b0005f37f5f5246b4491f2fe8e484c8fd7178da103"
#BASE_URL: str = 'http://web:8000/api/v1/' # Must use this address from within containers.

#BASE_URL: str = 'http://localhost:8015/api/v1/'
BASE_URL: str = 'http://192.168.12.189:8015/api/v1/' #server on desktop

current_time: str = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

# The foowing classes represent the way the endpoints expect the request to be prepared.
class UserCreate(BaseModel):
    email: EmailStr = "life.package.web@gmail.com"
    password: str = "password.testing"
    is_superuser: bool = True
    full_name: Optional[str]  = "Danny Account Tester 2"
    phone_number: Optional[str] = "8439260677"
    cell_provider: Optional[str] = "AT&T"

class AccountCreate(BaseModel):
    creation_date:  Union[datetime, str, None] = current_time
    subscription_type: str = 'super user'
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




def get_user(user_id: int, superuser_token):

    url = f"{BASE_URL}users/{user_id}"
    headers = {
        'Authorization': f'Bearer {superuser_token}',
        'Content-Type': 'application/json'
    }
    
    admin_token = ""
    url = url+f"?admin_token={admin_token}"

    response = requests.get(url, headers=headers)
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
        "use_2FA": True
    }

    headers = {
        'Authorization': f'Bearer {my_token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, json=update_data)  
    return response.json()



def get_by_email(email: str, admin_token: str, superuser_token) -> UserAccount:
    
    url = f"{BASE_URL}users/user-by/{email}"
    
    headers = {
        'Authorization': f'Bearer {superuser_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "admin_token" : admin_token
    }
    
    response = requests.get(url, headers=headers,json=payload)

    if 'detail' in response.json():
        msg = f"HTTPException raised: {response.json()['detail']}"
        return msg
    
    return response.json()


def delete_user(email: str, admin_token: str, superuser_token):
    '''
     Delete a user by email addy. Must be a superuser to do this.
    '''
    def remove_user(user_id: int) -> str:
        url = f"{BASE_URL}users/delete/{user_id}"
        headers = {
            'Authorization': f'Bearer {superuser_token}',  # SuperUser Bearer Token
            'Content-Type': 'application/json'
        }

        ad_token = {
            "admin_token": admin_token
        }

        response = requests.delete(url, headers=headers, json=ad_token)

        return response.json()    

    data = get_by_email(email=email, admin_token="", superuser_token=superuser_token)
    
    try:
        if (data["user"]):
            response = remove_user(data["account"]["user_id"])    

    except (TypeError):
        response = f"User: {email} was already deleted."

    return response


def is_superuser(token: str, actual_su_token: str, verbose: bool=True) -> str:     
    def _is_superuser(token: str) -> str:
        _token = jwt.decode(
            token, 
            API_KEY, 
            algorithms=["HS256"]
        )
        return _token    
     
    token_info = _is_superuser(token)    
    user: dict[str] = get_user(token_info["sub"], actual_su_token)
    
    is_su = True if token_info["user_role"] == "admin" else False

    if verbose:    
        resp_msg: str = f'\nUser Name: {user["user"]["email"]}\nis_superuser: {is_su}\n'
    else:
        resp_msg: bool = is_su


    return resp_msg
    
    

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
    

def get_all_emails(admin_token: str, superuser_token: str, is_list: bool=False) -> list[str]:
    data = get_all_users(superuser_token=superuser_token)     
    
    try:
        if is_list:
            res = [user["user"]["email"] for user in data]
        else:
            res = "\n".join([user["user"]["email"] for user in data]) 
        
        return res       
    
    except:        
        return "No records."



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
            "contact_method_2FA": "email",
            "use_2FA": True
        },
        "admin_token": "admin_token"
    } 
    
    response = requests.put(url, headers=headers, json=update_data_dict)  
    return response.json()


def delete_ALL(admin_token: str, superuser_token: str) -> str:
    '''
        Get a list of all the users email addresses, delete all users by email

    '''
    warn: str = "This will delete all the records in the database. \nContinue [y/n] "
    cont = input(warn)
    if cont in ['y', 'Y']:
        emails: list = get_all_emails(admin_token=admin_token, superuser_token=superuser_token, is_list=True)
        
        if len(emails) > 0:
            for email in emails:
                msg = delete_user(email, admin_token=admin_token, superuser_token=superuser_token) 
                print(msg)
                sleep(2)
        else:
            print("No records found")        
    else:
        print("Action aborted by user.")   


def get_user_test_data(su_token: str):
    """organize the reletive parts I need for testing of each user."""
    all_users: list[str] = get_all_users(su_token)     
    users_data_list: list[dict] = []

    for user in all_users:        

        user_atts: dict[str,Union[bool,str]] = {
            "email": user['user']['email'],
            "id": user["account"]["user_id"],
            "enable_2fa": user["account"]["use_2FA"],
            "is_verified": user["user"]["is_verified"],
            "logged_in": user['user']["is_loggedin"]
        }
        users_data_list.append(user_atts)  
        
    users_tabular_data: list[int][Union[str, bool, int]]  = [  
      [ 'User/Email:', 'User ID:', '2FA Enabled:', 'Verified:','Logged in:'],                        
    ]
    # make a list of the key names to get each users data
    keys: list[str] = 'email id enable_2fa is_verified logged_in'.split(" ")

    for user in users_data_list:
        inner_list = []        
        for key in keys:
            inner_list.append(user[key])                         
        users_tabular_data.append(inner_list)   
     
    print(f'\n{tabulate(users_tabular_data, headers="firstrow")}\n')




# add the user create data to the instance of the Object
user_instance = UserCreate()
account_instance = AccountCreate()
user_account_instance = UserAccount(user_in=user_instance, account_in=account_instance).dict()
#print(user_account_instance)


token_super: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDIxNjUyMzQsInN1YiI6IjI5IiwidXNlcl9yb2xlIjoiYWRtaW4iLCJjcmVhdGlvbl9kYXRlIjoiMTIvMDIvMjAyMyAxODo0MDozNCJ9.vstB2AWdXthw0EMsBKd_XswL3Z3c87pj-bGLdO-vhVY'
token_DANNY_super: str = ''
timed_Danny_reggae: str = ''
# alias login
get_token: callable = login

'''Write a request to get a timed token for a particular person.'''

#print(get_by_email(email="croftdanny1973@gmail.com", token="eat a dick", superuser_token=token_super))
#print(update_me(timed_Danny_reggae))

#create_user(full_name="su life.package.account")

#
#print(get_all_users(token_super))
#print(len(get_all_users(token_super)))
#print(json.dumps(get_all_users(token_super)))
#print(update_user(31, token_super))
#print(get_me())
#print(get_user(10, token_super))
#print(get_token(user_id="ddc.dev.python@gmail.com", password="password", verbose=False))
#print(delete_user(email="skippydo@mail.net", admin_token="", superuser_token=token_super))
#print(logout_user(40))

#print(is_superuser(token=token_super, actual_su_token=token_super))

#print('\n'+ get_all_emails(admin_token="", superuser_token=token_super))

#delete_ALL(admin_token="", superuser_token=token_super)

get_user_test_data(su_token=token_super)