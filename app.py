from bson.objectid import ObjectId
from flask import Flask, flash, redirect, render_template, request, url_for
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key="123456tgbgfdw3456ygfdew345tgse45thfdw"


## Database part
client = MongoClient('localhost', 27017)
db = client.Flask_Todo
todos = db.todo # collection for todo
user_login = db.Login # collection for Login


def find_or_not(list, ussid, password):
    for ele in list:
        if str(ele['ussid'])==ussid and str(ele['password'])==password:
            return True
    return False

@app.route("/", methods= ('GET', 'POST'))
def login():
    if request.method=="POST":
        ussid = request.form['ussid']
        password = request.form['password']
        get_login = user_login.find()
        res = list(get_login)
        check = find_or_not(res, ussid, password)
        if check==False:
            flash('Incorrect Credentials!!')
            return render_template('login_form.html')
        else:
            return redirect(url_for('index'))
    
    return render_template('login_form.html')


@app.route('/todo', methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        title = request.form['title'].strip()
        desc = request.form['desc'].strip()
        if len(title)>0 and len(desc)>0:
            todos.insert_one({'title': title, 'Description': desc})
        else:
            flash('Please provide valid title and description') 
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