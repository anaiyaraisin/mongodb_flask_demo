from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util


#connect to your database environment variable for your connect
connect = MongoClient("mongodb+srv://raisinghani:hello123@datafederationdemo.qqa6o9q.mongodb.net/?retryWrites=true&w=majority")

#add in your database and collection from Atlas
database = connect["bookshelf"]
collection = database["books"]
 
#instantiating new object with "name"
app = Flask(__name__)

#our initial form page
@app.route('/')  #root is "/"
def index():
    return render_template("index.html")

#CREATE WORKS
@app.route('/newbook', methods=['POST'])
def addbook(): 
    # POST new book this is how you'll enter it in Postman
    if request.method == 'POST':
        #request.json returns a JSON object. So you'll see it pretty in Postman
        book = request.json['book']
        pages = request.json['pages']

        #insert new book into books collection in MongoDB
        database['books'].insert_one({"book": book,"pages": pages})

        return "update: Your book has been added to your bookshelf."


#READ WORKS
@app.route('/viewbooks', methods=['GET'])
def viewbook():
    if request.method == 'GET':
        #view all books in your mongodb database
        bookshelf = list(database['books'].find())
        titles = []

        #make it pretty 
        for books in bookshelf:
            book = books['book']
            pages = books['pages']
            shelf = {'book': book, 'pages': pages}
            titles.append(shelf)
        print(titles)

        return titles 



#READ this output is sooo ugly. ignore this code block.
# @app.route('/viewbooks', methods=['GET'])
# def viewbooks():
#     if request.method == 'GET':
#         bookshelf = database['books'].find()
#         return json_util.dumps(bookshelf, indent=4)



#UPDATE WORKS   
@app.route('/exchangebook/<string:name>/<int:pages>', methods = ['PUT']) #to update in postman use PUT
def exchangebook(name, pages):
    if request.method == 'PUT':
        new_book = request.json['book']
        new_pages = request.json['pages']

        #this updates your selected book
        database['books'].update_one({"book": name, "pages": pages},{"$set": {"book": new_book, "pages": new_pages}})

        return "update: Your book has been exchanged."

#DELETE WORKS 
@app.route('/removebook/<string:name>/<int:pages>', methods = ['DELETE'])
def removebook(name,pages):
    if request.method == 'DELETE':
        database['books'].delete_one({"book": name, "pages": pages})

        return "update: Your book has been removed from your bookshelf."


#this makes it so our app runs on port 8000. when running, use command:
#flask run --port 8000
if __name__ == '__main__':
    app.run(port=8000)

        

