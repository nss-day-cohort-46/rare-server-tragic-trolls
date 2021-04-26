import datetime
class User():
    def __init__(self, first_name, last_name, email, bio, active = True, profile_image_url = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name 
        self.email = email
        self.__password
        self.bio = bio
        self.created_on = datetime.date.today()
        self.active = active
        self.profile_image_url = profile_image_url

    @property
    def __password(self, password):
        print("Password")
        self.__password = password

    @property
    def user_name(self, first_name, last_name):
        print("User Name")
        self.user_name = f'{first_name} {last_name}'