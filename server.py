from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import socketserver


names_dict = {'junhyung': 'bae',
              'hojung': 'jeong'}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_message("GET 요청을 처리합니다")
        try:
            name = parse_qs(self.path[2:])['name'][0]
        except:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
            return

        if name in names_dict.keys():
            self.send_response_to_client(200, names_dict[name])
        else:
            self.send_response_to_client(404, 'Can not find name.')
            self.log_message("이름을 찾을 수 없습니다.")

    def do_POST(self):
        self.log_message('POST 요청을 처리합니다.')
        data = parse_qs(self.path[2:])
        try:
            names_dict[data['name'][0]] = data['last_name'][0]
            self.send_response_to_client(200, names_dict)
        except KeyError:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")

    def do_DELETE(self):
        self.log_message('DELETE 요청을 처리합니다.')
        try:
            name = parse_qs(self.path[2:])['name'][0]
        except KeyError:
            self.send_response_to_client(404, self.path[2:])
            self.log_message("Incorrect parameters provided")
            return
            
        for key, value in names_dict.items():
            if name in names_dict.keys() or names_dict.values():
            
                if key == name:
                    del names_dict[key]
                    self.send_response_to_client(200, f'deleted complete, current dict: {names_dict}')
                    self.log_message("삭제 완료")
                    break
                elif value == name:
                    del names_dict[key]
                    self.send_response_to_client(200, f'deleted complete, current dict: {names_dict}')
                    self.log_message("삭제 완료")
                    break
        else:
            self.send_response_to_client(404, 'Can not find name.')
            self.log_message("이름을 찾을 수 없습니다.")

    def send_response_to_client(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(str(data).encode())


host = '127.0.0.1'
port = 8080

with socketserver.TCPServer((host, port), RequestHandler) as httpd:
    print("{}:{} 에서 서버 작동중.....".format(host, port))
    httpd.serve_forever()
