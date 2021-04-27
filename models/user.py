import datetime

class User():
    def __init__(self, first_name, last_name, display_name, user_name, password, email, bio, created_on, active = True, profile_image_url = "", is_admin = False):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = self.setFullName
        self.display_name = display_name
        self.username = user_name 
        self.email = email
        self.password = password
        self.bio = bio
        self.created_on = created_on
        self.active = bool(active)
        self.profile_image_url = profile_image_url
        self.is_admin = bool(is_admin)

    @property
    def setFullName(self):
        return f'{self.first_name} {self.last_name}'