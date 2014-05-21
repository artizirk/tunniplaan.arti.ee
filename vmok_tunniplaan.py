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

_real_print = print
def print(*args, **kwargs):
    _real_print(*args, **kwargs)
    sys.stdout.flush()



base_url = "http://www.v-maarja.ee/vmok/"
url = base_url + "Tunniplaan_42.htm"
if os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))).startswith("/srv/http/tunniplaan.arti.ee/"):
    img_path = "/srv/http/tunniplaan.arti.ee/static/img/vmok"
else:
    img_path = "./static/img/vmok/"


leht = requests.get(url).text
soup = BeautifulSoup(leht)
sisu = soup.find(id="sisu_env")
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
muu = items[3:]

# if muu:
#    print("vist on ka muudatused: {}".format(str(items[3:])))

print("laen alla tunniplaane")
for tunniplaan in tunniplaanid:
    future = False
    print("{0}".format(*tunniplaan))
    #embed();exit()
    if len(tunniplaan[0].strip()) <= 10:
        print("kuupäev on puudu, läheb future kasuta")
        future = True

    if not future:
        date_end = tunniplaan[0].split("-")[-1].strip()
        date_start = tunniplaan[0].split(" ")[1]+"."+date_end[-4:]
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
