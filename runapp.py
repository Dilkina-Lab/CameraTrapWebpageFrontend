import argparse
import sys
import bottle
import csv
import json
import pandas as pd
import nest_asyncio
import os
import time

import sys

# Add the directory to the search path
sys.path.insert(1,'/Users/nicolerussack/PycharmProjects/CameraTrapWebpge/CameraTrapWebpageBackend/scrpy/src')
print(sys.path)
import simulate_estimate



# Import the function "my_function" from the file "my_module.py"
# print(simulate_estimate.testFunction())

#add nest_asyncio to avoid RuntimeError: This event loop is already running
nest_asyncio.apply()

#--------some stuff needed to get AJAX to work with bottle?--------#
def enable_cors():
    '''
    From https://gist.github.com/richard-flosi/3789163
    This globally enables Cross-Origin Resource Sharing (CORS) headers for every response from this server.
    '''
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a web user interface for labeling camera trap images for classification.')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Web server host to bind to.')## default='localhost', help='Web server host to bind to.')
    parser.add_argument('--port', type=int, default=8081, help='Web server port port to listen on.')
    args = parser.parse_args(sys.argv[1:])


    # -------------------------------------------------------------------------------- #
    # CREATE AND SET UP A BOTTLE APPLICATION FOR THE WEB UI
    # -------------------------------------------------------------------------------- #

    webapp = bottle.Bottle()
    webapp.add_hook("after_request", enable_cors)
    webapp_server_kwargs = {
        "server": "tornado",
        "host": args.host,
        "port": args.port
    }

    @webapp.route('/')
    def index():
        return bottle.static_file("index.html", root='static/html')

    # @webUIapp.route('/<filename:re:raster\/test2.tiff>')
    # def send_tiff(filename):
    #     return bottle.static_file(filename, root='static')

    ## dynamic routes
    @webapp.route('/getCSV', method='POST')
    def getCSV():
        print("In get CSV")
        # data = bottle.request.json
        # with open('location_data_lat_long.csv') as csvfile:
        #     readCSV = csv.reader(csvfile, delimiter=',')
        #     count = 0
        #     data['locations'] = []
        #     for row in readCSV:
        #         data['locations'].append([row[0], row[1], row[2]])
        #         print(row[0], row[1], row[2])
        # bottle.response.content_type = 'application/json'
        # bottle.response.status = 200
        # print(type(data))
        # return data
        data = bottle.request.json
        #print('point one')
        # print(data)
        with open('sebangau_activity_center_summary.csv') as csvfile:
        #with open('sebangau_real_layout_caphist_summary.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            count = 0
            result = {}
            result['locations'] = []
            for row in readCSV:
                result['locations'].append([row[0], row[1], row[2]])
                print(row[0], row[1], row[2])
        bottle.response.content_type = 'application/json'
        bottle.response.status = 200
        return result

    # data is of type list
    # s is of type string because json.dumps take a Python object and turns it into JSON string
    # apparently, needed to return something of type string in order to go into success in ajax call
    @webapp.route('/savetoCSV', method='POST')
    def savetoCSV():
        data = bottle.request.json
        s = json.dumps(data)
        df = pd.read_json(s)
        df.to_csv('markers.csv')
        bottle.response.content_type = 'application/json'
        bottle.response.status = 200
        return s


    @webapp.route('/writeConfigFile', method='POST')
    def writeConfigFile():
        print("In write config file")
        data = bottle.request.json
        s = json.dumps(data)
        print("this is the data " + s)
        df = pd.read_json(s)
        df.to_csv('config.csv')
        bottle.response.content_type = 'application/json'
        bottle.response.status = 200
        return s


    @webapp.route('/analyzeLocations', method='POST')
    def analyzeLocations():
        print("in analyzeLocations")
        data = simulate_estimate.testFunction()
        # with open(filename) as f:
        #     code = f.read()
        #
        # a = exec(code)
        print("This is the reusel " + str(data))
        return data



    webapp.run(**webapp_server_kwargs)