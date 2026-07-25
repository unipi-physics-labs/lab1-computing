.PHONY: preview render clean test lint figures

preview:
	quarto preview

render:
	quarto render

clean:
	rm -rf _book .quarto

test:
	python -m pytest

lint:
	python -m ruff check src tests examples scripts

figures:
	python scripts/generate-figures.py