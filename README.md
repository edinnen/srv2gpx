# SRV to GPX

Hi!

This script is used to convert NAD83 UTM waypoints found in a .srv file into a .gpx XML format. The conversion will allow any coordinates found in the .srv file to be read by a .gpx compliant GPS device and by mapping software like Google Maps.

The script was built for the 2018 Bisaro Anima caving expedition, but is usable to convert UTM in any similarly formated .srv file into a Lat/Lon .gpx format.

Simply change line 44 in srv2gpx.py to use the correct EPSG number for your UTM zone.
