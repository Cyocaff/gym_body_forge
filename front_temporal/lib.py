from jinja2 import Environment, FileSystemLoader, TemplateNotFound

env = Environment(loader=FileSystemLoader('templates'))

def view(self, path, context):
    try:
        template = env.get_template(path)
        rendered_content = template.render(context)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(rendered_content.encode())
    except TemplateNotFound:
        template = env.get_template('404.html')
        rendered_content = template.render({'message':f'Error 404, page {path} not found', 'error_404': True})
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(rendered_content.encode())
