import psycopg2
from Logger import logger

# Define connection parameters
hostname = 'localhost'       # Host where the PostgreSQL server is running
port = '5432'                # Default PostgreSQL port
database = 'mydatabase'      # The database name you want to connect to
username = 'rohit'          # Your PostgreSQL username
password = 'mypassword'      # Your PostgreSQL password

# Establish the connection
try:
    connedatabase.pyction = psycopg2.connect(
        host=hostname,
        port=port,
        dbname=database,
        user=username,
        password=password
    )


    # Create a cursor object using a context manager
    with connection.cursor() as cursor:
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        logger.info("PostgreSQL version:", db_version)

except Exception as error:
    logger.info(f"Error: {error}")

finally:
    # Close the connection if it's open
    if connection:
        connection.close()
        logger.info("Connection closed.")
