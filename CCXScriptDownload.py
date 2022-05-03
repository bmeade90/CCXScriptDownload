import sys
import requests
import logging
import warnings
from requests.auth import HTTPBasicAuth
import json


def main(argv):
   warnings.filterwarnings("ignore")
   hostname = ''
   username = ''
   password = ''
   
   try:
      hostname = sys.argv[1]
      username = sys.argv[2]
      password = sys.argv[3]

   except:
      print('Please enter hostname/IP Address, username, and password')
      sys.exit()
	
   logging.basicConfig(filename='CCXScriptDownload.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

   #Create a new session to maintain cookies across requests      
   s = requests.Session()
   
   headers= {"Accept": "Application/JSON"}

   script_list_request = s.get('https://' + hostname + '/adminapi/script', verify=False, auth=HTTPBasicAuth(username,password),headers=headers)
   script_list_json = json.loads(script_list_request.text)
   for script in script_list_json["Script"]["File"]:
      script_download = s.get('https://' + hostname + '/adminapi/script/download//default' + script["path"] + script["FileName"], verify=False, auth=HTTPBasicAuth(username,password))
      with open(script["FileName"], 'wb') as f:
         f.write(script_download.content)
      logging.debug(script["path"] + script["FileName"] + " successfully downloaded")


if __name__ == "__main__":
     #Replace the below values or pass the commands through the command-line and remove the below line
     sys.argv = ["CCXScriptDownload.py", "ccx01.example.com","ccxadmin", "mypassword"]
     main(sys.argv[1:])