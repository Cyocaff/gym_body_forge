import http.server
import socketserver
import os
from lib import view
PORT = 8003
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path[0:7] == '/static':
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        if not self.headers.get('x-requested-with') == 'XMLHttpRequest':
            return view(self,'/base.html',{'load_data': True})
        if self.path == '/':
            self.path = '/base.html'
        return view(self,f'{self.path}.html',{'message':'hello',
                   'message2':'world'  
                   })
socketserver.TCPServer.allow_reuse_address = True  
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()

