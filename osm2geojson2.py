#!/usr/bin/env python

import sys
import json
import urllib2

from imposm.parser import OSMParser

def nodeToGEOJSON(node):
    id, tags, (lon, lat) = node
    pojo = { 'id': id, 'geometry': { 'type': 'Point', 'coordinates': [lon, lat] } , 'properties': tags }
    return pojo
    #return '{"id": %d, "type":"Feature", "geometry": ' % id + self.geojsonPoint(coords) + ', "properties": ' + self.geojsonProperties(tags) + '}\n'

def geojsonProperties(self, props):
    string = "{"
    for prop in props.items():
        (k, v) = prop
        string += '"%s":"%s"' % (k, v)
    return string + "}"

def geojsonPoint(coords):
    return '{ "type":"Point", "coordinates": [%f, %f]}' % coords

def geojsonNodes(nodes):
    data = []
    for node in nodes:
       data.append(nodeToGEOJSON(node))
    #url = 'http://db.osm.spline.de:5984/osm/_bulk_docs'
    url = 'http://localhost:5984/osm/_bulk_docs'
    req = urllib2.Request(url, json.dumps({'docs': data}), {'Content-Type':'application/json'})
    print req
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()




def geojsonWays(ways):
    for way in ways:
        pass
        #print ways

p = OSMParser(concurrency=4, nodes_callback=geojsonNodes)
p.parse('./berlin.osm.pbf')
#p.parse(sys.argv[1])
