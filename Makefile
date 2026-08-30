.PHONY: preview render clean test lint figures

preview:
	quarto preview

pdf:
	quarto render --to pdf

render:
	quarto render

clean:
	rm -rf _book .quarto
	rm -rf figures/scripts/__pycache__

test:
	python -m pytest

lint:
	python -m ruff check src tests examples scripts

figures:
	python figures/scripts/run.py
