#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import weibo
import os
import urllib.request
import cv2
import shutil
import time
import subprocess
from pathlib import Path
from PIL import Image
from pymongo import MongoClient

FILE_PATH = os.path.split(os.path.realpath(__file__))[0] + os.sep
IMAGE_PATH = FILE_PATH + "luhan1994.github.io/assets/"
INDEX_PATH = FILE_PATH + "luhan1994.github.io/index.html"
TEST_PATH = FILE_PATH + "luhan1994.github.io/test"

def detect_face(image_path):
    print(image_path)
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5)
    if (len(faces) == 0):
        return None, None
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite(image_path, img)
    (x, y, w, h) = faces[0]
    return gray[y:y + w, x:x + h], faces[0]

def get_index():
    p = Path(IMAGE_PATH)
    file_names = [x.name for x in p.iterdir()]
    max_nums = sorted([int(x.split('.')[0]) for x in file_names])
    return max_nums[-1] + 1

def save_img(infile="pic.jpg"):
    f, e = os.path.splitext(infile)
    outfile = f + ".jpg"
    if infile != outfile:
        try:
            with Image.open(infile) as im:
                im.save(IMAGE_PATH + outfile)
            os.remove(infile)
        except OSError:
            print("cannot convert", infile)
    shutil.move(outfile, IMAGE_PATH + str(get_index()) + ".jpg")
    return outfile

def edit():
    index = get_index()
    html = ""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    with open(INDEX_PATH, "wb") as f:
        f.write(html.replace("MAX_IMAGES", str(index - 1)).encode("utf-8"))
    with open(TEST_PATH, "w") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S"))


def forever():
    client = MongoClient("mongodb://admin:xx37b9900@localhost:27017/")
    db = client["weibo"]
    weibo_collection = db["weibo"]
    for one in weibo_collection.find({"finished": None}):
        print(one)
        if one["pics"] is not None and one["pics"] != "":
            for pic in one["pics"].split(","):
                print(pic)
                pic_path = "pic" + os.path.splitext(pic)[-1]
                urllib.request.urlretrieve(
                    pic, pic_path)
                gray, face = detect_face(pic_path)
                if gray is not None:
                    print("has face: ", pic)
                    save_img(pic_path)
                    # cv2.imshow('face', gray)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
        weibo_collection.update({"_id": one["_id"]}, { "$set": { "finished": True } })


def push():
    subprocess.run(["./push.sh", time.strftime("%Y-%m-%d %H:%M:%S")], shell=True)


if __name__ == "__main__":
    weibo.main()
    forever()
    edit()
    push()
    
