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
from flask import Blueprint, redirect, render_template, request, url_for


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


@crud.route('/<id>',methods=['GET', 'POST'])
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

# [START search_start]
@crud.route('/search', methods=['GET', 'POST'])
def search_start():
    if request.method == 'POST':
        query = request.form["q"]
        
        if(query is not None):
            category = request.form['Category']

            if category == 'Title':
                booklist = get_model().searchByTitle(query)
            
            elif category == 'Author':
                booklist = get_model().searchByAuthor(query)
                
            elif category == 'Rating':
                booklist = get_model().searchByRating(query)
            
            elif category == 'Description':
                booklist = get_model().searchByDescription(query)
            
            elif category == 'Year':
                booklist = get_model().searchByYear(query)
                
            return render_template("search.html", searchlist=booklist)
        
    return render_template("search.html")
    
# [END search_start]

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
