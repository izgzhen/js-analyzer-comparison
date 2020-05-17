from msbase.subprocess_ import try_call_std
from msbase.utils import log_progress
import glob

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

for f in log_progress(js_files, print_item=True):
    for name, get_cmd in tools.items():
        stdout, stderr, code = try_call_std(get_cmd(f), print_cmd=False, output=False, noexception=True)
        if code == 0:
            print("[%s] Success" % name)
        else:
            print("[%s] Failure" % name)
            print(stdout)
            print(stderr)