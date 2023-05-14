import re

def check_if_user_is_doctor(user):
    user_email = user.email
    user_details = dict()
    user_details['is_user_doctor'] = True
    user_details['user_identity'] = ""
    if not re.match(".@healthease.com$", user_email):
        if re.search(".@gmail.com$", user_email):
            is_user_doctor = False
            user_identity = "patient_dashboard"
            user_details['is_user_doctor'] = is_user_doctor
            user_details['user_identity'] = user_identity
        
    
    return user_details

