from msbase.utils import load_json

results = load_json("results.json")

total = len(results)

print("Total: %s" % total)

counts = {}

shared_counts = {}

for result in results:
    tools = list(result["outputs"].keys())
    tool_pairs = [ (tools[i], tools[j]) for i in range(0, len(tools) - 1) for j in range(i + 1, len(tools))]
    for name, info in result["outputs"].items():
        if name not in counts:
            counts[name] = {
                "ok": 0,
                "failure": 0
            }
        counts[name][info["status"]] += 1
    for pair in tool_pairs:
        if pair not in shared_counts:
            shared_counts[pair] = 0
        t1, t2 = pair
        if result["outputs"][t1]["status"] == result["outputs"][t2]["status"]:
            shared_counts[pair] += 1

print(counts)
print(shared_counts)