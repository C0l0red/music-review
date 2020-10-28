from flask import url_for

def send_email(email, msg):
    pass
"""
def reset_email(user):
    token = user.create_token()
    msg = f"{user}, please reset your password using this link, {url_for("auth.reset_password", token=token, external=True)}"
    email = user.email

    send_email(email, msg)
"""