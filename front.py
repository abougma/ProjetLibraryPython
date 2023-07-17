import requests
import getpass

def main():
    while True:
        print("----------Menu--------")
        print("1. Listing the books")
        print("2. Getting a book")
        print("3. Creating a book")
        print("4. Deleting a book")
        print("5. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_user()
            list_books()   
        elif choice == "2":
            create_user()
            get_book()
        elif choice == "3":
            create_book()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

def create_user():
    name = input("Enter your name : ")
    password = getpass.getpass("Enter your password : ")

    response = requests.post("http://127.0.0.1:8000/users", json={"pseudo" : name, "password": password})

    if response.status_code == 201:
        print("Name : ",name)
    else:
        print("The name already exists")    


def create_book():
    name = input("Enter name: ")
    release_date = input("Enter release date: ")
    author_name = input("Enter author name: ")
    number_of_pages = input("Enter number of pages: ")

    response = requests.post("http://127.0.0.1:8000/books/", json={"name": name, "release_date": release_date, " author_name": author_name, "number_of_pages": number_of_pages})
    
    if response.status_code == 201:
        print("Book created successfully")
    else:
        print("Error")


def list_books():
    response = requests.get("http://127.0.0.1:8000/books")
    if response.status_code == 200:
        books = response.json()["Reponse"]
        for book in books:
            bookInf = f"""
            Name: {book['Name']}
            Author: {book['Author name']}
            Date: {book['Release date']}
            Number of pages: {book['Number of pages']}
            """
            print(bookInf)
    else:
        print("Error")

def get_book():
    id_book = input("Enter book Id: ")
    response = requests.get(f"http://127.0.0.1:8000/books/{id_book}")
    if response.status_code == 200:
        book = response.json()
        bookInf = f"""
        Name: {book['Name']}
        Author: {book['Author name']}
        Date: {book['Release date']}
        Number of pages: {book['Number of pages']}
        """
        print(bookInf)
    else:
        print("Error")

def delete_book():
    id_book = input("Enter book Id: ")
    response = requests.delete(f"http://127.0.0.1:8000/books/{id_book}")
    if response.status_code == 200:
        print("Book deleted")
    else:
        print("Error")

if __name__ == "__main__":
    main()
