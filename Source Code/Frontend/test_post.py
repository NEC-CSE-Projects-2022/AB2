import requests

with open('sample_bulk.csv','rb') as f:
    r = requests.post('http://127.0.0.1:5000/api/predict/bulk', files={'file': f}, timeout=10)
print(r.status_code)
print(r.text)
