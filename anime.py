#!/usr/bin/env python
import json, os, subprocess
from pprint import pprint

ANIME_DIR = '/anime'
METADATA_FILENAME = 'metadata.json'
VIDEO_FILENAME = 'videoplayback'
SEEN_TAG_FILENAME = 'scrobble'
REQUIRED_FILENAMES = [METADATA_FILENAME, VIDEO_FILENAME]

def watchable():
    animes = {}
    for chance in os.listdir(ANIME_DIR):
        if os.path.isdir(os.path.join(ANIME_DIR, chance)):
            if set(os.listdir(os.path.join(ANIME_DIR, chance))).issuperset(REQUIRED_FILENAMES):
                with open(os.path.join(ANIME_DIR, chance, METADATA_FILENAME)) as file:
                    animes[chance] = json.load(file)
    return animes

def write_tag(id, series=None, episode=None):
    if os.path.isdir(os.path.join(ANIME_DIR, id)):
        if METADATA_FILENAME not in os.listdir(os.path.join(ANIME_DIR, id)):
            with open(os.path.join(ANIME_DIR, id, METADATA_FILENAME), 'w') as file:
                file.write(json.dumps({'series': series or raw_input("Series: "), 'episode': episode or raw_input("Episode: ")}))
    return True

def write_loop():
    for i in addable():
        print(i)
        write_tag(i)

def addable():
    animes = []
    for chance in os.listdir(ANIME_DIR):
        if os.path.isdir(os.path.join(ANIME_DIR, chance)):
            if METADATA_FILENAME not in os.listdir(os.path.join(ANIME_DIR, chance)) and VIDEO_FILENAME in os.listdir(os.path.join(ANIME_DIR, chance)):
                animes.append(chance)
    return sorted(animes)

def scrobble(id):
    if os.path.isdir(os.path.join(ANIME_DIR, id)):
        if not os.path.exists(os.path.join(ANIME_DIR, id, SEEN_TAG_FILENAME)):
            open(os.path.join(ANIME_DIR, id, SEEN_TAG_FILENAME), 'a').close()
            return True
    return False

def unseen():
    animes = {}
    chances = watchable()
    for chance in chances:
        if not os.path.exists(os.path.join(ANIME_DIR, chance, SEEN_TAG_FILENAME)):
            animes[chance] = chances[chance]
    return animes

def seen():
    animes = {}
    chances = watchable()
    for chance in chances:
        if os.path.exists(os.path.join(ANIME_DIR, chance, SEEN_TAG_FILENAME)):
            animes[chance] = chances[chance]
    return animes

def watch(id):
    if os.path.isdir(os.path.join(ANIME_DIR, id)):
        if os.path.isfile(os.path.join(ANIME_DIR, id, VIDEO_FILENAME)):
            if subprocess.call(['omxplayer', '-o', 'both', os.path.join(ANIME_DIR, id, VIDEO_FILENAME)]) == 0:
                scrobble(id)
                return True
    return False

def describe(d):
    for e in sorted(d):
        print("%s - %s %s" % (e, d[e]['series'], d[e]['episode']))

if __name__ == '__main__':
    cmds = sorted(['watchable()', 'addable()', 'write_tag(id[, series][, episode])', 'write_loop()', 'unseen()', 'seen()', 'scrobble(id)', 'watch(id)', 'describe(dict)'])
    import code
    code.InteractiveConsole(locals=globals()).interact(cmds)
#    while True:
#        michiprint(input(" > "))
