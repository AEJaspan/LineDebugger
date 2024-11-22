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
* build out a full [graph rag system](https://cookbook.openai.com/examples/rag_with_graph_db)
* use a [qna with sources chain](https://python.langchain.com/api_reference/langchain/chains/langchain.chains.qa_with_sources.retrieval.RetrievalQAWithSourcesChain.html)
* build a CLI
* make it into a decorator
* register app
* register on [vscode extensions](https://code.visualstudio.com/api/ux-guidelines/overview)
* apply for compute credits


## Resources:


* [Code4UIE](https://github.com/YucanGuo/Code4UIE) - uses python classes to define schemas for entities, relations and events
* [Code Property Graph (CPG) - retrieval augmented code summarisation via hybrid ANN](https://arxiv.org/abs/2006.05405)
* `code-cushman-001` - codex for code gen
* [CodeBERT](https://github.com/microsoft/CodeBERT) for code embeddings
* [Inferfix: End-to-end program repair with llms](https://www.microsoft.com/en-us/research/publication/inferfix-end-to-end-program-repair-with-llms-over-retrieval-augmented-prompts/)
* [Retrieval augmented patch generation with codet5](https://github.com/wang-weishi/RAP-Gen)
* [Syntax Aware retrieval - kNN TRANX](https://github.com/NUAAZXY/kNN-TRANX)
* [BASHEXPLAINERs Dual retrieval method](https://arxiv.org/pdf/2206.13325)
