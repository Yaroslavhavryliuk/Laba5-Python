from library import Library
import pika


def RunServer (clientMessage, library):
	command = int(clientMessage[0])
	if command == 1:
		result = library.loadFromDB()
	elif command == 2:
		authorName = clientMessage[1]
		result = library.addAuthor(authorName)
	elif command == 3:
		authorId = int(clientMessage[1])
		bookTitle = clientMessage[2]
		bookGenre = clientMessage[3]
		bookPages = int(clientMessage[4])
		result = library.addBook(authorId, bookTitle, bookGenre, bookPages)
	elif command == 4:
		authorId = int(clientMessage[1])
		authorName = clientMessage[2]
		result = library.editAuthor(authorId, authorName)
	elif command == 5:
		bookId = int(clientMessage[1])
		action = int(clientMessage[2])
		if action == 1:
			bookTitle = clientMessage[3]
			result = library.editBook(bookId, action, bookTitle)
		elif action == 2:
			bookGenre = clientMessage[3]
			result = library.editBook(bookId, action, bookGenre)
		elif action == 3:
			bookPages = int(clientMessage[3])
			result = library.editBook(bookId, action, bookPages)
		else:
			newData = 'falseAction'
			result = library.editBook(bookId, action, newData)
	elif command == 6:
		authorId = int(clientMessage[1])
		result = library.deleteAuthor(authorId)
	elif command == 7:
		bookId = int(clientMessage[1])
		result = library.deleteBook(bookId)
	elif command == 8:
		authorId = int(clientMessage[1])
		result = library.getAuthor(authorId, True)
	elif command == 9:
		bookId = int(clientMessage[1])
		result = library.getBook(bookId, True)
	elif command == 10:
		result = library.printAllAuthors()
	elif command == 11:
		result = library.getBooksNumber()
	elif command == 12:
		result = library.printAllBooks()
	elif command == 13:
		authorId = int(clientMessage[1])
		result = library.printAllBooksOfAuthor(authorId)
	elif command == 14:
		exit()
	else:
		result = 'R#Unknown command'
	return result


def callback(body):
	print('Receive query', body.decode())
	library = Library()
	response = RunServer(body.decode().split('|'), library)
	channel.basic_publish(exchange='', routing_key='client_queue', body=response)


if __name__ == '__main__':
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='server_queue')
	channel.queue_declare(queue='client_queue')
	print('Server started...')

	try:
		# time.sleep(15)
		channel.basic_consume(queue='server_queue', on_message_callback=callback, auto_ack=True)
		channel.start_consuming()
	except KeyboardInterrupt:
		print('Server stopped')
		connection.close()

