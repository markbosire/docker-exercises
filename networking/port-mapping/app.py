import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, service_name, port, *args, **kwargs):
        self.service_name = service_name
        self.port = port
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = f'''
        <h1>{self.service_name}</h1>
        <p>Running on container port {self.port}</p>
        <p>Service: {self.service_name}</p>
        <hr>
        <p>Try the other services:</p>
        <ul>
            <li><a href="http://localhost:3000">Web App (port 3000)</a></li>
            <li><a href="http://localhost:4000">API (port 4000)</a></li>
            <li><a href="http://localhost:5000">Admin (port 5000)</a></li>
        </ul>
        '''
        self.wfile.write(html.encode())

def run_server(service_name, port):
    handler = lambda *args, **kwargs: MyHandler(service_name, port, *args, **kwargs)
    with HTTPServer(("", port), handler) as httpd:
        print(f"{service_name} running on port {port}")
        httpd.serve_forever()

# Start three services on different ports
services = [
    ("Web App", 8000),
    ("API Service", 8001), 
    ("Admin Panel", 8002)
]

# Run first two services in background threads
for service_name, port in services[:-1]:
    thread = threading.Thread(target=run_server, args=(service_name, port), daemon=True)
    thread.start()

# Run the last service in main thread
run_server(services[-1][0], services[-1][1])