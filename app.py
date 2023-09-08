from flask import Flask, jsonify
from flask_swagger import swagger
from flask_restful import Api
from models.models import db, ma
from resources.resources import TimeResource, BarberShopResource, ClientResource, ResevationResource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/swagger')
def get_swagger():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Sistema de Barbearia"
    swag['info']['description'] = "API para gerenciamento do sistema da barbearia."

    swag['paths']['/client'] = {
    'post': {
        'summary': 'Criar um novo cliente',
        'consumes': ['application/json'],
        'tags': ['Client'],
        'parameters': [
            {
                'name': 'name',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'Nome do cliente'
            },
            {
                'name': 'phone',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'Telefone do cliente'
            },
            {
                'name': 'email',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'Email do cliente'
            },
        ],
        'responses': {
            '201': {
                'description': 'Cliente criado com sucesso'
            }
        }
    },
    'get': {
        'summary': 'Buscar todos os clientes',
        'tags': ['Client'],
        'responses': {
            '200': {
                'description': 'Lista de clientes'
            },
            '404': {
                'description': 'Cliente não encontrado'
            }
        }
    }
}

    swag['paths']['/client/{client_id}'] = {
        'get': {
            'summary': 'Buscar um cliente pelo ID',
            'tags': ['Client'],
            'parameters': [
                {
                    'name': 'client_id',
                    'in': 'path',
                    'required': True,
                    'type': 'integer'
                }
            ],
            'responses': {
                '200': {
                    'description': 'Detalhes do cliente'
                }
            }
        }
    }

    swag['paths']['/barbershop'] = {
        'post': {
            'summary': 'Criar uma nova barbearia',
            'tags': ['BarberShop'],
            'consumes': ['application/json'],
            'parameters': [
            {
                'name': 'name',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'Nome da barbearia'
            },
            {
                'name': 'cnpj',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'CNPJ da barbearia'
            }
        ],
        'responses': {
            '201': {
                'description': 'Barbearia criada com sucesso'
            }
        },
    },
    'get': {
        'summary': 'Buscar todas as barbearias',
        'tags': ['BarberShop'],
        'responses': {
            '200': {
                'description': 'Lista de barbearias'
            },
            '404': {
                'description': 'Barbearia não encontrada'
            }
        }
    }
    }

    swag['paths']['/barbershop/{barbershop_id}'] = {
        'get': {
            'summary': 'Buscar uma barbearia pelo ID',
            'tags': ['BarberShop'],
            'parameters': [
                {
                    'name': 'barbershop_id',
                    'in': 'path',
                    'required': True,
                    'type': 'integer'
                }
            ],
            'responses': {
                '200': {
                    'description': 'Detalhes da barbearia'
                }
            }
        }
    }

    swag['paths']['/time'] = {
        'post': {
            'summary': 'Criar um novo horário',
            'tags': ['Time'],
            'consumes': ['application/json'],
            'parameters': [
            {
                'name': 'start_time',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'inicio do horário'
            },
            {
                'name': 'end_time',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'encerramento do horário'
            },
            {
                'name': 'date',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'data'
            },
            {
                'name': 'id_barbershop',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'id da barbearia'
            }
        ],
            'responses': {
                '201': {
                    'description': 'Horário criado com sucesso'
                }
                
            }
        },
        'get': {
            'summary': 'Buscar todos os horários',
            'tags': ['Time'],
            'responses': {
                '200': {
                    'description': 'Lista de horários'
                },
                '404': {
                    'description': 'Horário não encontrado'
                }
            }
        }
    }

    swag['paths']['/time/{time_id}'] = {
        'get': {
            'summary': 'Buscar um horário pelo ID',
            'tags': ['Time'],
            'parameters': [
                {
                    'name': 'time_id',
                    'in': 'path',
                    'required': True,
                    'type': 'integer'
                }
            ],
            'responses': {
                '200': {
                    'description': 'Detalhes do horário'
                }
            }
        },
        'delete': {
            'summary': 'Excluir um horário pelo ID',
            'tags': ['Time'],
            'parameters': [
                {
                    'name': 'time_id',
                    'in': 'path',
                    'required': True,
                    'type': 'integer'
                }
            ],
            'responses': {
                '204': {
                    'description': 'Horário excluído com sucesso'
                }
            }
        }
    }

    swag['paths']['/reservation'] = {
        'post': {
            'summary': 'Criar uma nova reserva',
            'tags': ['Reservation'],
            'consumes': ['application/json'],
            'parameters': [
            {
                'name': 'id_client',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'id do cliente'
            },
            {
                'name': 'id_time',
                'in': 'formData',
                'type': 'string',
                'required': True,
                'description': 'id do horário'
            }
        ],
            'responses': {
                '201': {
                    'description': 'Reserva criada com sucesso'
                }
            }
        },
        'get': {
            'summary': 'Buscar todas as reservas',
            'tags': ['Reservation'],
            'responses': {
                '200': {
                    'description': 'Lista de reservas'
                },
                '404': {
                    'description': 'Reserva não encontrada'
                }
            }
        }
    }

    swag['paths']['/reservation/{reservation_id}'] = {
        'get': {
            'summary': 'Buscar uma reserva pelo ID',
            'tags': ['Reservation'],
            'parameters': [
                {
                    'name': 'reservation_id',
                    'in': 'path',
                    'required': True,
                    'type': 'integer'
                }
            ],
            'responses': {
                '200': {
                    'description': 'Detalhes da reserva'
                }
            }
        },
        'delete': {
            'summary': 'Excluir uma reserva pelo ID',
            'tags': ['Reservation'],
            'parameters': [
                {
                    'name': 'reservation_id',
                    'in': 'path',
                    'required': True,
                    'type': 'integer'
                }
            ],
            'responses': {
                '204': {
                    'description': 'Reserva excluída com sucesso'
                }
            }
        }
    }

    return jsonify(swag)

SWAGGER_URL = '/docs'
swagger_route = '/swagger'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    swagger_route,
    config={'app_name': "Sistema de Barbearia"}
)

api.add_resource(TimeResource, '/time', '/time/<int:time_id>')
api.add_resource(BarberShopResource, '/barbershop', '/barbershop/<int:barbershop_id>')
api.add_resource(ClientResource, '/client', '/client/<int:client_id>')
api.add_resource(ResevationResource, '/reservation', '/reservation/<int:reservation_id>')

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
