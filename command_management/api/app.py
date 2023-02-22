import logging
from flask import Flask
from flask_restful import Api
from cheroot.wsgi import Server as WSGIServer
from command_management.api.routes.purchase_orders import PurchaseOrders
from command_management.util.settings import PORT_API

APP = Flask(__name__)
API = Api(APP)
PORT = PORT_API
SERVER = WSGIServer(('0.0.0.0', PORT), APP)

API.add_resource(PurchaseOrders, '/pedido')

if __name__ == '__main__':
    logging.basicConfig(format='', level=logging.INFO)
    logging.info('Running server on port %s', PORT)
    SERVER.safe_start()
