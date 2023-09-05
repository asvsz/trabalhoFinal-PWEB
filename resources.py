from flask_restful import Resource, reqparse
from datetime import datetime
from model.models import db, BarberShop, BarberShopSchema, Time, TimeSchema, ClientWithReservation, ClientSchema, BarberShopWithTime
from model.models import Client

class TimeResource(Resource):
  def get(self, time_id=None):
    #Retorna todos os horários
    if time_id is None:
      times = Time.query.all()
      return TimeSchema(many=True).dump(times), 200
    
    #Retorna determinado horário
    time = Time.query.get(time_id)
    if time is not None:
      return TimeSchema().dump(time), 200
    return {'message': 'Horário não encontrado'}, 404
    
  #Adicionar um novo horário
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('start_time', type=str, required=True)
    parser.add_argument('end_time', type=str, required=True)
    parser.add_argument('date', type=str, required=True)
    parser.add_argument('id_barber_shop', type=int, required=True)
    
    args = parser.parse_args()
    
    start_time_str = args['start_time']
    end_time_str = args['end_time']
    date_str = args['date']
    id_barber_shop = args['id_barber_shop']
    
    id_barber = BarberShop.query.get(id_barber_shop) #Verifica a existência da barbearia
    if id_barber is not None:
      #Casting de String para DateTime
      start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
      end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
      date = datetime.strptime(date_str, '%Y-%m-%d').date()

      #Instância da classe
      time = Time(start_time=start_time, end_time=end_time, date=date, id_barber_shop=id_barber_shop)
      db.session.add(time)
      db.session.commit()
      return TimeSchema().dump(time), 201
    return {'message': 'A barbearia com o id: {} não foi encontrada'.format(id_barber_shop)}, 400
  
  #Deleta determinado horário
  def delete(self, time_id=None):
    time = Time.query.get(time_id)
    if time is not None:
      try: 
        db.session.delete(time)
        db.session.commit()
        return {'message': 'Reserva excluida com sucesso'}, 204
      except Exception:
        return {'message': 'A reserva não pode ser excluida pois está em uso'}, 409
    return {'message': 'Reserva não encontrada'}, 404
    
class BarberShopResource(Resource):
  def get(self, barbershop_id=None):
    #Retorna todos os barbearias
    if barbershop_id is None:
      barber_shops = BarberShop.query.all()
      return BarberShopWithTime(many=True).dump(barber_shops), 200
    
    #Retorna determinado barbearia
    barber_shop = BarberShop.query.get(barbershop_id)
    if barber_shop is not None:
      return BarberShopWithTime().dump(barber_shop), 200
    return {'message': 'Barbearia não encontrada'}, 404
      
  #Adiona um novo Barbeiro    
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('cpnj', type=str, required=True)
    args = parser.parse_args()
    
    barber = BarberShop(name=args['name'], cnpj=args['cpnj'])
    db.session.add(barber)
    db.session.commit()
    return BarberShopSchema().dump(barber), 201

class ClientResource(Resource):
  def get(self, client_id=None):
    #Retorna todos os clientes
    if client_id is None:
      clients = Client.query.all()
      return ClientWithReservation(many=True).dump(clients), 200
    
    #Retorna determinado cliente
    client = Client.query.get(client_id)
    if client is not None:
      return ClientWithReservation().dump(client), 200
    return {'message': 'Client não encontrada'}, 404
    
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('phone', type=str, required=True)
    parser.add_argument('email', type=str, required=True)
    args = parser.parse_args()
    
    client = Client(name=args['name'], phone=args['phone'], email=args['email'])
    db.session.add(client)
    db.session.commit()
    return ClientSchema().dump(client), 201