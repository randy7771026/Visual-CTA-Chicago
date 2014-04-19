import urllib2

# From John D. Cook dot Com
# Compute an arc between two pairs of lat lons

import math


god = {'n': 'Northbound', 's': 'Southbound', 'e': 'Eastbound', 'w': 'Westbound'}

go = raw_input('Input n, s, e or w and press Enter >>> ')
#   print god[go]


def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc

# 4886 W Irving Park

my_latitude = 41.953394
my_longitude = -87.749884

from xml.etree.ElementTree import parse


def distance(lat1, lat2):
    """
    Return distance in miles between two lats
    """
    return 60*abs(lat1 - lat2)

# This may not change as often as we would like but I am running with it for now since it seems to give me the routes
# some buses may not run on a given day or at a given time so this may need more than a few iterations of tweaks

u = urllib2.urlopen('http://chicago.transitapi.com/bustime/map/getBusesForRouteAll.jsp')
doc = parse(u)

routes = []


for bus in doc.findall('bus'):
    flat = float(bus.findtext('lat'))
    flon = float(bus.findtext('lon'))
    rt = bus.findtext('rt')

# possible distance use

    d = bus.findtext('d')
    dd = bus.findtext('dd')
    dn = bus.findtext('dn')
    pid = bus.findtext('pid')
    pd = bus.findtext('pd')
#    print 'lat', lat, 'lon', lon, 'rt', rt
#    print 'd', d, 'dd', dd, 'dn', dn, 'pid', pid, 'pd', pd

# If lat dist and lon dist less than 1.0 miles
# get route
# save route if not saved

    rarc = distance_on_unit_sphere(my_latitude, my_longitude, flat, flon)
    miles = rarc * 3960.0

    if miles <= 1.0:
#        print 'flat', flat, 'flon', flon, 'rt', rt
#        print 'd', d, 'dd', dd, 'dn', dn, 'pid', pid, 'pd', pd
        if god[go] == pd:
#           print 'match for ', pd
            if rt not in routes:
                routes = routes + [rt]

print 'routes ', routes, 'headed ', god[go]

gort = raw_input('Enter route and press Enter >>> ')

# will need to verify route entered correctly
# get stops for routes saved
# find stops within one mile
# and find the ones closest in the direction you want to go.

# http://chicago.transitapi.com/bustime/map/getRoutePoints.jsp?route=80
call = 'http://chicago.transitapi.com/bustime/map/getRoutePoints.jsp?route='

call = call + gort

print call

# url has been built but will not open

s = urllib2.urlopen(call)
# s = urllib2.urlopen(' http://chicago.transitapi.com/bustime/map/getRoutePoints.jsp?route=80')
docs = parse(s)

pa_elements = docs.findall('.//pa')
for pa in pa_elements:
    rection = pa.findtext('.//d')
    print 'rection', rection, 'pd', god[go]
    if rection == god[go]:
        bs_elements = pa.findall('.//bs')
        for bs in bs_elements:
            stop = bs.findtext('.//id')
            print stop
#            dis = distance(lon, my_longitude)
