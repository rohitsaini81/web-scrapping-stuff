import psycopg2
from Logger import logger

# Define connection parameters
hostname = 'localhost'       # Host where the PostgreSQL server is running
port = '5432'                # Default PostgreSQL port
database = 'mydatabase'      # The database name you want to connect to
username = 'rohitsaini'          # Your PostgreSQL username
# username = 'rohit'          # Your PostgreSQL username
password = 'mypassword'      # Your PostgreSQL password

# postgresql://rohitsaini:mypassword@127.0.0.1:5432/mydatabase


def create():
    return "Some data created"
# Establish the connection


def create_connection():
    try:
        connection = psycopg2.connect(
            host=hostname,
            port=port,
            dbname=database,
            user=username,
            password=password
        )
        return connection
    except Exception as error:
        logger.info(f"Error: {error}")
        return None

# Create (Insert data into the table)


def create_video(title, img_url, video_url, tags, description, category, duration):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                insert_query = '''
                    INSERT INTO videos2 (title, img_url, video_url, tags, description, category, duration)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                '''
                cursor.execute(insert_query, (title, img_url,
                               video_url, tags, description, category, duration))
                connection.commit()
                logger.info(f"Video inserted successfully.")
        except Exception as error:
            logger.info(f"Error: {error}")
        finally:
            connection.close()


def find_video(video_id=None, title=None, tags=None, keywords=None):
    """Retrieve video details based on ID, title, tags, or keywords."""
    connection = create_connection()
    if not connection:
        return None  # Exit if no connection is available

    try:
        with connection.cursor() as cursor:
            conditions = []
            params = []

            if video_id:
                conditions.append("id = %s")
                params.append(video_id)

            if title:
                conditions.append("title ILIKE %s")
                params.append(f"%{title}%")  # Partial match

            if tags:
                # Works for TEXT/VARCHAR columns
                conditions.append("tags ILIKE %s")
                params.append(f"%{tags}%")  # Partial match for any occurrence

            if keywords:
                # Works for TEXT/VARCHAR columns
                conditions.append("keywords ILIKE %s")
                params.append(f"%{keywords}%")  # Partial match

            # If no conditions are provided, return an error
            if not conditions:
                return {"error": "No search parameters provided"}

            # Join conditions with OR
            query = "SELECT * FROM videos WHERE " + " OR ".join(conditions)
            # logger.info("Generated Query:", query, params)

            # Execute Query
            cursor.execute(query, params)
            data = cursor.fetchall()

            # Process Results
            if data:
                for row in data:
                    logger.info(
                        f"ID: {row[0]}, Title: {row[1]}, Video URL: {row[3]}")
                return data
            else:
                logger.info("No videos found.")
                return None

    except Exception as error:
        logger.info(f"Error: {error}")
        return None
    finally:
        connection.close()  # Ensure connection is closed


# Read (Fetch all data from the table)
def read_videos():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM videos2;")
                data = cursor.fetchall()
                if data:
                    return data
                    for row in data:
                        logger.info(
                            f"ID: {row[0]}, Title: {row[1]}, Video URL: {row[3]}")
                else:
                    logger.info("No videos found.")
        except Exception as error:
            logger.info(f"Error: {error}")
        finally:
            connection.close()


def find_one(video_id=0):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM videos WHERE id = %s;"
                cursor.execute(query, (video_id,))
                data = cursor.fetchone()

                if data is None:
                    return None
                if data:
                    return {
                        "id": data[0],
                        "title": data[1],
                        "image": data[2],
                        "video_url": data[3],
                        "tags": data[4],
                        "description": data[5],
                        "keywords": data[6]
                    }
                    for row in data:
                        logger.info(
                            f"ID: {row[0]}, Title: {row[1]}, Video URL: {row[3]}")
                else:
                    logger.info("No videos found.")
        except Exception as error:
            logger.info(f"Error: {error}")
        finally:
            connection.close()


# Update (Update data in the table)


def update_video(video_id, title=None, img_url=None, video_url=None, tags=None, description=None, keywords=None):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                update_query = "UPDATE videos SET "
                params = []

                if title:
                    update_query += "title = %s, "
                    params.append(title)
                if img_url:
                    update_query += "img_url = %s, "
                    params.append(img_url)
                if video_url:
                    update_query += "video_url = %s, "
                    params.append(video_url)
                if tags:
                    update_query += "tags = %s, "
                    params.append(tags)
                if description:
                    update_query += "description = %s, "
                    params.append(description)
                if keywords:
                    update_query += "keywords = %s, "
                    params.append(keywords)

                # Remove trailing comma and space
                update_query = update_query.rstrip(', ')
                update_query += " WHERE id = %s;"
                params.append(video_id)

                cursor.execute(update_query, tuple(params))
                connection.commit()

                logger.info(f"Video with ID {video_id} updated successfully.")
        except Exception as error:
            logger.info(f"Error: {error}")
        finally:
            connection.close()


def update_url(old_img_url, new_img_url, image):
    connection = create_connection()
    isUpdated = False
    if connection:
        try:
            with connection.cursor() as cursor:
                if image:
                    update_query = "UPDATE videos SET img_url = %s WHERE img_url = %s;"
                    cursor.execute(update_query, (new_img_url, old_img_url))
                    if cursor.rowcount > 0:
                        logger.info("Update successful!")
                        isUpdated = True
                    else:
                        logger.info(
                            "No rows updated. (Maybe the old_img_url was not found?)")
                        return False
                else:
                    update_query = "UPDATE videos SET video_url = %s WHERE video_url= %s;"
                    cursor.execute(update_query, (new_img_url, old_img_url))
                    if cursor.rowcount > 0:
                        logger.info("Update successful!")
                        isUpdated = True
                    else:
                        logger.info(
                            "No rows updated. (Maybe the old_img_url was not found?)")
                        return False

            connection.commit()

        except Exception as error:
            logger.info(f"Error: {error}")
        finally:
            connection.close()
            return isUpdated

# Delete (Delete data from the table)


def delete_video(video_id):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                delete_query = "DELETE FROM videos WHERE id = %s;"
                cursor.execute(delete_query, (video_id,))
                connection.commit()
                logger.info(f"Video with ID {video_id} deleted successfully.")
        except Exception as error:
            logger.info(f"Error: {error}")
        finally:
            connection.close()


#     create_video(
#         title="How to Learn Python",
#         img_url="https://example.com/python_img.jpg",
#         video_url="https://example.com/python_video.mp4",
#         tags="Python, Programming, Tutorial",
#         description="This is a tutorial video on how to learn Python programming for beginners.",
#         keywords="Python, programming, tutorial"
#     )
#logger.info(read_videos())
