# -*- coding: utf-8 -*-
"""
Created on Wed May 17 08:36:40 2017

@author: Lucien
"""
import speedtest
import argparse
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import os
import httplib2

APPLICATION_NAME = __file__
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


class GoogleSheetsWrapper:
    def __init__(self, secrets, flags):
        self.secrets = secrets
        self.flags = flags
        
        self.creds = self.get_credentials()
        self.service = self.get_service()
        
    def get_credentials(self):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       __file__ + '.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.secrets, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, self.flags)
  
        return credentials
    
    def get_service(self):
        http = self.creds.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        return service
    
    def add_row(self, values):
        rangeName = 'Data!A2:D'
    
        values = [
            values
        ]
        body = {'values' : values}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=args.sheet_id, body=body, range=rangeName, 
            valueInputOption='USER_ENTERED').execute()

        


def get_bandwidth():
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    d = s.results.dict()
    results = {}
    results['upload'] = d['upload']
    results['download'] = d['download']
    results['ping'] = d['ping']
    results['timestamp'] = datetime.datetime.now().strftime("%x %X") # d['timestamp']
    return results


if __name__ == "__main__":
    argp = argparse.ArgumentParser(parents=[tools.argparser])
    argp.add_argument("--client_secret", type=str, 
                      default='client_secret.json', 
                      help="JSON file containing Google API keys")
    argp.add_argument('--sheet_id', type=str, 
                      default='1IHM1fiR1v1l8flve0yOs_DPS5f20K5O88HC9wIFCTvA', 
                      help="Google Sheet ID")
    args = argp.parse_args()
     
    g = GoogleSheetsWrapper(args.client_secret, args)
    
    bw = get_bandwidth()
    values = [bw['timestamp'], bw['ping'], bw['upload'], bw['download']]
    g.add_row(values)

