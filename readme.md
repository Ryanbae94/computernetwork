# TCP 소켓 통신을 사용한 HTTP 프로토콜
---
## 1. 동작환경
+ OS : Windows 11
+ Server : python의 http.server 모듈 사용
+ Client : python의 requests 모듈 사용

## 2. 프로그램 개요
1. 서버에 이름, 성을 담는 딕셔너리를 구현
```python
names_dict = {'junhyung': 'bae',
              'hojung': 'jeong'}
```
2. 클라이언트로부터 GET, POST, DELETE 요청을 받을 시 그에 해당하는 응답 코드, 응답 데이터, 로그 메세지를 출력
3. 가산점을 위한 추가구현 내용

+ 서버의 실제 데이터와 상호작용이 가능하도록 구현
+ GET 요청 시 서버의 딕셔너리에서 읽어온 내용 반환 (6-1, 6-2)
+ POST 요청 시 파라미터값을 서버의 딕셔너리에 추가 (6-1, 6-2)
+ DELETE 요청 시 파라미터 값을 서버의 딕셔너리에서 삭제 (6-1, 6-2)
+ 와이어샤크 패킷 트래킹 (6-3)

## 3. TCP 소켓 서버 구현 (server.py)
```python
host = '127.0.0.1'
port = 8080

with socketserver.TCPServer((host, port), RequestHandler) as httpd:
    print("{}:{} 에서 서버 작동중.....".format(host, port))
    httpd.serve_forever()
```

 로컬 호스트에 서버를 구현하였으며, socketserver 모듈의 TCPserver메소드를 통해 TCP서버를 구현하였습니다.

## 4. HTTP Request Handler 구현 (server.py)
**4-1. 클라이언트에 결과값을 전달하는 메소드 구현**

```python
    def send_response_to_client(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(str(data).encode())
```
**4-2. GET 메소드 구현**


```python
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
```

**4-3. POST 메소드 구현**
```python
    def do_POST(self):
        self.log_message('POST 요청을 처리합니다.')
        data = parse_qs(self.path[2:])
        try:
            names_dict[data['name'][0]] = data['last_name'][0]
            self.send_response_to_client(200, names_dict)
        except KeyError:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
```

**4-4. DELETE 메소드 구현**
```python
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
```


## 5. 클라이언트 구현 (client.py)
```python
import requests

r = requests.get("http://127.0.0.1:8080/", params={"name": 'junhyung'})
print("요청 메소드: GET")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
print()

r = requests.post("http://127.0.0.1:8080/",
                  params={'name': 'sangki', 'last_name': 'oh'})
print("요청 메소드: POST")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
print()

r = requests.post("http://127.0.0.1:8080/",
                  params={'name': 'keunho', 'last_name': 'byun'})
print("요청 메소드: POST")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
print()

r = requests.delete("http://127.0.0.1:8080/",
                    params={'name': 'sangki'})
print("요청 메소드: DELETE")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
print()

r = requests.get("http://127.0.0.1:8080/", params={"name": 'sangki'})
print("요청 메소드: GET")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
```
## 6. 실행결과
**6-1. server.py**

![server](https://user-images.githubusercontent.com/62899939/166221907-0ab39d2c-0d78-4abe-9664-0fe3ca24c51e.png)


**6-2. client.py**

![client](https://user-images.githubusercontent.com/62899939/166221875-44a01fee-2fa2-4560-8fc5-f99a12fe5bd4.png)


**6-3. wireshark 패킷 트래킹**

![wireshark](https://user-images.githubusercontent.com/62899939/166188997-36519f9d-91fc-4c25-afbe-bf13f7c99a0f.png)



## 7. 소스코드
**server.py**
```python
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

```
**client.py**
```python
import requests

r = requests.get("http://127.0.0.1:8080/", params={"name": 'junhyung'})
print("요청 메소드: GET")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
print()

r = requests.post("http://127.0.0.1:8080/",
                  params={'name': 'sangki', 'last_name': 'oh'})
print("요청 메소드: POST")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
print()

r = requests.post("http://127.0.0.1:8080/",
                  params={'name': 'keunho', 'last_name': 'byun'})
print("요청 메소드: POST")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
print()

r = requests.delete("http://127.0.0.1:8080/",
                    params={'name': 'sangki'})
print("요청 메소드: DELETE")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
print()

r = requests.get("http://127.0.0.1:8080/", params={"name": 'sangki'})
print("요청 메소드: GET")
print("응답코드: {}".format(r.status_code))
print("응답 데이터: {}".format(r.text))
```