#!/usr/bin/env python3
from flask import Flask, render_template, make_response, request, redirect
import os
import datetime

app = Flask(__name__)


@app.route("/")
def index():
    img_dir = os.path.abspath("./static/img/vmok")
    dirs = []
    for root, _dirs, _files in os.walk(img_dir):
        if _dirs:
            root = root[len(img_dir):]
            if len(root.split("/")) == 4:
                if len(root.split("/")[3]) == 1:
                    root = root[:-1]+"0"+root.split("/")[3]
                root = root[1:]
                dirs.append(root)
    dirs = [{"path": x,
             "week_numb":datetime.datetime.strptime(x, "%Y/%m/%d").isocalendar()[1]}
            for x in sorted(dirs)[::-1]]
    cur_week_numb = datetime.datetime.now().isocalendar()[1]
    for tp in dirs:
        if tp["week_numb"] == cur_week_numb:
            tp["title"] = "Praegune nädal"
            tp["bold"] = True
        elif tp["week_numb"]+1 == cur_week_numb:
            tp["title"] = "Eelmine nädal"
        elif tp["week_numb"]-1 == cur_week_numb:
            tp["title"] = "Järgmine nädal"

    if os.path.exists(img_dir+"/future"):
        dirs.insert(0, {"path": "future"})
        dirs[0]["title"] = "Järgmine nädal"

    vmg_dir = os.path.abspath("./static/img/vmg")
    vmg_dirs = os.listdir(vmg_dir)

    return render_template("index.html", dirs=dirs, vmg_dirs=vmg_dirs,
                           last_tp_vmg=request.cookies.get("last_tp_vmg"),
                           last_tp_vmok=request.cookies.get("last_tp_vmok"))


@app.route("/vmok/<aasta>/", defaults={"kuu": "", "paev": ""})
@app.route("/vmok/<aasta>/<tuup>/<name>", defaults={"kuu": "", "paev": ""})
@app.route("/vmok/<int:aasta>/<kuu>/<paev>/<tuup>/<name>")
@app.route("/vmok/<int:aasta>/<kuu>/<paev>/")
def vmok_show(aasta, kuu, paev, tuup=None, name=None):
    img_dir = os.path.abspath("./static/img/vmok")
    if tuup not in ("c", "r", "t"):
        tuup = "c"
    dir_list = os.listdir(img_dir+"/{}/{}/{}/{}".format(aasta,
                                                        kuu, paev, tuup))
    if name not in dir_list:
        try:
            name = dir_list[0]
        except IndexError:
            return redirect("/vmok/{}/{}/{}/".format(aasta, kuu, paev))
    if aasta == "future":
        img_path = "/{}/{}/{}".format(aasta, tuup, name)
    else:
        img_path = "/{}/{}/{}/{}/{}".format(aasta, kuu, paev, tuup, name)
    img_path = "/static/img/vmok"+img_path

    if aasta == "future":
        i_path = "/future/"
        date = "/vmok/future"
    else:
        date = "/vmok/{}/{}/{}".format(aasta, kuu, paev)
        i_path = "/{}/{}/{}/".format(aasta, kuu, paev)

    c_list = sorted(os.listdir(img_dir+i_path+"c"))
    r_list = sorted(os.listdir(img_dir+i_path+"r"))
    t_list = sorted(os.listdir(img_dir+i_path+"t"))

    names = ("Grupid", "Õpetajad", "Ruumid")

    resp = make_response(render_template("show_tp.html", img_path=img_path,
                                         names=names,
                                         t_list=[c_list, t_list, r_list],
                                         date=date))
    resp.set_cookie('last_tp_vmok', value='{}/{}'.format(tuup, name),
                    max_age=2592000)
    return resp


@app.route("/vmg/<date>/")
@app.route("/vmg/<date>/<tuup>/<name>")
def vmg_show(date, tuup=None, name=None):
    img_dir = os.path.abspath("./static/img/vmg")
    if tuup not in ("c", "r", "t"):
        tuup = "c"
    dir_list = os.listdir(img_dir+"/{}/{}".format(date, tuup))
    if name not in dir_list:
        name = dir_list[0]
    img_path = "/{}/{}/{}".format(date, tuup, name)
    img_path = "/static/img/vmg"+img_path

    c_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "c")))
    r_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "r")))
    t_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "t")))

    names = ("Klassid", "Õpetajad", "Ruumid")

    resp = make_response(render_template("show_tp.html", img_path=img_path,
                                         names=names,
                                         t_list=[c_list, t_list, r_list],
                                         date="/vmg/{}".format(date)))
    resp.set_cookie('last_tp_vmg', '{}/{}'.format(tuup, name),
                    max_age=2592000)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
