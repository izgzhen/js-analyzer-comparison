from msbase.utils import load_json

results = load_json("results.json")

total = len(results)

print("Total: %s" % total)

counts = {}

for result in results:
    for name, info in result.items():
        if name not in counts:
            counts[name] = {
                "ok": 0,
                "failure": 0
            }
        counts[name][info["status"]] += 1

print(counts)