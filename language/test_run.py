from benchmarks.experiments import EXPERIMENTS
from benchmarks.generator import generate
from regia.compiler import compile_source
from pathlib import Path
from benchmarks.runtime_bench import prepare_runtime_project, run_jason_benchmark
import os, subprocess, shutil

cfg = EXPERIMENTS["scale_roles"][0]
src = generate(cfg)
res = compile_source(src, emit=True)

out_dir = Path("results/debug_mas")
out_dir.mkdir(parents=True, exist_ok=True)
for fname, fcontent in res.outputs.items():
    (out_dir / fname).write_text(fcontent)
    
prepare_runtime_project(out_dir, cfg)

dur, ram = run_jason_benchmark(out_dir)
print(f"DURATION: {dur}, RAM: {ram}")
