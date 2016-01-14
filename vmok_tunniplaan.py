import requests
from bs4 import BeautifulSoup
import tempfile
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from IPython import embed
from datetime import datetime
import inspect
import sys
from datetime import datetime
import re

_real_print = print
def print(*args, **kwargs):
    _real_print(*args, **kwargs)
    sys.stdout.flush()



url = "http://vmok.v-maarja.ee/oppetoo/tunniplaan/"
base_url = "http://www.v-maarja.ee/vmok/"

if os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))).startswith("/srv/http/tunniplaan.arti.ee/"):
    img_path = "/srv/http/tunniplaan.arti.ee/static/img/vmok"
else:
    img_path = "./static/img/vmok/"


leht = requests.get(url).text
soup = BeautifulSoup(leht, "html.parser")
sisu = soup.find("div", {"class":"sidenews"})
items = [(x.get_text(), x.get("href"))
         for x in sisu.find_all("a") if x.get("href")]
#embed();exit()

def save_tunniplaan(swf, data, d_dir):
    subprocess.call(['wget', base_url+tunniplaan[1]+swf,
                     "-O", temp_dir+swf])
    for child in data:
        nimi = child.attrib["name"]#.encode("ascii","xmlcharrefreplace").decode("ascii")
        page_id = child.attrib["id"][1:]
        print("loon {} tunniplaani".format(nimi))
        # print(child.attrib["name"], child.attrib["id"][1:])

        subprocess.call(['swfrender', temp_dir+swf, '-r', '150',
                         '-o', temp_dir+'/{}.png'.format(nimi),
                         '-p', page_id])
        subprocess.call(['convert', temp_dir+'/{}.png'.format(nimi),
                         '-alpha', 'remove',
                         '{}/{}.png'.format(d_dir, nimi)])


tunniplaanid = items[:3]

# moar ugly hacks
tp_new=[]
for name, url in tunniplaanid:
    if url.endswith("swfcombiner.swf"):
        url = url[:-15]
    if url.startswith("http://www.v-maarja.ee/vmok/"):
        url = url[28:]
    tp_new.append((name, url))
tunniplaanid = tp_new

muu = items[3:]
#embed();exit()
# if muu:
#    print("vist on ka muudatused: {}".format(str(items[3:])))

print("laen alla tunniplaane")
for i, tunniplaan in enumerate(tunniplaanid):
    #if len(tunniplaan[1]) > 11:
    #    tunniplaan = (tunniplaan[0], tunniplaan[1][28:].strip("/"))
    future = False
    print("{0}".format(*tunniplaan))
    #embed();exit()
    if len(tunniplaan[0].strip()) <= 10:
        print("kuupäev on puudu, läheb future kasuta")
        future = True

    if not future:
        maches = re.search("\s([0-9\.]+)\-([0-9\.]+)", tunniplaan[0])
        #date_end = tunniplaan[0].split("-")[-1].strip()
        #date_start = tunniplaan[0].split(" ")[1]
        date_start = maches.group(1)
        date_end = maches.group(2)
        #if tunniplaan[0].count(" ") == 1:
        #    date_start = date_start.split("-")[0]
        #if i == 1: embed()#;exit()
        #embed()
        if date_end.count(".") == 1:
            today = datetime.today()
            date_start = date_start+"."+str(today.year)
        else:
            date_start = date_start+"."+date_end[-4:]
    #if i == 1: embed()#;exit()
    base_dir = os.path.abspath(img_path)
    if not future:
        t_dir = base_dir+"/{2}/{1}/{0}".format(*date_start.split("."))
    else:
        t_dir = base_dir+"/future"

    if not os.path.exists(t_dir):
        os.makedirs(t_dir)
        os.makedirs(t_dir+"/c")
        os.makedirs(t_dir+"/t")
        os.makedirs(t_dir+"/r")
    else:
        if not future:
            print("see tunniplaan on juba alla tõmmatud")
            continue

    print("loodud kausta tunniplaanide jaoks:{}".format(t_dir))
    temp_dir = tempfile.mkdtemp("tunniplaan")
    print("loodud temp dir:{}".format(temp_dir))

    r = requests.get(base_url+tunniplaan[1]+'/timetable.xml')
    r.encoding = "utf-8"
    data = r.text
    #embed();exit()
    data = ET.fromstring(data)

    #embed();exit()

    print("tõmban alla gruppide tunniplaane")
    save_tunniplaan("/index.swf", data[1], t_dir+"/c")

    print("tõmban alla õpetajate tunniplaane")
    save_tunniplaan("/teachers_0.swf", data[0], t_dir+"/t")

    print("tõmban alla ruumide tunniplaane")
    save_tunniplaan("/rooms.swf", data[3], t_dir+"/r")

    print("kustuta temp dir: {}".format(temp_dir))
    shutil.rmtree(temp_dir)
