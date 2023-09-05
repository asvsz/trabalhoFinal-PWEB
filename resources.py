from flask_restful import Resource, reqparse, request
from datetime import datetime, time
from model.models import db, BarberShop, BarberShopSchema, Time, TimeSchema, Reservation, ReservationSchema, ClientWithReservation, ClientSchema
from model.models import Client

class TimeResource(Resource):
  def get(self, time_id=None):
    #Retorna todos os times
    if time_id is None:
      times = Time.query.all()
      return TimeSchema(many=True).dump(times), 200
    
    #Retorna determinado time
    time = Time.query.get(time_id)
    if time is not None:
      return TimeSchema().dump(time), 200
    return {'message': 'Horário não encontrado'}, 404
    
  #Adicionar novo horário
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
    
    #Casting de String para DateTime
    start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
    end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    #Instância da classe
    time = Time(start_time=start_time, end_time=end_time, date=date, id_barber_shop=id_barber_shop)

    db.session.add(time)
    db.session.commit()
    return TimeSchema().dump(time), 201
    
class BarberResource(Resource):
  #Todas as reservas
  def get(self, reservation_id=None):
    if reservation_id is None:
      reservations = Reservation.query.all()
      reservations_list = [{"id": r.id, "id_client": r.id_client, "id_time": r.id_time} for r in reservations]
      return reservations_list
  
    else:
      reservation = Reservation.query.get(reservation_id)
      if reservation:
        return {
          'id': reservation.id,
          'id_client': reservation.id_client,
          'id_time': reservation.id_time
            }
      else:
        return {'message': 'Reserva não encontrada'}, 404
      
  #Adiona um novo Barbeiro    
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name_barber', type=str, required=True)
    parser.add_argument('cnpj_barber', type=str, required=True)
    args = parser.parse_args()
    
    barber = BarberShop(name=args['name_barber'], cnpj=args['cnpj_barber'])
    db.session.add(barber)
    db.session.commit()
    return BarberShopSchema().dump(barber), 201


    
class ClientResource(Resource):
  #Todos os horários
  def get(self, time_id=None ):
    if time_id is None:
      times = Time.query.all()
      return TimeSchema(many=True).dump(times), 200     
    
    
  def post(self):
        # Obtém os dados da reserva do corpo da solicitação JSON
        reservation = request.get_json()

        new_reservation = Reservation(id_client=reservation['id_client'], id_time=reservation['id_time'])

        db.session.add(new_reservation)
        db.session.commit()

        return ReservationSchema().dump(new_reservation), 201

#Referente a Criação de um Cliente      
class ClientCreateResource(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('name_client', type=str, required=True)
    parser.add_argument('phone_client', type=str, required=True)
    parser.add_argument('email_client', type=str, required=True)
    args = parser.parse_args()
    
    client = Client(name=args['name_client'], phone=args['phone_client'], email=args['email_client'])
    db.session.add(client)
    db.session.commit()
    return ClientSchema().dump(client), 201