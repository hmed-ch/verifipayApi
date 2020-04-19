#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_pymongo import PyMongo

    


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')

    
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Verifi API'})
    app.run(port=8080)
    

