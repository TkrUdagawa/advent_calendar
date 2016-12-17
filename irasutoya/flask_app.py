# -*- coding:utf-8 -*-

import os
import json
import script.analyze as an

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file


app = Flask(__name__)
app_home=os.path.dirname(__file__)
@app.route("/")
def main_view():
    return render_template("index.html")

@app.route("/imgs")
@app.route("/imgs/<year>")
@app.route("/imgs/<year>/<month>")
@app.route("/imgs/<year>/<month>/<filename>")
def get_img(year, month, filename):
    return send_file(os.path.join(app_home, "static", "imgs", year, month, filename))

@app.route("/more_recommend", methods=["POST"])
def more_recommend():
    q = query()
    q.body = request.form["text"]
    q.title = request.form["title"]
    q.img = "{}/static{}".format(app_home,request.form["file_name"])
    method = request.form["method"]
    num = int(request.form["num"])
    res = an.similar_row(q, method, num)
    if len(res) > 0:
        r = parse_result(res)
        return render_template("recommend.html", res = r, num=num, method=method)
    else:
        return '''
        nothing can be found
        <a href="/"> TOP</a>
        '''

@app.route("/recommend", methods=["GET"])
@app.route("/more_recommend", methods=["GET"])
def redirect():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    print(request.files)
    q = query()
    q.body = request.form["text"]
    q.title = request.form["title"]
    try:
        file_body = request.files['img']
    except:
        file_body = None
    q.img = file_body.stream.read()
    method = request.form["method"]
    print(file_body)
    num = int(request.form["num"])
    res = an.similar_row_binary(q, method, num)
    if len(res) > 0:
        r = parse_result(res)
        return render_template("recommend.html", res = r, num=num, method=method)
    else:
        return '''
        nothing can be found
        <a href="/"> TOP</a>
        '''

class query:
    def __init__(self):
        self.id = None
        self.body = None
        self.title = None
        self.img = None
        self.method = "datum"

def parse_result(res):
    result_list = []
    for r in res:
        y, m, t, n = r.id.split("_")
        with open(os.path.join(app_home, "static", "article", y, m, "{}_{}.json".format(t, n))) as f:
            j = json.load(f)
            title = j["title"]
            text = j["text"]
            img = "/imgs/{}/{}/{}".format(y, m, j["img"].split("/")[-1])
            url = "http://irasutoya.com/{}/{}/{}_{}.html".format(y, m, t, n)
            score = round(r.score, 4)
            result_list.append({"title": title, "text": text, "img": img, "url": url, "score":score})
    return result_list

if __name__ == "__main__":
    app.run()

