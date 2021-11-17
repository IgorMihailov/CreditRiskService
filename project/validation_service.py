import requests

def is_passport_valid(passport):
    url = get_url(passport)
    response = requests.get(url)
    data = response.json()

    return not data['foundInExpiredPassports']

def get_url(passport):
    first_part = passport[0:4]
    second_part = passport[-6:]
    url = "http://localhost:8000/expired-passports/series/" + first_part + "/numbers/" + second_part
    return url

def check_length(passport):
    if len(passport) != 10:
        return False
    else:
        return True
