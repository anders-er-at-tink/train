from subprocess import run

from .commit import Commit

HEAD = """\
digraph g {
  concentrate=true
  node [shape=record,fontsize=9]
"""

FOOT = """\
}
"""


def show(commit: Commit):
    edges = "".join(f'  "{c}" -> "{p}"\n' for c in commit for p in c.parents)
    return HEAD + edges + FOOT


def display(commit: Commit):
    buf = show(commit)
    print(buf)
    run("dot -Tpng -s64 | display", shell=True, input=buf.encode('utf-8'))


pass

