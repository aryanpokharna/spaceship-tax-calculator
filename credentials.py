# Add username and password in main.py, not here.

class Credentials:
    def __init__(self, email, password):
        self.email= email
        self.password = password
        self.user_id = None
        self.mfa_code = None
        self.auth_token = None
        self.bearer = None

    def update_email(self, email):
        self.email = email

    def update_password(self, password):
        self.password = password

    def update_user_id(self, user_id):
        self.user_id = user_id

    def update_mfa_code(self, mfa_code):
        self.mfa_code = mfa_code

    def update_auth_token(self, auth_token):
        self.auth_token = auth_token
        self.bearer = "Bearer " + auth_token