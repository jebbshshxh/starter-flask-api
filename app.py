from flask import Flask, request
import requests
import json
try:
  from bs4 import BeautifulSoup
except:
  import os
  os.system('pip install bs4')

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

@app.route('/bs/<string:tag>/stats')
def bs_stats(tag):
  page = requests.get(f'https://brawltime.ninja/profile/{tag}')
  doc = BeautifulSoup(page.text, 'html.parser')

  profile = doc.find(id='aside')

  pic = profile.find('img')['src'].replace('200', '50')
  name = profile.findAll('span')[0].text
  name_color = profile.findAll('span')[0]['style'].replace('color:', '').replace(';', '')
  try:
    club = profile.findAll('span')[2].text
  except:
    club = None
  data = profile.findAll('dd')
  if len(data) == 9:
    trophies = data[3].text.replace(' ', '')
    highest = data[4].text.replace(' ', '')
    exp = data[5].text.replace(' ', '')
    trio = data[6].text.replace(' ', '')
    solo = data[7].text.replace(' ', '')
    duo = data[8].text.replace(' ', '')
  elif len(data) == 8:
    trophies = data[2].text.replace(' ', '')
    highest = data[3].text.replace(' ', '')
    exp = data[4].text.replace(' ', '')
    trio = data[5].text.replace(' ', '')
    solo = data[6].text.replace(' ', '')
    duo = data[7].text.replace(' ', '')

  output = {
    	'pic': pic,
    	'name': name,
    	'name_color': name_color,
    	'tag': tag,
    	'club': club,
    	'trophies': trophies,
    	'highest': highest,
    	'exp': exp,
    	'trio': trio,
    	'solo': solo,
    	'duo': duo
    }
  return output
