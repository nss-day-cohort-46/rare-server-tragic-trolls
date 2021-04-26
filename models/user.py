import datetime

class User():
    def __init__(self, first_name, last_name, user_name, email, bio, created_on, active = True, profile_image_url = ""):
        self.first_name = first_name
        self.last_name = last_name
        # self.display_name
        self.user_name = user_name 
        self.email = email
        self.__password
        self.bio = bio
        self.created_on = created_on
        self.active = active
        self.profile_image_url = profile_image_url

    @property
    def __password(self, password):
        print("Password")
        self.__password = password

    # @property
    # def display_name(self, first_name, last_name):
    #     print("User Name")
    #     self.display_name = f'{first_name} {last_name}'
    