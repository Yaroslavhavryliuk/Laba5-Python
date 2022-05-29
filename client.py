from colors import greenText, yellowText, redText, blueText
import pika

def printColor (serverMessage):
    if serverMessage[0] == 'G':
        greenText(serverMessage[1])
    elif serverMessage[0] == 'Y':
        yellowText(serverMessage[1])
    elif serverMessage[0] == 'R':
        redText(serverMessage[1])
    elif serverMessage[0] == 'B':
        blueText(serverMessage[1])
    else:
        redText('Data sending ERROR')


def startConsumer():
    def callback(body):
        serverMessage = body.decode().split('#')
        printColor(serverMessage)
    channel.basic_consume(queue='client_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='client_queue')
    channel.queue_declare(queue='server_queue')

    greenText("1. Recieve answer from server \n" +
              "2. Make a query to a server")
    greenText("Enter a command:")
    choice = int(input())
    if choice == 1:
        startConsumer()
    elif choice == 2:
        while True:
            greenText("1. Load and print data from the DB \n" +
                    "2. Add a new author \n" +
                    "3. Add a new book \n" +
                    "4. Edit an author \n" +
                    "5. Edit a book \n" +
                    "6. Delete an author \n" +
                    "7. Delete a book \n" +
                    "8. Find an author by id \n" +
                    "9. Find a book by id \n" +
                    "10. Print all authors \n" +
                    "11. Get books number \n" +
                    "12. Print all books \n" +
                    "13. Print all books of author \n" +
                    "14. Exit")
            greenText('Enter command:')
            command = int(input())
            query = str(command)

            if command == 1:
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 2:
                greenText("Enter author's name: ")
                name = input()
                query = query + '#' + name
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 3:
                greenText("Enter the author id: ")
                author_id = int(input())
                greenText("Enter the title: ")
                title = input()
                greenText("Enter the genre: ")
                genre = input()
                greenText("Enter the number of pages: ")
                pages = int(input())
                query = query + '#' + str(author_id) + '#' + title + '#' + genre + '#' + str(pages)
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 4:
                greenText("Enter the author id: ")
                authorId = int(input())
                greenText("Enter new author name: ")
                authorName = input()
                query = query + '#' + str(authorId) + '#' + authorName
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 5:
                greenText("Enter the book id: ")
                bookId = int(input())
                greenText("What do you want to edit? \n" +
                            "1. Title \n" +
                            "2. Genre \n" +
                            "3. Pages number")
                choice = int(input())
                if choice == 1:
                    greenText("Enter new title: ")
                    bookTitle = input()
                    query = query + '#' + str(bookId) + '#' + str(choice) + '#' + bookTitle
                elif choice == 2:
                    greenText("Enter new genre: ")
                    bookGenre = input()
                    query = query + '#' + str(bookId) + '#' + str(choice) + '#' + bookGenre
                elif choice == 3:
                    greenText("Enter new number of pages: ")
                    bookPages = int(input())
                    query = query + '#' + str(bookId) + '#' + str(choice) + '#' + str(bookPages)
                else:
                    redText("Unknown command")
                    continue
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 6:
                greenText("Enter the author id: ")
                authorId = int(input())
                query = query + '#' + str(authorId)
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 7:
                greenText("Enter the book id: ")
                bookId = int(input())
                query = query + '#' + str(bookId)
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 8:
                greenText("Enter the author id: ")
                authorId = int(input())
                query = query + '#' + str(authorId)
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 9:
                greenText("Enter the book id: ")
                bookId = int(input())
                query = query + '#' + str(bookId)
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 10:
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 11:
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 12:
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 13:
                greenText("Enter the author id: ")
                authorId = int(input())
                query = query + '#' + str(authorId)
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
            elif command == 14:
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
                exit()
            else:
                channel.basic_publish(exchange='', routing_key='server_queue', body=query)
