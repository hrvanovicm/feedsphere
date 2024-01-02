from wsgiref.simple_server import make_server
import falcon

app = falcon.App()

if __name__ == "__main__":
    with make_server('', 5000, app) as httpd:
        print("Serving at port", 5000)
        httpd.serve_forever()
