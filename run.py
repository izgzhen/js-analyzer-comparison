from msbase.subprocess_ import try_call_std
from msbase.utils import log_progress
import glob

js_files = glob.glob("test262-master/test/**/*.js", recursive=True)
print("Total JS files: %s" % len(js_files))

for f in log_progress(js_files, print_item=True):
    stdout, stderr, code = try_call_std(["java", "-jar", "wala-demo/target/wala-demo-1.0-SNAPSHOT-jar-with-dependencies.jar", f], print_cmd=False, output=False, noexception=True)
    if code == 0:
        print("Success")
    else:
        print("Failure")
        print(stdout)
        print(stderr)