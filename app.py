from flask import Flask
from flask_restful import Api
from model.models import db, ma
from resources import TimeResource, BarberShopResource, ClientResource, ClientCreateResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()
    
api.add_resource(TimeResource, '/time', '/time/<int:time_id>') #Okay
api.add_resource(BarberShopResource,'/barbershop', '/barbershop/<int:barbershop_id>') #Okay
api.add_resource(ClientResource, '/client', '/client/<int:client_id>') #Okay'''


if __name__ == '__main__':
    app.run(debug=True)