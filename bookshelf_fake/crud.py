# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for, session


crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list]


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        token = request.args.get('page_token', None)
        if token:
            token = token.encode('utf-8')
        search_query=request.form["search_query"]
        if request.form['Search_Category'] == 'title':
            booklist=get_model().search_title(search_query)
        elif request.form['Search_Category'] == 'year':
            booklist=get_model().search_year(search_query)
        elif request.form['Search_Category'] == 'month':
            booklist=get_model().search_month(search_query)
        elif request.form['Search_Category'] == 'day':
            booklist=get_model().search_day(search_query)
        elif request.form['Search_Category'] == 'author':
            booklist=get_model().search_author(search_query) 
        elif request.form['Search_Category'] == 'rating':
            booklist=get_model().search_rating(search_query)     
        return render_template("search.html", searchlist=booklist)
    return redirect(url_for('.list'))

@crud.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form.to_dict(flat=True)
        result = get_model().usermatch(data)
        if result==True:
            session.permanent = True
            session['id'] = data["id"]
            session['name']=get_model().getname(data)
            return redirect(url_for('.list'))

        if result == False:
            return render_template("login.html")

    if 'id' in session and 'name' in session:
        return f"<h1>Already Logged In</h1>"
    return render_template("login.html",id="")

@crud.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        get_model().adduser(data)
        session['id'] = data["id"]
        session['name']=get_model().getname(data)
        return render_template("mypage.html")

    if 'id' in session and 'name' in session:
        return f"<h1>Already Logged In</h1>"

    return render_template("register.html",action = "Register")

@crud.route("/logout")
def logout():
    session.pop("id",None)
    session.pop("name",None)
    return redirect(url_for('.list'))

@crud.route('/mypage')
def mypage():
    if 'id' in session:
        books = get_model().mybooks(session['id'])
        return render_template("mypage.html", booklist=books)
    return f"<h1>You are not logged in yet</h1>"

@crud.route('/mypage/edit/<id>', methods=['GET', 'POST'])
def edituser(id):
    user = get_model().readuser(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = get_model().update_user(data, id)
        session['name'] =data["name"]
        return redirect(url_for('.mypage', id=user['id']))

    return render_template("register.html", action="Edit")

@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
