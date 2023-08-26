from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Client(db.Model):
    id = db.Column(db.Uuid, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(25))
    
class BarberShop(db.Model):
    id = db.Column(db.Uuid, primary_key=True)
    cnpj = db.Column(db.String(50))
    name = db.Column(db.String(100))
    #free_time = db.relationship('Time', backref='barber_shop', lazy=True)
    #reservations = db.relationship('ClientArtTime', backref='barber_shop', lazy=True)

class Time(db.Model):
    id = db.Column(db.Uuid, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    id_barber_shop = db.Column(db.Uuid, db.ForeignKey('barber_shop.id'), nullable=False)
    day = db.Column(db.DateTime)
    
class ClientArtTime(db.Model):
    id = db.Column(db.Uuid, primary_key=True)
    id_client = db.Column(db.Uuid, db.ForeignKey('client.id'), nullable=False)
    id_time = db.Column(db.Uuid, db.ForeignKey('time.id'), nullable=False)
    
class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone')
        
class BarberShopSchema(ma.Schema):
    class Meta:
        fields = ('id', 'cnpj', 'name', 'free_time', 'reservations')
        include_fk = True
        
class TimeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'start_time', 'end_time', 'id_barber_shop', 'day')
        include_fk = True
        
class ClientArtTimeSchema(ma.Schema):
    class Meta:
        fields = ('id', "id_client", 'id_time')
        include_fk = True
        
class BarberShopWithTime(BarberShopSchema):
    free_time = ma.Nested(TimeSchema, many=True)
    
class BarberShopWithClientArtTime(BarberShopSchema):
    reservations = ma.Nested(ClientArtTimeSchema, many=True)