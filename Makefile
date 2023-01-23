install:
	pip install -r requirements.txt

test:
	python -m unittest discover

lint:
	pylint src/*.py

run:
	python src/main.py

clean:
	rm -rf dist
	rm -rf build
	rm -rf Project_Name.egg-info

build: clean
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/*
