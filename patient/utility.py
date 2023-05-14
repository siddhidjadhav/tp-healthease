import re

def check_if_user_is_patient(user):
    user_email = user.email
    user_details = dict()
    user_details['is_user_patient'] = True
    user_details['user_identity'] = ""
    if not re.match(".@gmail.com$", user_email):
        if re.search(".@healthease.com$", user_email):
            user_details['is_user_patient'] = False
            user_details['user_identity'] = "doctor_dashboard"
    
    return user_details