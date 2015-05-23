#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template, redirect, url_for, jsonify, flash
import anime as animelib
import subprocess, os, shutil
app = Flask(__name__)
app.secret_key = "mou-oshimai-da"
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
    flash("%s marked as seen" % anime)
    return redirect(url_for('watchable'))

@app.route(prefix+'/write/<anime>/<title>/<episode>')
def write(anime, title, episode):
    animelib.write_tag(anime, title, episode)
    flash("%s tagged!" % anime)
    return redirect(url_for('watchable'))

@app.route(prefix+'/remove/<anime>')
def remove(anime):
    if anime in animelib.seen() and not os.path.isfile(os.path.join(animelib.ANIME_DIR, anime, animelib.KEEPALIVE_FILENAME)):
        shutil.rmtree(os.path.join(animelib.ANIME_DIR, anime))
        flash("%s removed!" % anime)
    else:
        flash("%s wasn't watched yet or was marked as worth rewatching." % anime)
    return redirect(url_for("watchable"))

@app.route(prefix+'/watch/<anime>')
def watch(anime):
    kill()
    subprocess.Popen(['omxplayer', '-o', 'both', os.path.join(animelib.ANIME_DIR, anime, 'videoplayback')])
    flash("%s launched on Michinom Pi!")
    return redirect(url_for('watchable'))

@app.route(prefix+'/kill')
def kill():
    subprocess.call(['killall','omxplayer.bin'])
    flash("Omxplayer instances killed")
    return redirect(url_for('watchable'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8766)
