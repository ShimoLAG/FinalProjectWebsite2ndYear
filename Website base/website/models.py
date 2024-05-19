from flask_login import UserMixin
from flask_login import LoginManager



class users(UserMixin):
    def __init__(self, accountID, firstName, lastName, Dyear, month, day, sex, email, password):
        self.accountID = accountID
        self.firstName = firstName
        self.lastName = lastName
        self.Dyear = Dyear
        self.month = month
        self.day = day
        self.sex = sex
        self.email = email
        self.password = password

    def get_id(self):
        return self.accountID
    

