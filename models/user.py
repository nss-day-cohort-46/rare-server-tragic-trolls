import datetime

class User():
    def __init__(self, first_name, last_name, display_name, user_name, password, email, bio, created_on, active = True, profile_image_url = "", is_admin = False):
        self.firstName = first_name
        self.lastName = last_name
        self.fullName = self.setFullName
        self.displayName = display_name
        self.username = user_name 
        self.email = email
        self.password = password
        self.bio = bio
        self.createdOn = created_on
        self.active = bool(active)
        self.profileImageUrl = profile_image_url
        self.isAdmin = bool(is_admin)

    @property
    def setFullName(self):
        return f'{self.firstName} {self.lastName}'