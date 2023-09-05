import pymongo
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form

uri = 'mongodb+srv://maheshdmah:Mahesh%40divya@cluster0.36cpwss.mongodb.net/?retryWrites=true&w=majority'

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]
# Replace with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def insert_user_data(first_name, last_name, username, phone_number, email):
    try:
        # Connect to the MongoDB server
        client = pymongo.MongoClient(uri)  # Replace with your MongoDB connection URL

        # Select the database
        db = client['LOGIN']  # Replace 'LOGIN' with your desired database name

        # Select the collection (analogous to a table in SQL)
        collection = db['users']

        # Create a user document
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'phone_number': phone_number,
            'email': email
        }

        # Insert the user data into the collection
        result = collection.insert_one(user_data)

        # Close the MongoDB client
        client.close()

        if result.acknowledged:
            return "Data inserted successfully!"
        else:
            return "Error inserting user data."

    except Exception as e:
        return "Error inserting user: " + str(e)
