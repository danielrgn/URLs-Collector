from cloudant import Cloudant

import os
import json


def config_db():
    db_name = 'mydb'
    client, db = None, None

    if 'VCAP_SERVICES' in os.environ:
        vcap = json.loads(os.getenv('VCAP_SERVICES'))
        print('Found VCAP_SERVICES')
        if 'cloudantNoSQLDB' in vcap:
            creds = vcap['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
    elif "CLOUDANT_URL" in os.environ:
        client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'],
                          url=os.environ['CLOUDANT_URL'], connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
    elif os.path.isfile('vcap-local.json'):
        with open('vcap-local.json') as f:
            vcap = json.load(f)
            print('Found local VCAP_SERVICES')
            creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)

    return client, db


client, db = config_db()


def get_document(_id):
    doc = None

    if client and _id is not None:
        doc = db[_id]
    
    return doc


def create_document(data):
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
    return data


def close_connection():
    if client:
        client.disconnect()
