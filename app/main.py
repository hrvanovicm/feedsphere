import falcon

from wsgiref.simple_server import make_server
from app.api.v1 import actuator
from app.config import PORT, HOST

app = falcon.App()

if __name__ == "__main__":
    app.add_route("/actuator", actuator.ActuatorResource())
    with make_server(HOST, int(PORT), app) as httpd:
        print("Serving at {}:{}".format(HOST, PORT))
        httpd.serve_forever()
