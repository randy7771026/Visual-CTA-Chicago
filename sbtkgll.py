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

my_latitude = 41.878493
my_longitude = -87.631173

# OK so moving to another imperfect solution I will get a mac address and then see if openbmap can get me
# my lat and lon within reason

from uuid import getnode as get_mac
mac = get_mac()

print 'mac addy is',mac,'hex', hex(mac).upper() 

from xml.etree.ElementTree import parse


def distance(lat1, lat2):
    """
    Return distance in miles between two lats
    """
    return 60*abs(lat1 - lat2)

# This may not change as often as we would like but I am running with it for now since it seems to give me the routes
# some buses may not run on a given day or at a given time so this may need more than a few iterations of tweaks
# one will have to set up error handling here.  Got a file empty but ran great second time.

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

def closest_stop(gort):



# http://chicago.transitapi.com/bustime/map/getRoutePoints.jsp?route=80
    call = 'http://chicago.transitapi.com/bustime/map/getRoutePoints.jsp?route='

    call = call + gort

# print call

# url has been built but will not open
# Neat, Norbert fixed that
# Now to find the closest stop

    s = urllib2.urlopen(call)
# s = urllib2.urlopen(' http://chicago.transitapi.com/bustime/map/getRoutePoints.jsp?route=80')
    docs = parse(s)

    cstop = ''
    clat  = 0.0
    clon  = 0.0
    cstopdis = 100.00

    pa_elements = docs.findall('.//pa')
    for pa in pa_elements:
        rection = pa.findtext('.//d')
#   print 'rection', rection, 'pd', god[go]
        if rection == god[go]:
            pt_elements = pa.findall('.//pt')
            for pt in pt_elements:    
                bs_elements = pt.findall('.//bs')
                for bs in bs_elements:
      	            if len(bs_elements) != 0:
	                bs = bs_elements[0]
	                stopflat = pt.findtext('.//lat')
       	                stopflon = pt.findtext('.//lon')
                        stop = bs.findtext('.//id')
                        ints = bs.findtext('.//st')
#                    print 'stop', stop, 'lat', stopflat, 'lon', stopflon
                        stopflat = float(stopflat)
                        stopflon = float(stopflon)
                        starc = distance_on_unit_sphere(my_latitude, my_longitude, stopflat, stopflon)
                        stmiles = starc * 3960.0
                        if stmiles < cstopdis:
                            cstopdis = stmiles
                            cstop = stop
                            intersection = ints
# print 'cstopdis', cstopdis, 'cstop', cstop, 'intersection', intersection  

    print ' '  

    print 'Your closest stop for route ', gort, ' headed ', god[go], ' is stop ', cstop

#    print ' '

    print 'That stop is at ', intersection, ' ', cstopdis, ' miles away'   

#    print ' ' 
    return cstop    
                 
#            dis = distance(lon, my_longitude)

# code to call url for bus arrivals

# http://chicago.transitapi.com/bustime/map/getStopPredictions.jsp?stop=5623&route=80
call = 'http://chicago.transitapi.com/bustime/map/getStopPredictions.jsp?stop='

for route in routes:
    closest_stop(route)

print 'routes ', routes, 'headed ', god[go]

gort = raw_input('Enter route and press Enter >>> ')

cstop = closest_stop(gort)

# will need to verify route entered correctly
# get stops for routes saved
# find stops within one mile
# and find the ones closest in the direction you want to go.

callstop = call + cstop + '&route=' + gort

# print callstop

# url has been built 





def monitor():

    arvs = urllib2.urlopen(callstop)
    docarvs = parse(arvs)
    
    for pre in docarvs.findall('pre'):
        vid = pre.findtext('v')
        eta = pre.findtext('pt')
        print 'Bus number ', vid, 'will arrive in ', eta
        print '---'
                           

    print '_'*10
import time
count = 0
while count < 60 :
    monitor()
    count = count + 1
    time.sleep(60)
