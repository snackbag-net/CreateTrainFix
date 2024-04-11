from pathlib import Path
from sys import stdout as terminal
from time import sleep
import itertools
from threading import Thread


class Storage:
    loading_finished = True


def path_to_file() -> Path:
    return Path("input/create_tracks.dat")


def track_file_exists() -> bool:
    return path_to_file().exists()


def animate():
    Storage.loading_finished = False
    lst = ["|", "-"]
    i = 0
    while not Storage.loading_finished:
        terminal.write('\rloading ' + lst[i])
        terminal.flush()
        i += 1
        if i > len(lst) - 1:
            i = 0
        sleep(0.5)
    terminal.flush()


def start_loading_thread():
    t = Thread(target=animate)
    t.start()
