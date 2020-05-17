from msbase.subprocess_ import try_call_std, multiprocess
from msbase.utils import log_progress, write_pretty_json

import random
import glob
import time
import os

js_files = glob.glob("test262-master/test/**/*.js", recursive=True)
print("Total JS files: %s" % len(js_files))

def tajs_cmd(js_path: str):
    return ["java", "-jar", "TAJS/dist/tajs-all.jar", js_path]

def wala_cmd(js_path: str):
    return ["java", "-jar", "wala-demo/target/wala-demo-1.0-SNAPSHOT-jar-with-dependencies.jar", js_path]

def safe_cmd(js_path: str):
    return ["safe/bin/safe", "cfgBuild", js_path]

tools = {
    "tajs": tajs_cmd,
    "wala": wala_cmd,
    "safe": safe_cmd
}

NPROC = 4
if os.getenv("NPROC") is not None:
    NPROC = int(os.getenv("NPROC")) # type: ignore


NSAMPLES = 20
if os.getenv("NSAMPLES") is not None:
    NSAMPLES = int(os.getenv("NSAMPLES")) # type: ignore

random.seed(0)

tasks = random.sample(js_files, k=NSAMPLES)

def process(f: str):
    result = {}
    for name, get_cmd in tools.items():
        now = time.time()
        stdout, stderr, code = try_call_std(get_cmd(f), print_cmd=False, output=False, noexception=True)
        duration_seconds = time.time() - now
        if code == 0:
            result[name] = {
                "status": "ok",
                "duration_seconds": duration_seconds
            }
        else:
            result[name] = {
                "status": "failure",
                "duration_seconds": duration_seconds
            }
    return result

results = multiprocess(process, tasks, return_dict=False, n=NPROC, throws=True)

write_pretty_json(results, "results.json")