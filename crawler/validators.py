import re


def email_validator(email):
    # this function validates the email address using regex
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    if re.match(pattern, email):
        return True
    return False

