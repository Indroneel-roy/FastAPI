# Import FastAPI from the fastapi module
from fastapi import FastAPI

# Create an instance of the FastAPI class
# This 'app' object will be used to define routes (URLs) and handle incoming HTTP requests
app = FastAPI()

# Define a route for the root URL "/"
# This decorator tells FastAPI to call the 'hello()' function when someone visits "/"
@app.get("/")  # HTTP GET method on the root path "/"
def hello():
    # Return a JSON response with a key "Message" and value "hello world"
    return {"Message": "hello world"}

# Define another route for "/about"
@app.get("/about")  # HTTP GET method on path "/about"
def about():
    # Return a JSON response with a custom message
    return {"message": "Indroneel is going to get a job at Google as an ML Engineer"}
