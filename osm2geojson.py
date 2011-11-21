#!/usr/bin/env python

import sys
import io
from imposm.parser import OSMParser
class Writer(object):
    def __init__(self, file):
        self.file = file

    def nodeToGEOJSON(self, node):
        id, tags, coords = node
        return '{"id": %d, "type":"Feature", "geometry": ' % id + self.geojsonPoint(coords) + ', "properties": ' + self.geojsonProperties(tags) + '}\n'

    def geojsonProperties(self, props):
        string = "{"
        for prop in props.items():
            (k, v) = prop
            string += '"%s":"%s"' % (k, v)
        return string + "}"

    def geojsonPoint(self, coords):
        return '{ "type":"Point", "coordinates": [%f, %f]}' % coords

    def geojsonNodes(self, nodes):
        for node in nodes:
           self.file.write(self.nodeToGEOJSON(node))

    def geojsonWays(self, ways):
        for way in ways:
            pass
            #print ways

with io.open('/dev/stdout', 'w') as file:
    writer = Writer(file)
    p = OSMParser(concurrency=4, nodes_callback=writer.geojsonNodes)
    p.parse('./berlin.osm.pbf')
#p.parse(sys.argv[1])
