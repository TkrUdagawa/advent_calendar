# -*- coding:utf-8 -*-

import argparse
import jubatus
from jubatus.common import Datum


def make_datum_binary(title = None, text = None, picture = None):
    d = Datum()
    if title:
        d.add_string("title", title)
    if text:
        d.add_string("text", text)
    if picture:
        d.add_binary("img", picture)
    return d

def make_datum(title = None, text = None, picture = None):
    d = Datum()
    if title:
        d.add_string("title", title)
    if text:
        d.add_string("text", text)
    if picture:
        with open(picture, "rb") as f:
            d.add_binary("img", f.read())
    return d

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img", action="store", default= None, help="path to img file")
    parser.add_argument("-t", "--title", action="store", default= None, help="title string")
    parser.add_argument("-b", "--body", action="store", default= None, help="body string")
    parser.add_argument("-d", "--id", action="store", default=None, help="id of blog-post")
    parser.add_argument("-m", "--method", action="store", required=True, choices=["id", "datum"], help="")
    return parser.parse_args()

def make_client(address="160.16.239.168", port=9199, name="irasutoya", timeout=0):
    return jubatus.Recommender(address, port, name, timeout)

def similar_row_binary(args, method = "ORB", num=10):
    if method == "ORB":
        port = 9199
    else:
        port = 9200
    cl = make_client(port = port)
    if args.method == "id":
        return cl.similar_row_from_id(args.id, num)
    elif args.method == "datum":
        d = make_datum_binary(args.title, args.body, args.img)
        return cl.similar_row_from_datum(d, num)

def similar_row(args, method="ORB", num=10):
    if method == "ORB":
        port = 9199
    else:
        port = 9200
    cl = make_client(port = port)
    if args.method == "id":
        return cl.similar_row_from_id(args.id, num)
    elif args.method == "datum":
        d = make_datum(args.title, args.body, args.img)
        return cl.similar_row_from_datum(d, num)

if __name__ == "__main__":
    args = parse_args()
    print(similar_row(args))
