from zipfile import ZipFile
import re
import mysql.connector
import os
import requests
import time

# go to the url and download the zip folder in current directory


def download_zip_file(url):
    # Extract the file name from the URL
    file_name = url.split('/')[-1]

    # Determine the destination directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Send a GET request to the URL
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Define the file path
        file_path = os.path.join(script_dir, file_name)

        start_time = time.time()
        downloaded_bytes = 0

        # Save the file to the destination directory
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_bytes += len(chunk)

                    elapsed_time = int(time.time() - start_time)
                    print(
                        f"Download started, Running since {elapsed_time} seconds elapsed.", end='\r')

        end_time = time.time()
        duration = end_time - start_time

        print(
            f"File '{file_name}' downloaded and saved successfully in {duration} seconds.")
    else:
        print("Error: Failed to download the file.")


# Example usage
# url = "https://cricsheet.org/downloads/all_json.zip"
# download_zip_file(url)

# do a basic check of database and table existence


def check_database(database_name):
    print("Database check started")

    start_time = time.time()

    # Connect to the MySQL server
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456"
        )

        cursor = connection.cursor()

        # Check if the database exists
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        database_exists = False

        for db in databases:
            if db[0] == database_name:
                database_exists = True
                break

        # If the database doesn't exist, create it
        if not database_exists:
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database '{database_name}' created")
        else:
            print(f"Database '{database_name}' exists")

        # Use the database
        cursor.execute(f"USE {database_name}")

        # List of required tables
        required_tables = [
            "matches",
            "meta_info",
            "info_section",
            "innings_info",
            "over_section"
        ]

        # Check and create missing tables
        for table in required_tables:
            cursor.execute(f"SHOW TABLES LIKE '{table}'")
            table_exists = cursor.fetchone()

            if table_exists:
                print(f"Table '{table}' exists")
            else:
                # Create the table
                create_table_query = None
                if table == "matches":
                    create_table_query = """
                        CREATE TABLE matches (
                            start_date DATE,
                            teams_type VARCHAR(255),
                            match_type VARCHAR(255),
                            gender VARCHAR(255),
                            match_id VARCHAR(50) PRIMARY KEY,
                            team_involved_one VARCHAR(255),
                            team_involved_two VARCHAR(255)
                        )
                    """
                elif table == "meta_info":
                    create_table_query = """
                        CREATE TABLE meta_info (
                            match_id VARCHAR(255) PRIMARY KEY,
                            data_version VARCHAR(255),
                            created VARCHAR(255),
                            revision VARCHAR(255)
                        )
                    """
                elif table == "info_section":
                    create_table_query = """
                        CREATE TABLE info_section (
                            match_id VARCHAR(255) PRIMARY KEY,
                            balls_per_over INT,
                            bowl_out VARCHAR(255),
                            city VARCHAR(255),
                            dates TEXT,
                            event TEXT,
                            gender VARCHAR(255),
                            match_type VARCHAR(255),
                            match_type_number INT,
                            missing VARCHAR(255),
                            officials TEXT,
                            outcome TEXT,
                            overs INT,
                            player_of_match TEXT,
                            players TEXT,
                            registry TEXT,
                            season TEXT,
                            supersubs VARCHAR(255),
                            team_type VARCHAR(255),
                            teams TEXT,
                            toss TEXT,
                            venue VARCHAR(255)
                        )
                    """
                elif table == "innings_info":
                    create_table_query = """
                        CREATE TABLE innings_info (
                            match_id VARCHAR(255),
                            team VARCHAR(255),
                            declared VARCHAR(255),
                            forfeited VARCHAR(255),
                            powerplays TEXT,
                            target TEXT,
                            super_over TEXT,
                            innings INT
                        )
                    """
                elif table == "over_section":
                    create_table_query = """
                        CREATE TABLE over_section (
                            match_id VARCHAR(255),
                            innings VARCHAR(255),
                            overs VARCHAR(10),
                            batter VARCHAR(255),
                            bowler VARCHAR(255),
                            extras JSON,
                            non_striker VARCHAR(255),
                            review JSON,
                            runs JSON,
                            wickets JSON,
                            replacements JSON
                        )
                    """

                if create_table_query:
                    cursor.execute(create_table_query)
                    print(f"Table '{table}' created")

        connection.commit()
        cursor.close()
        connection.close()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Database check completed in {duration} seconds")

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)


# Example usage
database_name = "cricket_data"
check_database(database_name)


def extract_number_from_text(text):
    pattern = r'This\s*archive\s*contains\s*(\d+)\s*matches'
    match = re.search(pattern, text)
    if match:
        number = int(match.group(1))
        return number
    return None


def check_match_count():
    print("Starting data check and storage")

    # Specify the name of the zip file and the file within it
    zip_file_name = 'all_json.zip'  # Replace with the actual zip file name
    file_within_zip = 'README.txt'  # Replace with the actual file name within the zip

    # Extract the number from the file within the zip
    with ZipFile(zip_file_name, 'r') as zip:
        with zip.open(file_within_zip) as file:
            data = file.read().decode('utf-8')
            total_matches = extract_number_from_text(data)

    # Connect to the MySQL server
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="cricket_data"  # Replace with the actual database name
        )

        cursor = connection.cursor()

        # Query the matches table for the count of match_id
        cursor.execute("SELECT COUNT(match_id) FROM matches")
        result = cursor.fetchone()
        db_total_matches = result[0]

        # Print the match counts
        print(f"Match count from db: {db_total_matches}")
        print(f"Match count from README.txt: {total_matches}")

        # Compare the match counts
        if db_total_matches != total_matches:
            print("Data mismatch.")
        else:
            print("Data up to date.")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)

    print("Data check and storage completed")


# Example usage
check_match_count()
