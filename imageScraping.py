import glob
import json
import re
import os
import shutil
from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

absFilePath = os.path.abspath(__file__)

fileDir = os.path.dirname(os.path.abspath(__file__))

targetDir = fileDir + "\logs" 

lista = []

def get_items(tentativi, s , previous_s):
  os.chdir(targetDir)
  read_files = glob.glob("*.json")
  s = ""
  for f in read_files :
    if (f!= "photosresult.json") and open(f, "r").read(1) :
      with open(f, "r") as forz:
        obj_json = json.load(forz)
        if(len(obj_json)==0):
          tmp = re.sub('\.json$','',f)
          s = s + tmp + ","
        else :
          lista.append(f)
  s = s[:-1]
  if s != previous_s :
    tentativi = 5
    previous_s = s
  else :
    tentativi = tentativi - 1
  check(tentativi, s, previous_s)


def check(tentativi,string_query, previous_query):
  global response
  if (string_query == "" or tentativi == 0):
    return
  else:
    os.chdir(fileDir)
    arguments = {"keywords": string_query, "limit":2, "no_download" : True , "extract_metadata" : True}
    response.download(arguments)
    get_items(tentativi, string_query, previous_query)


def start(input_list):
  s = "";
  for i in range(len(input_list)) :
    s = s + input_list[i] + ","
  s = s[:-1]
  arguments = {"keywords": s, "limit":2, "no_download" : True , "extract_metadata" : True}
  response.download(arguments)

def join_items():
  os.chdir(targetDir)
  with open('photosresult.json', 'w') as f:
    f.write("{\n")
    for j in range(len(lista)):
      cerca = lista[j]
      with open(cerca, 'r') as fi :
        obj = json.load(fi)
        cerca = re.sub('\.json$','',cerca)
        newDict = {"name" : cerca, "photos" : obj}
        result_json = json.dumps(newDict, indent=2)
        f.write('%s'%result_json)
        f.write(",\n")
    f.write("}\n")
  shutil.move(targetDir+"\photosresult.json" , fileDir+"\photosresult.json")
  os.chdir(fileDir)

def unique_items_on_list():
  global lista
  temp = set(lista)
  lista = list(temp)
  

def remove_logs_folder_and_result_file():
  if os.path.isdir('./logs'):
    shutil.rmtree(targetDir)
  if os.path.exists('photosresult.json'):
    os.remove('photosresult.json')

input_list = ['AI SOLTERI DR. ANDREA GADOTTI', 'ALLA MADONNA DR. GIANMARCO CASAGRANDE', 'BETTA DR. MARCO',
              'BOLGHERA TRENTO', 'CAMPAGNOLO DR.A VIRGINIA', 'COMUNALE 1 SAN GIUSEPPE', 'COMUNALE 10 COGNOLA', 'COMUNALE 2 AL SAN CAMILLO',
              'COMUNALE 3 SAN PIO X', 'COMUNALE 4 CLARINA', 'COMUNALE 5 SAN DONA', 'COMUNALE 6 POVO', 'COMUNALE 7 MEANO', 'COMUNALE 8 MADONNA BIANCA',
              'COMUNALE 9 PIEDICASTELLO', 'CRISTO RE DR.A MARCELLA FONTANA', "DALL'ARMI DR.I PATTINI", 'DE BATTTAGLIA DR.E SANDRA E GIULIANA BONI', 'DE GERLONI DR. PIER FRANCESCO',
              'DI GARDOLO DR. RENATO BRANDOLANI', 'DISPENSARIO DI NOGAREDO', 'FRANZELLIN DR. VITTORIO ALA 2^ SEDE', 'GALLO DR. LAMBERTO', 'GMG DR.I RAVAGNANI E AGAZZANI',
              'GRANDI DR. MARCO LEPORE', 'IGEA DR. MAHLOUL EL ZENNAR MOHAMMAD', 'LA DI RONCAFORT', 'MARTIGNANO DR.A FRANCESCA FERRI', 'MATTARELLO DR. GIUPPONI',
              'SAN BARTOLAMEO DR. C. BERTOLINI', 'SAN LORENZO DR. BRUNO BIZZARO', 'SANTA CHIARA DR.I ALESSIA ED EDOARDO ABBONDI', 'VILLAZZANO DR. PAOLO BOLEGO']    

remove_logs_folder_and_result_file()
start(input_list)
get_items(5, "", "")
unique_items_on_list()
join_items()






