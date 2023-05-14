import re

def get_user_identity(user):
    user_email = user.email
    user_identity = "patient_dashboard"
    if re.search(".@gmail.com$", user_email):
        user_identity = "patient_dashboard"
        return user_identity
    elif re.search(".@healthease.com$", user_email):
        user_identity = "doctor_dashboard"
        return user_identity
    elif re.search(".insurance.com$", user_email):
        user_identity = "insurance_dashboard"
        return user_identity

        
    return user_identity