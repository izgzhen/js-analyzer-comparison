from msbase.subprocess_ import try_call_std, multiprocess
from msbase.utils import log_progress, write_pretty_json

import random
import glob
import time
import os

js_files = glob.glob("test262-master/test/**/*.js", recursive=True)
js_files += glob.glob("jsnice/data/**/*.js", recursive=True)
print("Total JS files: %s" % len(js_files))

run_kwargs = {
    "print_cmd": False,
    "output": False,
    "noexception": True,
    "timeout_s": 10
}

def cc_cmd(js_path: str):
    out = js_path.replace(".js", ".js_cc")
    _, _, code = try_call_std(["java", "-jar", "lib/closure-compiler-v20200112.jar", "--debug",
                                "--formatting=PRETTY_PRINT", "--js", js_path, "--js_output_file", out], **run_kwargs)
    return code == 0

def with_cc_wrapper(f):
    def wrapped(js_path):
        cc = js_path.replace(".js", ".js_cc")
        if os.path.exists(cc):
            return f(cc)
        else:
            return None
    return wrapped

def tajs_cmd(js_path: str):
    _, _, code = try_call_std(["java", "-jar", "TAJS/dist/tajs-all.jar", js_path], **run_kwargs)
    return code == 0

def wala_cmd(js_path: str):
    _, _, code = try_call_std(["java", "-jar", "wala-demo/target/wala-demo-1.0-SNAPSHOT-jar-with-dependencies.jar", js_path], **run_kwargs)
    return code == 0

def safe_cmd(js_path: str):
    out = js_path.replace(".js", ".safe_ast")
    stdout, stderr, code = try_call_std(["safe/bin/safe", "parse", "-parser:out=%s" % out, js_path], **run_kwargs)
    return os.path.exists(out)

# The order is important
tools = [
    ("cc", cc_cmd),
    ("tajs", tajs_cmd),
    ("wala", wala_cmd),
    ("safe", safe_cmd),
    ("cc_tajs", with_cc_wrapper(tajs_cmd)),
    ("cc_wala", with_cc_wrapper(wala_cmd)),
    ("cc_safe", with_cc_wrapper(safe_cmd))
]

NPROC = 4
if os.getenv("NPROC") is not None:
    NPROC = int(os.getenv("NPROC")) # type: ignore


NSAMPLES = 20
if os.getenv("NSAMPLES") is not None:
    NSAMPLES = int(os.getenv("NSAMPLES")) # type: ignore

random.seed(0)

tasks = random.sample(js_files, k=NSAMPLES)

def process(f: str):
    result = {
        "file": f,
        "outputs": {}
    }
    for name, cmd in tools:
        now = time.time()
        success = cmd(f)
        duration_seconds = time.time() - now
        if success:
            result["outputs"][name] = {
                "status": "ok",
                "duration_seconds": duration_seconds
            }
        else:
            result["outputs"][name] = {
                "status": "failure",
                "duration_seconds": duration_seconds
            }
    return result

results = multiprocess(process, tasks, return_dict=False, n=NPROC, throws=True)

write_pretty_json(results, "results.json")