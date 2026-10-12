import json, sys
src, out = sys.argv[1], sys.argv[2]
nb = json.load(open(src, encoding="utf-8"))
with open(out, "w", encoding="utf-8") as f:
    for i, c in enumerate(nb["cells"]):
        hidden = c.get("metadata", {}).get("jupyter", {}).get("source_hidden")
        f.write(f"\n### [{i}] {c['cell_type']}{' (code collapsed)' if hidden else ''}\n")
        f.write("".join(c["source"]) + "\n")
        for o in c.get("outputs", []):
            if o.get("name") == "stdout":
                f.write("--- output:\n" + "".join(o["text"]))
            elif o.get("output_type") == "error":
                f.write(f"--- error: {o['ename']}: {o['evalue']}\n")
            elif "data" in o and ("text/html" in o["data"] or "application/vnd.plotly.v1+json" in o["data"]):
                f.write("--- output: [interactive plot]\n")
