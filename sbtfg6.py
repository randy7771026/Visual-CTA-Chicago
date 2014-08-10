import urllib, time
from xml.etree.ElementTree import parse
def r76museum():
    p = urllib.urlopen('http://chicago.transitapi.com/bustime/map/getStopPredictions.jsp?stop=17413&route=76')
    pdoc = parse(p)
    for pre in pdoc.findall('pre'):
        vid = pre.findtext('v')
        eta = pre.findtext('pt')
        print '76 Diversy to Museum Bus number ', vid, 'will arrive in ', eta
        print '---'
def r76harlem():
    p = urllib.urlopen('http://chicago.transitapi.com/bustime/map/getStopPredictions.jsp?stop=11071&route=76')
    pdoc = parse(p)
    for pre in pdoc.findall('pre'):
        vid = pre.findtext('v')
        eta = pre.findtext('pt')
        print '76 Diversy to Harlem Bus number ', vid, 'will arrive in ', eta
        print '---'
def r82north():
    p = urllib.urlopen('http://chicago.transitapi.com/bustime/map/getStopPredictions.jsp?stop=11267&route=82')
    pdoc = parse(p)
    for pre in pdoc.findall('pre'):
        vid = pre.findtext('v')
        eta = pre.findtext('pt')
        print '82 Kimball North Bus number ', vid, 'will arrive in ', eta
        print '---'
def r82south():
    p = urllib.urlopen('http://chicago.transitapi.com/bustime/map/getStopPredictions.jsp?stop=11143&route=82')
    pdoc = parse(p)
    for pre in pdoc.findall('pre'):
        vid = pre.findtext('v')
        eta = pre.findtext('pt')
        print '82 Kimball South Bus number ', vid, 'will arrive in ', eta
        print '---'
def r56loop():
    p = urllib.urlopen('http://chicago.transitapi.com/bustime/map/getStopPredictions.jsp?stop=17413&route=56')
    pdoc = parse(p)
    for pre in pdoc.findall('pre'):
        vid = pre.findtext('v')
        eta = pre.findtext('pt')
        print '56 Milwaukee to Loop Bus number ', vid, 'will arrive in ', eta
        print '---'
def r56jeff():
    p = urllib.urlopen('http://chicago.transitapi.com/bustime/map/getStopPredictions.jsp?stop=5562&route=56')
    pdoc = parse(p)
    for pre in pdoc.findall('pre'):
        vid = pre.findtext('v')
        eta = pre.findtext('pt')
        print '56 Milwaukee to Jefferson Park Bus number ', vid, 'will arrive in ', eta
        print '---'
    print '_'*10

count = 0
while count < 60 :
    r76harlem()
    r76museum()
    r82north()
    r82south()
    r56loop()
    r56jeff()
    count = count + 1
    time.sleep(60)
