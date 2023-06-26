from sqlalchemy import create_engine, text, insert
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
db_connection_string = os.getenv('DB_CONNECTION_STRING')


engine = create_engine(db_connection_string)



def load_users_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))

        all_users = []
        for row in result.all():
            all_users.append(dict(row))
            print(row)
        return all_users
    
def get_user_firstname_from_db(email):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = '%s'" %email))
        user = []
        for row in result.all():
            user.append(dict(row))
        user_firstname = user[0].get('firstname')
        return user_firstname
# result = get_user_firstname_from_db('jimh01@gmail.com')
# print(get_user_firstname_from_db('jimh01@gmail.com'))
# print(load_users_from_db())

def get_username_from_db(email):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = '%s'" %email))
        user = []
        for row in result.all():
            user.append(dict(row))
        username = user[0].get('username')
        return username


def add_video_from_db(username, video_name):
    with engine.connect() as conn:
        query = text("INSERT INTO uploaded_videos (username, video_name ) values (:username, :video_name)")
        conn.execute(query, username=username, video_name=video_name)
        result = conn.execute(text("SELECT * FROM uploaded_videos WHERE username = '%s'" %username))
        all_videos = []
        for row in result.all():
            all_videos.append(dict(row))
            print(row)
        return all_videos
    
