import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from datetime import datetime, timedelta
import dateutil.parser
import pytz
import click
import time

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

client_id = '33467c23-fada-4405-8a5b-33ee38169273'
client_secret = '&O97/<>sWmmUrI2KctxxVf9iCQi*~eN|:I6R%o6:'
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
hed = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type' : 'client_credentials'
}

token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token', client_id=client_id, client_secret=client_secret)
hed = {
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': 'Bearer '+token['access_token']
}

urlS = 'https://services.sentinel-hub.com/configuration/v1/wms/instances'
reponses = requests.request("GET", urlS, headers=hed)
instances = reponses.json()

now = datetime.now()
yesterday = datetime(now.year, now.month, now.day)
yesterday -= timedelta(days=1)  #Ayer
yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999) # TIEMPO
#yesterday = yesterday.replace(hour=17, minute=59, second=59, microsecond=999999) # TIEMPO
print(pytz.utc.localize(yesterday))
count = 0
arrInstancesDel = []
for instance in instances:
    if instance['name'] == 'Polygons4GraficosType2Tmp':
        if dateutil.parser.parse(instance['created']) < pytz.utc.localize(yesterday):
            print(instance['name'], '-', dateutil.parser.parse(instance['created']), '- Ayer', instance['id'])
            count +=1
            arrInstancesDel.append(instance['id'])
        #else:
        #    print(instance['name'], '-', dateutil.parser.parse(instance['created']), '- HOY', instance['id'])
print('Se han detectado', len(arrInstancesDel), ' Instancias para elminar anterioes a la fecha ', pytz.utc.localize(yesterday))
if click.confirm('Quieres eliminarlas?', default=True):
    l = len(arrInstancesDel)
    printProgressBar(0, l, prefix = 'Progreso:', suffix = 'Completado', length = 50)
    for i, instance in enumerate(arrInstancesDel):
        time.sleep(0.1)
        # Update Progress Bar
        urlS = 'https://services.sentinel-hub.com/configuration/v1/wms/instances/'+instance
        requests.request("DELETE", urlS, headers=hed)
        printProgressBar(i + 1, l, prefix = 'Progreso:', suffix = 'Completado', length = 50)
