class Post():

    def __init__(self, id, user_id, category_id, title, publication_date, image_url = "", content = "", approved = True):
        self.id = id
        self.userId = user_id
        self.categoryId = category_id
        self.title = title
        self.publicationDate = publication_date
        self.imageUrl = image_url
        self.content = content
        self.approved = bool(approved)
        self.tags = None
        self.comments = None
        self.user = None
        self.category = None