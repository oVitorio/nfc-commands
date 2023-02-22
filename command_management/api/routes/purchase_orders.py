import json
import queue
import threading
from flask import Response, request, abort
from flask_restful import Resource


class PurchaseOrders(Resource):

    task = queue.Queue()

    def post(self):

        order = request.args.get('order', '').upper()

        supported_orders = {
            'TESTE':  PurchaseOrders.teste,
        }

        if order not in supported_orders:
            abort(400, f'Purchase Orders {order.lower()} not fund!')

        new_thread = threading.Thread(target=supported_orders[order])

        if self.task.empty():
            new_thread.start()
            self.task.put(new_thread)
            return Response(response=json.dumps({f'Running order {order}': 'ok'}), status=202)

        for thread in self.task.queue:
            if not thread.is_alive():
                self.task.queue.remove(thread)
                self.task.task_done()
                self.task.put(new_thread)
                new_thread.start()
                return Response(response=json.dumps({f'Running order {order}': 'ok'}), status=202)

            return Response(
                response=json.dumps(
                    {'pedido feito espere': 'blabla'}
                ),
                status=429,
            )

    @staticmethod
    def teste():
        print(" hello word ")


