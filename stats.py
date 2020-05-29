from msbase.utils import load_json

import pandas as pd
import seaborn

results = load_json("results.json")

total = len(results)

print("Total: %s" % total)

counts = {}
ok_shared_counts = {}
failure_shared_counts = {}

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
        if pair not in ok_shared_counts:
            ok_shared_counts[pair] = 0
        if pair not in failure_shared_counts:
            failure_shared_counts[pair] = 0
        t1, t2 = pair
        if result["outputs"][t1]["status"] == result["outputs"][t2]["status"]:
            if result["outputs"][t1]["status"] == "ok":
                ok_shared_counts[pair] += 1
            if result["outputs"][t1]["status"] == "failure":
                failure_shared_counts[pair] += 1

counts_md = pd.DataFrame.from_dict(counts).T.to_markdown(open("counts.md", "w"))

tool_idx = list(enumerate(tool_set))
tool_names = [ tool for idx, tool in tool_idx ]

def render_shared_heatmap(shared_counts, heatmap_output: str):
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

    import matplotlib.pyplot as plt
    import seaborn as sns; sns.set()

    sns.heatmap(mat, xticklabels=tool_names, yticklabels=tool_names)
    plt.tight_layout()
    plt.savefig(heatmap_output)
    plt.clf()

render_shared_heatmap(ok_shared_counts, "heatmap_ok.svg")
render_shared_heatmap(failure_shared_counts, "heatmap_failure.svg")