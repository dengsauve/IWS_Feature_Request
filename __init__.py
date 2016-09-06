from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////var/www/FlaskApp/FlaskApp/database/flaskapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Request(db.Model):
    __tablename__ = 'Request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(1000))
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    client = db.relationship('Client', backref=db.backref('requests', lazy='dynamic'))
    priority = db.Column(db.Integer)
    targetdate = db.Column(db.Date)
    ticketurl = db.Column(db.String(200))
    productarea_id = db.Column(db.Integer, db.ForeignKey('ProductArea.id'))
    productarea = db.relationship('ProductArea', backref=db.backref('requests', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))

    def __init__(self, title, description, client, priority, targetdate, ticketurl, productarea, user):
        self.title = title
        self.description = description
        self.client = client
        self.priority = priority
        self.targetdate = targetdate
        self.ticketurl = ticketurl
        self.productarea = productarea
        self.user = user

    def __repr__(self):
        return '<Request> %r' % self.title


class Client(db.Model):
    __tablename__ = 'Client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Client> %r' % self.name


class ProductArea(db.Model):
    __tablename__ = 'ProductArea'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ProductArea> %r' % self.name


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(16))
    isAdmin = db.Column(db.Boolean)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    client = db.relationship('Client', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, email, password, idAdmin, client):
        self.username = username
        self.email = email
        self.password = password
        self.isAdmin = False
        self.client = client

    def __repr__(self):
        return '<User> %r' % self.username


@app.route('/')
@app.route('/login/', strict_slashes=False)
def render_main():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def render_home():
    clients = Client.query.with_entities(Client.name)
    areas = ProductArea.query.with_entities(ProductArea.name)
    return render_template('index.html', areas=areas, clients=clients)


@app.errorhandler(404)
    def render_page_not_found():
        return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
