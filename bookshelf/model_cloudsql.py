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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publishedDate = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))
    description = db.Column(db.String(4096))
    rating = db.Column(db.Integer)

    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))

    def __repr__(self):
        return "<Book(title='%s', author=%s)" % (self.title, self.author)
# [END model]

# [START model]
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    pwd = db.Column(db.String(255))
    
    def __repr__(self):
        return "<User(id='%d', name='%s', pwd=%s)" % (self.id, self.name, self.pwd)
# [END model]


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Book.query
             .order_by(Book.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END list]


# [START read]
def read(id):
    result = Book.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read]


# [START create]
def create(data):
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)
# [END create]

# [START createUser]
def createUser(data):
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return from_sql(user)
# [END createUser]

def getName(name):
    user = User.query.filter_by(name = name).first()
    if user is not None:
        return from_sql(user)
    else: return None

# [START update]
def update(data, id):
    book = Book.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)
# [END update] 


def delete(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()

def searchByTitle(title):
    results = builtin_list(map(from_sql, Book.query.filter(Book.title.contains(title)).all()))
    return results

def searchByAuthor(author):
    results = builtin_list(map(from_sql, Book.query.filter(Book.author.contains(author)).all()))
    return results

def searchByDescription(description):
    results = builtin_list(map(from_sql, Book.query.filter(Book.description.contains(description)).all()))
    return results

def searchByRating(rating):
    results = builtin_list(map(from_sql, Book.query.filter_by(rating = rating).all()))
    return results

def searchByYear(year):
    results = builtin_list(map(from_sql, Book.query.filter(Book.publishedDate.contains(year)).all()))
    return results

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
