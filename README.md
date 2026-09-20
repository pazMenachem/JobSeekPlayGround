# JobSeekPlayGround

A practice repository, not a product. It is where I work through things I want to be able to do from memory rather than from a tutorial — build pipelines, design patterns, data structures, and one security demo.

It is public because the working is the point. Two directories here are substantial; the rest are exercises at varying stages, and the map below says which is which so you do not have to click around to find out.

## Where the substance is

### `calculatorCICD` — the pipeline, not the calculator

The calculator is four arithmetic functions. It exists only to give the pipeline something to act on, and the pipeline is the actual project.

[`.github/workflows/calculatorCICD-ci.yml`](.github/workflows/calculatorCICD-ci.yml) runs four jobs:

- **test** — a matrix across Python 3.11 and 3.12, with flake8, `black --check`, `mypy`, and pytest with coverage. Results and HTML coverage upload as artifacts with `if: always()`, so a failed run still leaves something to read.
- **security** — `safety` for known CVEs in dependencies and `bandit` for static analysis, running *in parallel* with tests rather than after them. Both are suffixed `|| true`: they report without gating, which was a deliberate choice for a learning repo and would be the wrong default in a real one.
- **docker** — `needs: test`, so an image is only built from code that passed.
- **summary** — `if: always()`, collecting job results into the GitHub step summary.

Two decisions worth naming. The workflow is **path-filtered** to `calculatorCICD/**`, because this repository is a monorepo of unrelated exercises and a change to a C++ file has no business triggering a Python pipeline. And the same checks are mirrored in [`calculatorCICD/run.sh`](calculatorCICD/run.sh), so the pipeline can be reproduced locally before pushing instead of debugging it through commit-and-wait cycles.

Tooling config is centralised in `pyproject.toml` — pytest, coverage exclusions, black, and mypy with `disallow_untyped_defs`, which is what forces the type hints to actually exist rather than being optional.

### `Cyber/CsrfAttack` — a vulnerability and its fix, side by side

Two Flask "banking" apps and a malicious page. The vulnerable app accepts a state-changing POST with no token; `attack.html` is a cross-origin auto-submitting form that drains $100 from the logged-in session. The protected app rejects the same request.

The design decision is that both apps exist. Running them on ports 5000 and 5001 makes the fix a diff you can execute rather than a paragraph you have to believe. The protection itself is deliberately hand-rolled — a `secrets.token_hex(16)` per session, echoed into the form and compared on submit — because wiring up Flask-WTF would have hidden the mechanism being demonstrated.

Both apps use plaintext passwords and a dictionary for storage. That is intentional for a demo and is called out in its own [README](Cyber/CsrfAttack/README.md).

### `design_patterns` — 11 GoF patterns in C++

Factory, Observer, Prototype, Builder, Singleton, Strategy, Template Method, Decorator, State, Facade, Adapter. Each is a standalone file with a runnable example. These are complete.

## Everything else, honestly

| Directory | State |
| --- | --- |
| `DataStructures` | BST, linked list, vector and queue are implemented. **`HashTable.cpp`, `Tries.cpp`, `Graph.cpp` and `Heaps.cpp` are empty placeholders**, and `Stack.cpp` is a single line. |
| `Algorithms` | Binary search, merge sort and quicksort are implemented. **`BFS.cpp` is an empty placeholder.** |
| `CrakingTheCodeQuestions` | Chapter 1 solved in JavaScript against Jest specs, chapters 2–3 in Python against pytest. Written test-first — the assertions came before the implementations. |
| `ceva_ip` | A linked list and a small memory exercise in C. |
| `selenium` | A booking-site scraper built as a Page Object-style wrapper class. |
| `FullStackBootCamp` | Course exercises (HTML/CSS/Express/EJS). Included for completeness; there is nothing of mine to judge here. |

## Running the pipeline project

```bash
cd calculatorCICD
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e ".[dev]"
./run.sh          # runs the same checks the CI pipeline runs
```
