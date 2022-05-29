class Book:
    def __init__(self, id, authorId, title, genre, pages):
        self.id = int(id)
        self.authorId = int(authorId)
        self.title = title
        self.genre = genre
        self.pages = int(pages)