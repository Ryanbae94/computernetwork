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