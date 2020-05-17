import os
import sys
import subprocess
import glob
from typing import Dict, Any

from msbase.utils import load_json, getenv
from msbase.subprocess_ import try_call_std

REMOTE_HOST = getenv("REMOTE_HOST")
REMOTE_DIR = getenv("REMOTE_DIR")

files = [
    "Makefile",
    "run.py",
    "safe/bin",
    "safe/target/scala-2.12/classes",
    "safe/lib_managed",
    "safe/lib",
    "TAJS/dist/tajs-all.jar",
    "wala-demo/target/wala-demo-1.0-SNAPSHOT-jar-with-dependencies.jar"
]

def rsync(relpath: str):
    print('sync ' + relpath)
    cmd = ["zrsync", relpath, REMOTE_HOST + ":" + REMOTE_DIR + "/" + relpath]
    try_call_std(cmd, print_cmd=False)

dir_files = {} # type: Dict[Any, Any]
for f in files:
    d = os.path.dirname(f)
    if d not in dir_files:
        dir_files[d] = set()
    dir_files[d].add(f)

print("SSH mkdir")
cmd = ["ssh", REMOTE_HOST, "mkdir", "-p" ] + [ REMOTE_DIR + "/" + d for d in dir_files.keys() ]
try_call_std(cmd, print_cmd=False)

for d, files in dir_files.items():
    print("Sync " + d)
    cmd = ["zrsync"] + list(files) + [REMOTE_HOST + ":" + REMOTE_DIR + "/" + d]
    try_call_std(cmd, print_cmd=False)