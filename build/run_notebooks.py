import sys, time, nbformat, pathlib
from nbclient import NotebookClient
aus = pathlib.Path(sys.argv[1]); aus.mkdir(exist_ok=True)
for name in sys.argv[2:]:
    nb = nbformat.read(name, as_version=4)
    t = time.perf_counter()
    try:
        NotebookClient(nb, timeout=900, kernel_name="python3", resources={"metadata": {"path": "."}}).execute()
        print(f"OK   {name} {time.perf_counter()-t:.0f}s", flush=True)
    except Exception as e:
        print(f"FAIL {name}: {str(e)[-1500:]}", flush=True)
    nbformat.write(nb, aus / name)
