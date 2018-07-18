#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   srv2gpx.py

   Hi!

   This script is used to convert NAD83 UTM
   waypoints found in a .srv file into a .gpx
   XML format. The conversion will allow any
   coordinates found in the .srv file to be
   read by a .gpx compliant GPS device and
   by mapping software like Google Maps.

   The script was built for the 2018
   Bisaro Anima caving expedition, but
   is usable to convert UTM in any similarly
   formated .srv file into a Lat/Lon .gpx
   format.

   Simply change line 44 to use the correct
   EPSG number for your UTM zone.

   -
   with love <3
   -

   Ethan Dinnen
"""

# Handles coordinate projection and conversion
import pyproj
# Handles escaping special characters following XML convensions
from xml.sax.saxutils import escape
# Handles getting current datetime
from datetime import datetime

# Initialize projection using EPSG 2153
# NAD83(CSRS98) / UTM Zone 11N
# Area of use: Canada south of 60 deg N and
# between 102 deg E and 114 deg W
# Alberta, British Columbia (accuracy: unknown)
p = pyproj.Proj(init='epsg:2153')

# Read the file line-wise
lines = [line.rstrip('\n') for line in open('./coords.srv')]

# Initialize the waypoints list
waypoints = []

# Parse our waypoints
for line in lines:
    # Split the line into an array for easy manipulation
    arr = line.split()
    # If the line is not empty
    if (len(arr) > 0):
        # If the line is a fix and not commented
        if (arr[0] == '#fix'):
            # Find the longitude and latitude from the UTMx and UTMy coords given
            lon, lat = p(float(arr[2]), float(arr[3]), inverse=True)
            # Find the name of the waypoint
            name = arr[1]
            # Find the recorded elevation
            elevation = arr[4]
            # Set the note to blank initially
            note = ''
            # If there is a note the string will be more than 5 words long
            if (len(arr) > 5):
                # The note is all words from word 5 onward, so...
                # Remove the ';' preceding the note
                arr[5] = arr[5][1:]
                # Join together all the words from word 5 to word 'n'
                # Then escape any special characters according to the XML standard
                note = escape(' '.join(arr[5:]))

            # Create the waypoint as a dict for easy referencing later
            wpt = {'lon': lon, 'lat': lat, 'name': name,
                   'elevation': elevation, 'note': note}
            # Append the waypoint to our array
            waypoints.append(wpt)

# Write the GPX file!
with open('./bisaro.gpx', 'w') as f:
    # Declare as an XML file
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    # Set up our GPX file and relevant namespaces
    f.write('<gpx version="1.0" creator="Ethan Dinnen" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0">\n')
    # Set the creation time to the time this script was run
    f.write('<time>{0}</time>\n'.format(datetime.utcnow()))
    # Set the name of the GPX file
    f.write('<name>Bisaro Anima</name>\n')
    # Loop over all our previously parsed waypoints
    for wpt in waypoints:
        # Create the waypoint element <wpt lat="x" lon="y" />
        f.write('<wpt lat="{0}" lon="{1}">\n'.format(wpt['lat'], wpt['lon']))
        # Set its elevation
        f.write('<ele>{0}</ele>\n'.format(wpt['elevation']))
        # Set its name
        f.write('<name>{0}</name>\n'.format(wpt['name']))
        # Set its note
        f.write('<desc>{0}</desc>\n'.format(wpt['note']))
        # Close the current waypoint
        f.write('</wpt>\n')
    # Clone the GPX file
    f.write('</gpx>')
