#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template, redirect, url_for
import anime as animelib
import subprocess, os
app = Flask(__name__)
prefix = '/otaku'

@app.route(prefix+'/addable')
def addable():
    return render_template('addable.html', anime=animelib.addable())

@app.route(prefix+'/')
def watchable():
    return render_template('watchable.html', anime=animelib.watchable(), addable=len(animelib.addable()))

@app.route(prefix+'/edit/<anime>')
def edit(anime):
    return render_template("write_form.html", codename=anime)

@app.route(prefix+'/write/<anime>/<title>/<episode>')
def write(anime, title, episode):
    animelib.write_tag(anime, title, episode)
    return redirect(url_for('watchable'))

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
