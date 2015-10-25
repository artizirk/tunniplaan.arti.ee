#!/usr/bin/env python3
from flask import Flask, render_template, make_response, request, redirect, abort
import os
import datetime

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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
    #dirs[0]["title"] = "Praegune nädal"

    if os.path.exists(img_dir+"/future"):
        dirs.insert(0, {"path": "future"})
        dirs[0]["title"] = "Järgmine nädal"

    vmg_dir = os.path.abspath("./static/img/vmg")
    vmg_dirs = os.listdir(vmg_dir)

    jogeva_dir = os.path.abspath("./static/img/jogeva")
    jogeva_dirs = os.listdir(jogeva_dir)

    return render_template("index.html", dirs=dirs, vmg_dirs=vmg_dirs, jogeva_dirs=jogeva_dirs,
                           last_tp_vmg=request.cookies.get("last_tp_vmg"),
                           last_tp_vmok=request.cookies.get("last_tp_vmok"),
                           last_tp_jogeva=request.cookies.get("last_tp_jogeva"))


@app.route("/vmok/<int:aasta>/<kuu>/<paev>/<tuup>/<name>")
@app.route("/vmok/<int:aasta>/<kuu>/<paev>/")
def vmok_show(aasta, kuu, paev, tuup=None, name=None):
    img_dir = os.path.abspath("./static/img/vmok")
    if tuup not in ("c", "r", "t"):
        tuup = "c"
    try:
        dir_list = os.listdir(img_dir+"/{}/{}/{}/{}".format(aasta,
                                                            kuu, paev, tuup))
    except FileNotFoundError as err:
        abort(404)

    if name and not name.endswith(".png"):
        name += ".png"
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

    type_pairs = {"c":"grupi", "r":"ruumi", "t":""}

    tp_name = name[:-4]
    page_tp_name = tp_name
    if tuup == "c":
        tp_name = "".join(tp_name.split(" ")[0])
    tp_type = type_pairs[tuup]

    resp = make_response(render_template("show_tp.html", img_path=img_path,
                                         tp_name=tp_name,
                                         names=names,
                                         t_list=[c_list, t_list, r_list],
                                         date=date,
                                         head_title="Väike-Maarja Õppekeskuse {} {} Flashi vabad tunniplaan".format(tp_name,tp_type),
                                         header_title="{} {} tunniplaan mobiilseadmes".format(tp_name,tp_type)))
    resp.set_cookie('last_tp_vmok', value='{}/{}'.format(tuup, page_tp_name),
                    max_age=2592000)
    return resp


@app.route("/vmg/<date>/")
@app.route("/vmg/<date>/<tuup>/<name>")
def vmg_show(date, tuup=None, name=None):
    img_dir = os.path.abspath("./static/img/vmg")
    if tuup not in ("c", "r", "t"):
        tuup = "c"
    try:
        dir_list = os.listdir(img_dir+"/{}/{}".format(date, tuup))
    except FileNotFoundError as err:
        abort(404)

    if name and not name.endswith(".png"):
        name += ".png"
    if name not in dir_list:
        name = dir_list[-1]
    img_path = "/{}/{}/{}".format(date, tuup, name)
    img_path = "/static/img/vmg"+img_path

    c_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "c")))
    r_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "r")))
    t_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "t")))

    names = ("Klassid", "Õpetajad", "Ruumid")

    type_pairs = {"c":"", "r":"ruumi", "t":""}

    tp_name = name[:-4]
    tp_type = type_pairs[tuup]

    resp = make_response(render_template("show_tp.html", img_path=img_path,
                                         tp_name=tp_name,
                                         names=names,
                                         t_list=[c_list, t_list, r_list],
                                         date="/vmg/{}".format(date),
                                         head_title="Väike-Maarja Gümnaasiumi {} {} Flashi vabad tunniplaan".format(tp_name,tp_type),
                                         header_title="{} {} tunniplaan mobiilseadmes".format(tp_name,tp_type)))
    resp.set_cookie('last_tp_vmg', '{}/{}'.format(tuup, tp_name),
                    max_age=2592000)
    return resp

@app.route("/jogeva/<date>/")
@app.route("/jogeva/<date>/<tuup>/<name>")
def jogeva_show(date, tuup=None, name=None):
    img_dir = os.path.abspath("./static/img/jogeva")
    if tuup not in ("c", "r", "t"):
        tuup = "c"
    try:
        dir_list = os.listdir(img_dir+"/{}/{}".format(date, tuup))
    except FileNotFoundError as err:
        abort(404)

    if name and not name.endswith(".png"):
        name += ".png"
    if name not in dir_list:
        name = dir_list[-1]
    img_path = "/{}/{}/{}".format(date, tuup, name)
    img_path = "/static/img/jogeva"+img_path

    c_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "c")))
    r_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "r")))
    t_list = sorted(os.listdir(img_dir+"/{}/{}".format(date, "t")))

    names = ("Klassid", "Õpetajad", "Ruumid")

    type_pairs = {"c":"klassi", "r":"ruumi", "t":""}

    tp_name = name[:-4]
    tp_type = type_pairs[tuup]

    resp = make_response(render_template("show_tp.html", img_path=img_path,
                                         tp_name=tp_name,
                                         names=names,
                                         t_list=[c_list, t_list, r_list],
                                         date="/jogeva/{}".format(date),
                                         head_title="Jõgevamaa Gümnaasiumi {} {} Flashi vabad tunniplaan".format(tp_name,tp_type),
                                         header_title="{} {} tunniplaan mobiilseadmes".format(tp_name,tp_type)))
    resp.set_cookie('last_tp_jogeva', '{}/{}'.format(tuup, tp_name),
                    max_age=2592000)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
