venv: requirements.txt
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

.PHONY: setup
setup: venv

.PHONY: run
run:
	venv/bin/python3 color.py

.PHONY: clean
clean:
	rm -rf venv
