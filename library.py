import sqlite3
from author import Author
from book import Book



class Library:
    def __init__(self):
        self.authors = dict()
        self.books = dict()
        self.isDataLoad = False

        dbFile = 'library.sqlite'
        self.db = sqlite3.connect(dbFile)
        self.cursor = self.db.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Authors ( id INTEGER , name TEXT );')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Books ( id INTEGER , author_id INTEGER, title TEXT, genre TEXT, pages INTEGER );')

    def clean(self):
        self.authors = dict()
        self.books = dict()

    def printData(self):
        try:
            ret = 'Y#'
            self.cursor.execute('SELECT id, name FROM Authors')
            results = self.cursor.fetchall()
            for row in results:
                authorId = row[0]
                authorName = row[1]
                ret = ret + "Author id: " + str(authorId) + ", name: " + authorName + "\n"

            self.cursor.execute('SELECT * FROM Books')
            results = self.cursor.fetchall()
            for row in results:
                bookId = row[0]
                author_id = row[1]
                bookTitle = row[2]
                bookGenre = row[3]
                bookPages = row[4]
                ret = ret + "Book id: " + str(bookId) + ", author id: " + str(author_id) + ", title: " + bookTitle + \
                                       ", genre: " + str(bookGenre) + ", pages number: " + str(bookPages) + "\n"
            return ret
        except:
            return 'R#Data recieving ERROR'



    def loadFromDB(self):
        self.clean()

        self.cursor.execute('SELECT * FROM Authors')
        results = self.cursor.fetchall()
        for row in results:
            authorId = row[0]
            authorName = row[1]
            author = Author(authorId, authorName)
            self.authors[authorId] = author

        self.cursor.execute('SELECT * FROM Books')
        results = self.cursor.fetchall()
        for row in results:
            bookId = row[0]
            author_id = row[1]
            bookTitle = row[2]
            bookGenre = row[3]
            bookPages = row[4]
            book = Book(bookId, author_id, bookTitle, bookGenre, bookPages)
            self.books[bookId] = book

        self.isDataLoad = True
        return self.printData()



    def addAuthor(self, authorName):
        if not self.isDataLoad:
            self.loadFromDB()
        if len(self.authors) == 0:
            key = 0
        else:
            key = max(self.authors.keys()) + 1
        newAuthor = Author(key, authorName)
        self.authors[key] = newAuthor


        try:
            self.cursor.execute('INSERT INTO Authors (id, name) VALUES (?, ?)', (newAuthor.id, newAuthor.name))
            self.db.commit()
            return 'G#Author added'
        except:
            self.db.rollback()
            return 'R#Author adding ERROR'



    def addBook(self, author_id, bookTitle, bookGenre, bookPages):
        if not self.isDataLoad:
            self.loadFromDB()
        if not self.getAuthor(author_id, False) == '':
            return 'R#Author does not exist'
        if len(self.books) == 0:
            key = 0
        else:
            key = max(self.books.keys()) + 1
        newBook = Book(key, author_id, bookTitle, bookGenre, bookPages)
        self.books[key] = newBook

        try:
            self.cursor.execute('INSERT INTO Books (id, author_id, title, genre, pages) VALUES (?, ?, ?, ?, ?)',
                (newBook.id, newBook.authorId, newBook.title, newBook.genre, newBook.pages))
            self.db.commit()
            return 'G#Book added'
        except:
            self.db.rollback()
            return 'R#Book adding ERROR'



    def editAuthor(self, authorId, newName):
        if not self.isDataLoad:
            self.loadFromDB()
        if self.getAuthor(authorId, False) == '':
            self.authors[authorId].name = newName
            try:
                self.cursor.execute("UPDATE Authors SET name = '" + newName + "' WHERE id = " + str(authorId))
                self.db.commit()
                return 'G#Author edited'
            except:
                self.db.rollback()
                return 'R#Author editing ERROR'
        else:
            return 'R#Author does not exist'



    def editBook(self, bookId, action, newField):
        if not self.isDataLoad:
            self.loadFromDB()
        if self.getBook(bookId, False) == '':
            if action == 1:
                self.books[bookId].title = newField
                sql_part = "title = '" + newField + "'"
            elif action == 2:
                self.books[bookId].genre = newField
                sql_part = "genre = '" + newField + "'"
            elif action == 3:
                self.books[bookId].pages = newField
                sql_part = "pages = '" + str(newField) + "'"
            else:
                return 'R#Unknown command'
            try:
                self.cursor.execute("UPDATE Books SET " + sql_part + " WHERE id = " + str(bookId))
                self.db.commit()
                return 'G#Book edited'
            except:
                self.db.rollback()
                return 'R#Book editing ERROR'
        else:
            return 'R#Book does not exist'



    def deleteAuthor(self, authorId):
        if not self.isDataLoad:
            self.loadFromDB()
        if self.getAuthor(authorId, False) == '':
            booksIdSet = set()
            for bookId in self.books.keys():
                if self.books[bookId].authorId == authorId:
                    booksIdSet.add(bookId)

            for bookId in booksIdSet:
                self.deleteBook(self.books[bookId].id)
            del self.authors[authorId]

            try:
                self.cursor.execute('DELETE FROM Authors WHERE id = ?', (authorId,))
                self.db.commit()
                return 'G#Author deleted'
            except:
                self.db.rollback()
                return 'R#Author deleting ERROR'
        else:
            return 'R#Author does not exist'



    def deleteBook(self, bookId):
        if not self.isDataLoad:
            self.loadFromDB()
        if self.getBook(bookId, False) == '':
            del self.books[bookId]
            try:
                self.cursor.execute('DELETE FROM Books WHERE id = ?', (bookId,))
                self.db.commit()
                return 'G#Book deleted'
            except:
                self.db.rollback()
                return 'R#Book deleting ERROR'
        else:
            return 'R#Book does not exist'



    def getAuthor(self, authorId, boolToPrint):
        try:
            self.cursor.execute('SELECT * FROM Authors WHERE id = ?', (authorId,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'R#Incorrect id'
            for row in results:
                authorId = row[0]
                authorName = row[1]
                if boolToPrint:
                    return 'Y#Author id: ' + str(authorId) + ', name: ' + authorName + '\n'
                return ''
        except:
            self.db.rollback()
            return 'R#Author getting ERROR'



    def getBook(self, bookId, boolToPrint):
        try:
            self.cursor.execute('SELECT * FROM Books WHERE id = ?', (bookId,))
            results = self.cursor.fetchall()
            if len(results) == 0:
                return 'R#Incorrect id'
            for row in results:
                bookId = row[0]
                author_id = row[1]
                bookTitle = row[2]
                bookGenre = row[3]
                bookPages = row[4]
                if boolToPrint:
                    return "B#Book id: " + str(bookId) + ", author id: " + str(
                        author_id) + ", title: " + bookTitle + ", genre: " + bookGenre + ", pages: " + str(bookPages)
                return ''
        except:
            self.db.rollback()
            return 'R#Book getting ERROR'



    def printAllAuthors(self):
        ret = 'Y#'
        self.cursor.execute('SELECT id, name FROM Authors')
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'R#No authors in DB'

        for row in results:
            authorId = row[0]
            authorName = row[1]
            ret = ret + 'Author id: ' + str(authorId) + ', name: ' + authorName + '\n'
        return ret



    def getBooksNumber(self):
        self.cursor.execute('SELECT count(id) FROM Books')
        return 'B#There are ' + str(self.cursor.fetchone()[0]) + ' books in the DB'



    def printAllBooks(self):
        ret = 'B#'
        self.cursor.execute('SELECT * FROM Books')
        results = self.cursor.fetchall()
        if len(results) == 0:
            return 'R#No books in DB'

        for row in results:
            bookId = row[0]
            self.cursor.execute('SELECT name FROM Authors JOIN Books ON Authors.id = Books.author_id WHERE Books.id = ?', (bookId,))
            authorName = self.cursor.fetchone()[0]
            bookTitle = row[2]
            bookGenre = row[3]
            bookPages = row[4]
            ret = ret + 'Book id: ' + str(bookId) + ", author's name: " + authorName + ", title: " + bookTitle + ", genre: " + bookGenre + ", pages: " + str(bookPages) + '\n'
        return ret



    def printAllBooksOfAuthor(self, authorId):
        ret = self.getAuthor(authorId, True)
        self.cursor.execute('SELECT * FROM Books WHERE author_id = ?', (authorId,))
        results = self.cursor.fetchall()
        if len(results) == 0:
             return 'R#No books of this author in DB'
        for row in results:
            bookId = row[0]
            author_id = row[1]
            bookTitle = row[2]
            bookGenre = row[3]
            bookPages = row[4]
            ret = ret + "Book id: " + str(bookId) + ", author id: " + str(
                    author_id) + ", title: " + bookTitle + ", genre: " + bookGenre + ", pages: " + str(bookPages) + '\n'
        return ret
