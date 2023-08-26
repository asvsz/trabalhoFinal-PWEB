from flask import Flask
from flask_restful import Api
from model.models import db, ma 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)