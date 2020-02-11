import math
import ephem
from tabulate import tabulate

#Input: hs, ie, hoe, wt, we, Celestial Body (Sun is default), lat, long

#todo: validate that degrees < 360 and minutes < 60
class Arc: #Used for Hs, Ho, GHA, and LHA. Lat, Long, Dec and IE have a direction specified
    def __init__(self, degrees, minutes, direction = None):
        if direction == 's' or direction == 'w' or direction == 'on':
            degrees = -1 * degrees
            minutes = -1 * minutes
        self.degrees = degrees
        self.minutes = minutes
    def __str__(self):
        return str(self.degrees) + u'\N{DEGREE SIGN} ' + str(self.minutes) + '\''

#converts pyephem arc to radians   
def ephemrad(arc):
    d = int(math.degrees(arc))
    m = round((math.degrees(arc) - d) * 60, 1)
    return rad(Arc(d, m))

#converts arcs from degrees and minutes to radians
def rad(arc):
    return math.radians(arc.degrees + (arc.minutes / 60))

#converts arcs from radians to degrees and minutes
def degmin(rad):
    deg = math.degrees(rad)
    d = int(deg)
    m = round((deg - d) * 60, 1)
    if m == 60:
        d += 1
        m = 0
    return Arc(d, m)

#finds the gha and dec of a celestial body at a given date and time
#todo: allow moon, stars, and planets to be searched
def getCelestialPosition(date, body):
    if body == 'sun':
        b = ephem.Sun()
    elif body == 'moon':
        b = ephem.Moon()
    obs = ephem.Observer()
    obs.date = date
        
    b.compute(date, epoch = date)
    gha = ephemrad(ephem.degrees(obs.sidereal_time() - b.g_ra).norm)
    dec = ephemrad(b.g_dec)
    sd = rad(Arc(0, (b.size / 60) / 2)) #convert arcseconds to minutes, then divide by 2 to get semidiameter
    hp = b.radius / 0.272805950305
    return {'gha':gha, 'dec':dec, 'sd':sd, 'hp':hp}

def getAssLat(lat):
    lat = degmin(lat)
    minutes = lat.minutes
    degrees = lat.degrees
    if degrees >= 0 and minutes >= 30:
        degrees = degrees + 1
    if degrees <= 0 and minutes <= -30:
        degrees = degrees - 1
    return rad(Arc(degrees, 0))

#returns assumed longitude: closest longitude to inputted longitude
#that makes gha minutes add or subtract to 0
def getAssLong(long, gha):
    long = degmin(long)
    gha = degmin(gha)
    
    degrees = long.degrees
    
    if degrees >= 0 and long.minutes > 0:
        minutes = 60 - gha.minutes
    else:
        minutes = -1 * gha.minutes
    
    asslong1 = rad(Arc(degrees - 1, minutes))
    asslong2 = rad(Arc(degrees, minutes))
    asslong3 = rad(Arc(degrees + 1, minutes))

    radlong = rad(long)
    diff1 = abs(radlong - asslong1)
    diff2 = abs(radlong - asslong2)
    diff3 = abs(radlong - asslong3)

    diffdict = {
        diff1 : asslong1,
        diff2 : asslong2,
        diff3 : asslong3
        }

    return diffdict[min(diff1, diff2, diff3)]

#input---------------------

#todo: improve user friendliness and add error handling
#date = input('gmt date/time (mm/dd/yyyy hh:mm:ss): ') or '2019/9/21 18:36:31'
#hsdeg, hsmin = input('sextant height: ').split() or '47', '31.2'
#iemin, iedir = input('index error: ').split() or '0.6', 'on'
#hoe = input('height of eye in feet: ') or '10'
#latdeg, latmin, latdir = input('latitude: ').split() or '37', '44.3', 'n'
#longdeg, longmin, longdir = input('longitude: ').split() or '122', '46.4', 'w'

#print('\n')

#hs = Arc(int(hsdeg), float(hsmin))
#ie = Arc(0, float(iemin), iedir)
#hoe = int(hoe)
#lat = Arc(int(latdeg), float(latmin), latdir)
#long = Arc(int(longdeg), float(longmin), longdir)

date = '2019/10/21 18:25:46'
hs = Arc(36, 51.6)
ie = Arc(0, 3.0)
hoe = 10
lat = Arc(37, 45.8, 'n')
long = Arc(122, 59.0, 'w')
body = 'moon'
limb = 'u'

#celestial body calculations--------------
pos = getCelestialPosition(date, body)
gha = pos['gha']
dec = pos['dec']
sd = pos['sd']
hp = pos['hp']

#sight corrections---------------
hs = rad(hs)
ie = rad(ie)
dip = rad(Arc(0, round(-0.97 * math.sqrt(hoe), 1)))

h2 = hs + ie + dip

#refraction, parallax, and semidiamter
ref = (0.0167 * math.pi / 180) / math.tan(h2 + ((7.32 * math.pi / 180) / (h2 + (4.32 * math.pi/ 180)))) #todo allow for correction beyond standard atomspheric conditions

h3 = h2 - ref

if body == 'sun':
    pa = rad(Arc(0, 0.144)) * math.cos(h2) #constant for sun, variable for moon and planets. 0 for stars
    h4 = h3 + pa
    ho = h4 + sd if limb == 'l' else h4 - sd #add for lower limb, subtract for upper limb
    acorr = degmin(sd + pa - ref)
elif body == 'moon':
    pa = hp * math.cos(h2)
    print(degmin(hp))
    print(degmin(pa))
    print(degmin(sd))
    print(degmin(ref))
    ho = h3 + pa - sd
    acorr = degmin(pa - sd - ref)

#get assumed position
asslat = getAssLat(rad(lat))
asslong = getAssLong(rad(long), gha)

lha = gha + asslong

if lha < 0:
    lha = lha + (2 * math.pi)

hc = math.asin((math.sin(asslat) * math.sin(dec)) + (math.cos(asslat) * math.cos(dec) * math.cos(lha)))
diff = abs(ho - hc)

z = math.acos((math.sin(dec) - math.sin(asslat) * math.sin(hc)) / (math.cos(asslat) * math.cos(hc)))

zn = z if lha > math.pi else (2 * math.pi) - z

print(tabulate([['hs', degmin(hs)], ['ie', degmin(ie)], ['dip', degmin(dip)], \
                ['altitude correction', acorr], \
                #['ref', degmin(ref)], ['pa', degmin(pa)], ['sd', degmin(sd)], \
                ['ho', degmin(ho)], [None, None], \
                ['lat', lat], ['long', long], ['asslat', degmin(asslat)], ['asslong', degmin(asslong)], \
                ['gha', degmin(gha)], ['lha', degmin(lha)], ['dec', degmin(dec)], [None, None], \
                ['hc', degmin(hc)], ['zn', degmin(zn)], \
                ['intercept', str(degmin(diff)) + ('towards' if ho > hc else 'away')]
                ], headers = ['Description', 'Angle']))






