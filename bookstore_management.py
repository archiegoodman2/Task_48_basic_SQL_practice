#add new books - just use sql command insert
#update book info - just use sql command update
#delete books - just use sql command delete
#search for specific book - just use the SELECT FROM and WHERE syntax already in sql: set up a try except structure to handle if it isn't there

import sqlite3
from sqlite3 import Error

conn = sqlite3.connect('books.db')
cur = conn.cursor()

#time to reset our table: 

# Check if the table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
result = cur.fetchone()

# If the table exists, delete it, so we dont get a 'table already exists' error
if result:
    cur.execute("DROP TABLE books")
    print("Table 'books' deleted.")

#first we make sure our previous table does not exist already:


#then we create our table and populate it
conn.executescript('''CREATE TABLE books(id int(4), Title varchar (30), Author varchar(25), Qty int(3), PRIMARY KEY (id));
INSERT INTO books VALUES (3001, "A Tale of Two Cities", 'Charles Dickens', 30);
INSERT INTO books VALUES (3002, "Harry Potter and the Philosopher's Stone", 'JK Rowling', 30);
INSERT INTO books VALUES (3003, "The Lion, the Witch, and the Wardrobe", 'CS Lewis', 30);
INSERT INTO books VALUES (3004, "The Lord of the Rings", 'JRR Tolkein', 30);
INSERT INTO books VALUES (3005, "Alice in Wonderland", 'Lewis Carroll', 30);''')
conn.commit()


#then define our functions


def insert_book(id, name, author, qty):
    #sanitise our inputs:
    id_int = int(id)
    name_str = str(name)
    author_str = str(author)
    qty_int = int(qty)

    #insert into table
    conn.execute('''INSERT INTO books VALUES (?, ?, ?, ?);''', (id_int, name_str, author_str, qty_int))
    conn.commit()

def update_book():

    id_int = int(input('''
    What is the ID of the book you would like to update:
    '''))

    #now we must check if there is a book with this ID, so we simply make a list of the id's and check in there:

    cur.execute('''SELECT id FROM books''')

    # Fetch all the rows
    rows = cur.fetchall()

    id_values = []

    # Add the values to the list
    for row in rows:
        id_values.append(row[0])

    
    #we want to change the details of a book with a given id
    if id_int in id_values:
        choice2 = int(input('''
        Please select which data you would like to update for your given ID:
        [1] - name
        [2] - author
        [3] - quantity
    '''))   

        id_str = str(id_int)

        if choice2 == 1:
            new_name = input("Please enter the new name: ")
            cur.execute('''UPDATE books SET Title = ? WHERE id = ?;''', (new_name, id_str))
            conn.commit()
        elif choice2 == 2:
            new_author = input("Please enter the new author: ")
            cur.execute('''UPDATE books SET Author = ? WHERE id = ?;''', (new_author, id_str))
            conn.commit()
        elif choice == 3:
            new_quantity = input("Please enter the new quantity: ")
            cur.execute('''UPDATE books SET Title = ? WHERE id = ?;''', (new_quantity, id_str))
            conn.commit()
        else:
            print("Please enter one of the three menu options.")
    else:
        print("Error: ID not found. Please try again. ")

def list_all():
    
    #assume this works: fix later
    cur.execute('''SELECT * FROM books''')
    output = cur.fetchall()
    for row in output:
        print(row)
        
    conn.commit()

#then we define our while True loop for our interface 
 
def delete_book():
    #plan: allow them to search for a book title, and delete
    try:
        target = input("Please enter the id of the book you would like to delete: ")
        conn.execute('''DELETE FROM books WHERE id = ?;''', (target,))                    #annoyingly, this function takes a tuple as an input: so we need that comma to make it a tuple
        print('Any book present on the database with id: ' + target + ' has now been deleted from the database.')

    except sqlite3.OperationalError as e:
        print(e + ' Book may not be present on database, check list and try again.')
        #i think this is the errorname that sqlite3 throws when you search for a title that isnt there

def search_for():
    #allow users to enter a title, then print all info about it: maybe allow them to change info?? why not, its easy

    target = input("Please enter the name of the book for which you would like to search: ").strip(" ")  
    
    cur.execute('''SELECT * FROM books''')
    output = cur.fetchall()
    rows = []
    for row in output:
        rows.append(row)

    #this variable will be set to True if we get a hit for our search query:
    hit = False


    #-----[THERE IS DEFINITELY A BETTER WAY TO DO THIS, USING THE SELECT FROM books WHERE Title = ? SYNTAX, PLEASE LET ME KNOW]-----

    #now we should have a list of tuples, where each row is a tuple
    #iterate through list of rows:
    for x in range(0, len(rows)):   
        #now we iterature through each row itself
        for y in range(0, len(rows[x])):
            if rows[x][y] == target:
                hit = True
                result_details = str(rows[x])
        
    if hit == True:
        print('''
Book found, with the ID, Name, Author and Quantity of: ''' + result_details + ''' respectively.
        ''')
    else:
        print("Book not found.")
    conn.commit()
    
    

while True:
    
    choice = int(input('''
    WELCOME TO THE BOOKSTORE INVENTORY MANAGEMENT SYSTEM

    Please enter the name of the option you would like to select:
    [1] - Enter book
    [2] - Update the details of a book with a given ID
    [3] - Delete a book
    [4] - Search for a book by name
    [5] - List all books on record
    [0] - Exit the program

    '''))

    
    if choice == 1:
        #ask for id, name, author, qty
        id = input('''Please enter the id of the book you would like to record: 
        ''')
        name = input('''Please enter the name of the book you would like to record: 
        ''')
        author = input('''Please enter the author of the book you would like to record: 
        ''')
        qty = input('''Please enter the quantity of the book you would like to record: 
        ''')

        insert_book(id, name, author, qty)
        print("Task complete.")

    elif choice == 2:

        update_book()

    elif choice == 3: 
        delete_book()

    elif choice == 4:
        search_for()
    
    elif choice == 5 :
        list_all()

    
    elif choice == 0 :
        print('''
Goodbye!
        ''')
        break

    else: 
        print("Error: Please choose from the given options")

#once we are done we must delete our table so the program can run agaim
conn.execute('DROP TABLE books;')
conn.close()