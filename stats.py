from msbase.utils import load_json

import pandas as pd
import seaborn

results = load_json("results.json")

total = len(results)

print("Total: %s" % total)

counts = {}

shared_counts = {}

tool_set = set()

for result in results:
    tools = list(result["outputs"].keys())
    for tool in tools:
        tool_set.add(tool)
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
        if result["outputs"][t1]["status"] == result["outputs"][t2]["status"] and result["outputs"][t1]["status"] == "ok":
            shared_counts[pair] += 1

print(counts)
counts_md = pd.DataFrame.from_dict(counts).T.to_markdown()

tool_idx = list(enumerate(tool_set))
tool_names = [ tool for idx, tool in tool_idx ]
print(tool_idx)

mat = []
for i, tool in tool_idx:
    row = []
    for j, tool2 in tool_idx:
        if (tool, tool2) in shared_counts:
            row.append(shared_counts[(tool, tool2)])
        elif (tool2, tool) in shared_counts:
            row.append(shared_counts[(tool2, tool)])
        elif tool == tool2:
            row.append(counts[tool]["ok"])
        else:
            raise Exception((tool, tool2))
    mat.append(row)

print(shared_counts)
print(mat)

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

sns.heatmap(mat, xticklabels=tool_names, yticklabels=tool_names)
plt.tight_layout()
plt.savefig("heatmap.pdf")