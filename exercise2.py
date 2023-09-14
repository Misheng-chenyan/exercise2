import sqlite3


# Function to read the content of the file and return it as a list
def read_file_to_list(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()


# Function to establish a connection to the SQLite database
def connect_to_database(db_name):
    return sqlite3.connect(db_name)


# Function to create the table in the database
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
            movieID TEXT,
            movieName TEXT,
            movieYear INTEGER,
            imdbRating REAL
        )
    ''')
    connection.commit()


# Function to insert data into the table
def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        cursor.execute('''
            INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating)
            VALUES (?, ?, ?, ?)
        ''', row)
    connection.commit()


# Function to search for movies in the database based on user's choice
def search_movies(connection):
    while True:
        print("\nSearch options:")
        print("1. Movie name")
        print("2. Movie year")
        print("3. Movie rating")
        print("4. STOP")

        choice = input("Enter your choice: ")

        if choice == '1':
            movie_name = input("Enter the movie name: ")
            search_movie_by_name(connection, movie_name)
        elif choice == '2':
            year = input("Enter the movie year: ")
            search_movies_by_year(connection, year)
        elif choice == '3':
            rating = input("Enter the minimum IMDb rating: ")
            search_movies_by_rating(connection, rating)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


# Function to search for movies by name
def search_movie_by_name(connection, movie_name):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT DISTINCT * FROM stephen_king_adaptations_table
        WHERE movieName LIKE ?
    ''', (f'%{movie_name}%',))

    result = cursor.fetchall()
    if result:
        print("Movies found with the given name:")
        for row in result:
            print(f"Movie ID: {row[0]}, Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
    else:
        print("No such movie exists in our database.")


# Function to search for movies by year
def search_movies_by_year(connection, year):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT DISTINCT * FROM stephen_king_adaptations_table
        WHERE movieYear = ?
    ''', (year,))

    result = cursor.fetchall()
    if result:
        print(f"Movies released in {year}:")
        for row in result:
            print(f"Movie ID: {row[0]}, Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
    else:
        print("No movies were found for that year in our database.")


# Function to search for movies by rating
def search_movies_by_rating(connection, rating):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT DISTINCT * FROM stephen_king_adaptations_table
        WHERE imdbRating >= ?
    ''', (rating,))

    result = cursor.fetchall()
    if result:
        print(f"Movies with IMDb rating of {rating} or above:")
        for row in result:
            print(f"Movie ID: {row[0]}, Name: {row[1]}, Year: {row[2]}, Rating: {row[3]}")
    else:
        print(f"No movies at or above {rating} rating were found in the database.")


if __name__ == "__main__":
    file_name = "stephen_king_adaptations.txt"
    db_name = "stephen_king_adaptations.db"

    # Read data from the file and split it into a list of lists
    data = [line.split(',', 3) for line in read_file_to_list(file_name)]

    # Establish a connection to the database, create a table, and insert data
    connection = connect_to_database(db_name)
    create_table(connection)
    insert_data(connection, data)

    print("Database initialized.")

    # Allow the user to search for movies
    search_movies(connection)

    # Close the database connection when done
    connection.close()
