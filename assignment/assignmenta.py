import requests
from models import User,Post,Owner
from datetime import datetime
from mongoengine import connect
from db import connect_to_database
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
    'app-id': '651444b564575f215f403798'
     }

# Establish the database connection
connect(
    db="TailNode",  
    host=os.environ.get('MongoURL'),
)
db_client = connect_to_database()

def save_users():
   if db_client:  
  
     # Make the HTTP GET request with headers
     response = requests.get('https://dummyapi.io/data/v1/user', headers=headers)

     # Check the response
     if response.status_code == 200:

     # Process the response data here

      data = response.json()

      for data in data["data"]:
        # creating instance of User
        user=User(user_id=data["id"],title=data["title"],firstName=data["firstName"],lastName=data["lastName"],picture=data["picture"])

        # saving instance of user
        user.save()
      
      # response after posting all data
      print(" All user data saved in the database")
     else:
       print(f"Failed to post data. Status code: {response.status_code}")
   else:
    # Handle the case where the connection failed
    print("Exiting the application due to a database connection error.")

def post_save():
  if db_client:
    # get all the users from database
    datas = User.objects()
    
    # get request from api and adding user_id from data i.e retrived from database.
    for data in datas:
      #  retriving data from api
       response = requests.get(f'https://dummyapi.io/data/v1/user/{data["user_id"]}/post', headers=headers)

      #  converting data to json
       postdata=response.json()

       for postdata in postdata["data"]:
         
        #  creating instance of Post
         post=Post(image=postdata["image"],likes=postdata["likes"],tags=postdata["tags"],text=postdata["text"],publishDate=datetime.strptime(postdata["publishDate"], "%Y-%m-%dT%H:%M:%S.%fZ"),
          owner=Owner(id=data["user_id"],title=data["title"],firstname=data["firstName"],lastname=data["lastName"],picture=data["picture"]))
         
        #  saving the instance into database.
         post.save()
         
    print("post for all the users got saved!")


def main():
    save_users()
    post_save()

if __name__=="__main__":
  main()
  