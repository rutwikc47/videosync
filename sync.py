from math import cos, asin, sqrt
from natsort import natsorted, ns
from moviepy.tools import subprocess_call
import os
import pandas

pathjan = '/Users/Rutwik/Documents/Skylark/Videoproc/jan_cleaned.csv'
pathapr = '/Users/Rutwik/Documents/Skylark/Videoproc/apr_cleaned.csv'
videojan = '/Users/Rutwik/Documents/Skylark/vidproc/jan.mp4'
videoapr = '/Users/Rutwik/Documents/Skylark/vidproc/april.mp4'
output = '/Users/Rutwik/Documents/Skylark/vidproc/outapr.mp4'
outputin = '/Users/Rutwik/Documents/Skylark/vidproc/aprout.mp4'
outfolder = '/Users/Rutwik/Documents/Skylark/aprproc/'

datajan = pandas.read_csv(pathjan)
dataapr = pandas.read_csv(pathapr)

latlonjan = zip(datajan['latitude'], datajan['longitude'], datajan['time(millisecond)'])
latlonjanlist = list(latlonjan)
latlonjanlist = latlonjanlist[24:]

latlonapr = zip(dataapr['latitude'], dataapr['longitude'], dataapr['time(millisecond)'])
latlonaprlist = list(latlonapr)
latlonaprlist = latlonaprlist[221:]
latlonaprlist = latlonaprlist[::100]


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


def closest(data, v):
    return min(data, key=lambda p: distance(v[0], v[1], p[0], p[1]))


def get_values(iterables, key_to_find):
    return list(filter(lambda x: key_to_find in x, iterables))


for r in range(len(latlonaprlist)):

    if r >= 1:

        latloncomp1 = latlonaprlist[r-1]
        latloncomp2 = latlonaprlist[r]
        timediffapr = latloncomp2[2]-latloncomp1[2]
        print("APR " + str(distance(latloncomp1[0], latloncomp1[1], latloncomp2[0], latloncomp2[0])))
        print("TIME " + str(timediffapr))

        try:
            janindex1 = latlonjanlist.index(latloncomp1)
        except ValueError:
            janindex1 = closest(latlonjanlist, latloncomp1)

        try:
            janindex2 = latlonjanlist.index(latloncomp2)
        except ValueError:
            janindex2 = closest(latlonjanlist, latloncomp2)

        timediffjan = janindex2[2]-janindex1[2]

        print("JAN " + str(distance(janindex1[0], janindex1[1], janindex2[0], janindex2[0])))
        print("TIME " + str(timediffjan))

        perctime = timediffjan / timediffapr
        print("PERCENT DIFF  " + str(perctime))

        x = latloncomp1[2]-52900
        secx = int((x / 1000) % 60)
        minx = int((x / (1000 * 60)) % 60)
        hrsx = int((x / (1000 * 60 * 60)) % 24)

        y = latloncomp2[2]-52900
        secy = int((y / 1000) % 60)
        miny = int((y / (1000 * 60)) % 60)
        hrsy = int((y / (1000 * 60 * 60)) % 24)

        cmdtrim = "ffmpeg -y -i " + videoapr + " -ss " + str(hrsx) + ":" + str(minx) + ":" + str(secx) + " -to " + str(hrsy) + ":" + str(miny) + ":" + str(secy) + " -c copy " + "/Users/Rutwik/Documents/Skylark/aprproc/" + str(r) + ".mp4"
        subprocess_call(cmdtrim.split())

        cmdspeed = "ffmpeg -y -an -i " + "/Users/Rutwik/Documents/Skylark/aprproc/" + str(r) + ".mp4 -r 30" + " -filter_complex [0:v]setpts=" + str(perctime) + "*PTS[v] -map [v] " + "/Users/Rutwik/Documents/Skylark/aprproc/aprout" +str(r)+".mp4"
        subprocess_call(cmdspeed.split())

        print('\n')


vids=[]
for f in os.listdir(outfolder):

    if f.startswith('aprout'):

        vids.append("file '" + outfolder + f + "'")

sortvids = natsorted(vids)
print(sortvids)

with open("/Users/Rutwik/Documents/Skylark/aprproc/filemp4.txt", mode='wt') as output:
    output.write('\n'.join((line) for line in sortvids))


# Concatenate code:-

# cmdmerge = "ffmpeg -f concat -safe 0 -i /Users/Rutwik/Documents/Skylark/aprproc/filemp4.txt -c copy -sn -y /Users/Rutwik/Documents/Skylark/aprproc/output_file.mp4"
#
# subprocess_call(cmdmerge.split())
