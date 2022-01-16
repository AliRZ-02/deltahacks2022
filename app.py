from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Creating the Flask App and Configuring the Database through SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///requests.db'
db = SQLAlchemy(app)

# Class that handles the database and the columns present in it
class UserReviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    review = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Main Website URL - Uses index.html


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/addReview', methods=['GET', 'POST'])
def add_review():
    return render_template('reviews.html')


if __name__ == "__main__":
    app.run(debug=True)
