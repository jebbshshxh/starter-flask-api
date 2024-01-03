from flask import Flask, request
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
  return 'Hello from Flask!'


@app.route('/emulate')
def emulate():
  try:
    url = str(request.args.get('url'))
    domain = str(request.args.get('domain'))
    data = str(request.args.get('data'))
    data = json.loads(data)
    resp = requests.post(url, data=data)
    return resp.text.replace('href="/',
                             f'href="{domain}/').replace(
                                 'src="/', f'src="{domain}/')
  except Exception as _ex:
    return f'{_ex}'
