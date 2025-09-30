from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
import json 
import crud_alumno
import crud_docente

port = 3000

crudAlumno = crud_alumno.crud_alumno()
crudDocente = crud_docente.crud_docente()

class miServidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/":
            self.path="index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        if self.path=="/alumnos":
            alumnos = crudAlumno.consultar("")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(alumnos).encode('utf-8'))
        if self.path=="/docentes":
            docentes = crudDocente.consultar("")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(docentes).encode('utf-8'))
    
    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        datos = parse.unquote(datos)
        datos = json.loads(datos)
        
        if self.path == "/alumnos":
            resp = {"msg": crudAlumno.administrar(datos)}
        elif self.path == "/docentes":
            resp = {"msg": crudDocente.administrar(datos)}
        else:
            resp = {"msg": "Ruta no encontrada"}
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode("utf-8"))

print("Servidor ejecutandose en el puerto", port)
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()