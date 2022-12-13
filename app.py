from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__)

## Database part
client = MongoClient('localhost', 27017)
db = client.Flask_Todo
todos = db.todo


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todos.insert_one({'title': title, 'Description': desc})
        return redirect(url_for('index'))
    
    all_todos = todos.find()
    return render_template('index.html', allTodo = all_todos)


@app.route('/delete/<id>')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/update/<id>', methods = ['GET', 'POST'])
def update(id):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todos.delete_one({"_id": ObjectId(id)})
        todos.insert_one({'title': title, 'Description': desc})
        return redirect(url_for('index'))

    update_todo = todos.find_one({"_id": ObjectId(id)})
    print(update_todo)
    return render_template('update.html', update_todo = update_todo)


if __name__ == "__main__":
    app.run(debug = True)