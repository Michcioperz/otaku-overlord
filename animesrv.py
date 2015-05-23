#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template, redirect, url_for, jsonify, g, json
import anime as animelib
import subprocess, os, shutil
app = Flask(__name__)
prefix = '/otaku'

def desc(series):
    try:
        with open(os.path.join("/datanime",series,"desc.txt")) as f:
            return f.read()
    except:
        return ""

def series():
    return os.listdir("/datanime")

@app.route(prefix+'/shirley')
def shirley_api():
    return jsonify(videos=animelib.shirley(), series=series())

@app.route(prefix+'/')
def watchable():
    return render_template('watchable.html', animes=animelib.watchable(), sorted=sorted, addable=len(animelib.addable()), series=series())

@app.route(prefix+'/edit/<anime>')
def edit(anime):
    return render_template("write_form.html", codename=anime)

@app.route(prefix+'/scrobble/<anime>')
def scrobble(anime):
    animelib.scrobble(anime)
    return redirect(url_for('watchable'))

@app.route(prefix+'/write/<anime>/<title>/<episode>')
def write(anime, title, episode):
    animelib.write_tag(anime, title, episode)
    return redirect(url_for('watchable'))

@app.route(prefix+'/remove/<anime>')
def remove(anime):
    if anime in animelib.seen() and not os.path.isfile(os.path.join(animelib.ANIME_DIR, anime, animelib.KEEPALIVE_FILENAME)):
        shutil.rmtree(os.path.join(animelib.ANIME_DIR, anime))
    return redirect(url_for("watchable"))

@app.route(prefix+'/watch/<anime>')
def watch(anime):
    kill()
    subprocess.Popen(['omxplayer', '-o', 'both', os.path.join(animelib.ANIME_DIR, anime, 'videoplayback')])
    return redirect(url_for('watchable'))

@app.route(prefix+'/kill')
def kill():
    subprocess.call(['killall','omxplayer.bin'])
    return redirect(url_for('watchable'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8766)
