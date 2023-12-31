from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(25))
    email = db.Column(db.String(50))
    reservation = db.relationship('Reservation', backref='client', cascade='all, delete-orphan')
      
class BarberShop(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    cnpj = db.Column(db.String(50))
    time = db.relationship('Time', backref='barber_shop', cascade='all, delete-orphan')
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    id_time = db.Column(db.Integer, db.ForeignKey('time.id'), nullable=False)
    
class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    date = db.Column(db.DateTime)
    id_barber_shop = db.Column(db.Integer, db.ForeignKey('barber_shop.id'), nullable=False)
    
class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'phone', 'email', 'reservation')
        include_fk = True

class BarberShopSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'cnpj', 'time')
        include_fk = True
    
class ReservationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_client', 'id_time')
        include_fk = True
        
class TimeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'start_time', 'end_time', 'date', 'id_barber_shop')
        include_fk = True
            
class ClientWithReservation(ClientSchema):
    reservation = ma.Nested(ReservationSchema, many=True)
    
class BarberShopWithTime(BarberShopSchema):
    time = ma.Nested(TimeSchema, many=True)