# RubberDuck


![lint](https://github.com/AEJaspan/LineDebugger/actions/workflows/pylint.yml/badge.svg)

![ci/cd](https://github.com/AEJaspan/LineDebugger/actions/workflows/python-app.yml/badge.svg)


## How To

### Setup

```bash
pip install poetry
poetry install
```

### To Run

```bash
poetry run linedebugger -s my_script.py -o my_output.md
```

### To Run in VS code

Use the VS code command to run and build a task. On Windows this is

```bash
ctrl + shift + B
```

Or via the VS code options panel, go:

```
Terminal -> Run Build Task
```

## ToDo:

* Add tooling (i.e. internet search)
* build out a full graph rag system
* use a qna with sources chain
* build a CLI
* make it into a decorator
* register app
* register on [vscode extensions](https://code.visualstudio.com/api/ux-guidelines/overview)
* apply for compute credits
