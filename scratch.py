from train.commit import *

from train.viz import *


def make_ex1():
    root = Commit()
    master = root.commit("ma").commit("mb").commit("mc")
    b1 = master.commit("1a").commit("1b").commit("1c")
    b2 = master.commit("2a").commit("2b")
    return root, master, b1, b2


def make_knobby():
    root = Commit("root")
    feat = root.commit("f1").commit("f2").commit("f3")
    merge = root.commit("merge feat", feat)
    return merge


root, master, b1, b2 = make_ex1()
knobby = make_knobby()

display(Commit("merge!", (b1, b2)))

display(knobby)
