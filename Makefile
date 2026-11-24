# One entry point for the whole artifact. `make help` lists the targets.
#
#   make check-env   check the tools that must already be installed
#   make all         run the pipeline

# Run one recipe at a time even under `make -j`: the targets share .venv and
# the minds build, and parallel work would distort the benchmark timings.
.NOTPARALLEL:

.DEFAULT_GOAL := help

# Syncs the workspace first if needed, so every target works in a fresh clone.
UV_RUN := uv run --locked --all-packages --all-extras

# --no-daemon: leave no Gradle JVM behind. The runtime benchmarks would
# measure it, and kill it.
GRADLEW := ./gradlew --no-daemon

# Timed repetitions per benchmark configuration. Empty: each suite's own value.
REPS :=

.PHONY: help all check-env setup gen test minds bench bench-runtime qscores figures compare-figures editor serve clean

help:  ## List the targets
	@awk -F ':.*## ' '/^[a-z-]+:.*## / { printf "  %-15s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

all: setup gen test minds bench qscores figures  ## The whole pipeline, without Godot, the editor or the runtime benchmarks

check-env:  ## Check the required tools (Godot: warning only)
	@ok=1; \
	if command -v uv >/dev/null; then echo "ok       $$(uv --version)"; \
	else echo "MISSING  uv: https://docs.astral.sh/uv/"; ok=0; fi; \
	if out=$$(cd science_game/minds && $(GRADLEW) -q javaToolchains 2>&1); then \
		if echo "$$out" | grep -Eq 'Language Version: +21$$'; then echo "ok       JDK 21, found by the Gradle wrapper"; \
		else echo "ok       Gradle wrapper (no JDK 21 found: the build downloads one)"; fi; \
	else echo "$$out" | head -5; echo "MISSING  a JDK >= 17 that can run the Gradle wrapper (or no network for its first download)"; ok=0; fi; \
	want=$$(cat editor/.nvmrc); \
	if ! command -v node >/dev/null; then echo "MISSING  Node $$want (editor only): https://nodejs.org/"; ok=0; \
	elif [ "$$(node -p 'process.versions.node.split(".")[0]')" = "$$want" ]; then echo "ok       Node $$(node --version)"; \
	else echo "WRONG    Node $$(node --version), the editor needs $$want"; ok=0; fi; \
	godot=$$(command -v godot || command -v godot4 || true); \
	version=$$([ -n "$$godot" ] && "$$godot" --version 2>/dev/null || true); \
	case "$$version" in \
		4.7|4.7.*) echo "ok       Godot $$version";; \
		"") echo "warning  Godot not on the PATH; playing the game needs 4.7";; \
		*) echo "warning  Godot $$version; the game needs 4.7";; \
	esac; \
	[ $$ok = 1 ]

setup:  ## Create .venv with the locked Python and dependencies
	uv sync --locked --all-packages --all-extras

gen:  ## Transpile the game's .regia sources to AgentSpeak
	cd science_game/minds && $(GRADLEW) compileRegia

test:  ## Run the transpiler's tests
	cd language && $(UV_RUN) pytest

minds:  ## Build the game's agents, without running them
	cd science_game/minds && $(GRADLEW) classes

bench:  ## Rerun the compile benchmarks (REPS=1 for a quick pass)
	cd language && $(UV_RUN) python -m benchmarks run --all $(if $(REPS),--reps $(REPS))

bench-runtime:  ## Rerun the runtime benchmarks (opt-in; kills other running Gradle and JaCaMo JVMs)
	cd language && $(UV_RUN) python -m benchmarks.runtime run --all

qscores:  ## Recompute the questionnaire scores and compare them with the paper's
	$(UV_RUN) python qscores/compute_metrics.py
	$(UV_RUN) python qscores/compare_reference.py

# The paper's fits are redrawn from its own runs; a rerun's plots and fits
# need `make bench` first.
figures: qscores  ## Redraw the figures (those of the benchmark rerun need `make bench` first)
	$(UV_RUN) python qscores/make_figures.py
	cd language && $(UV_RUN) python benchmarks/bench_fits.py benchmarks/reference --out benchmarks/results/reference_fits --format png
	@if [ -d language/benchmarks/results/interaction_full_game_case_study ]; then \
		set -ex; cd language; \
		$(UV_RUN) python -m benchmarks plot --all; \
		$(UV_RUN) python benchmarks/bench_fits.py benchmarks/results --format png; \
	else echo "No benchmark rerun to plot: run 'make bench' first."; fi

# Not in `all`: another CPU or OS may draw a pixel differently. CI runs it.
compare-figures: figures  ## Redraw the figures and compare those drawn from the paper's data, pixel by pixel
	$(UV_RUN) python qscores/compare_figures.py
	$(UV_RUN) python qscores/compare_figures.py language/benchmarks/results/reference_fits language/benchmarks/reference/fits

editor:  ## Build the visual editor
	cd editor && npm ci && npm run build

serve:  ## Start the editor's API server on 127.0.0.1:8000
	$(UV_RUN) regia serve

# Keeps .venv and editor/node_modules.
clean:  ## Delete everything the targets generate, except the installed dependencies
	rm -rf science_game/minds/build science_game/minds/.gradle science_game/minds/bin
	rm -rf science_game/minds/src/agt/gen science_game/minds/logs
	rm -rf language/benchmarks/results language/.pytest_cache
	rm -rf qscores/results qscores/figures
	rm -rf editor/dist
	find language qscores -name __pycache__ -type d -prune -exec rm -rf {} +
