TEMPLATES := $(shell find templates/ -type f -name "*.html")
CSS := $(shell find css/ -type f -name "*.css")

all: $(TEMPLATES) $(CSS) gen-pages.py
	python-dist/bin/python3 gen-pages.py

install: python-dist

python-dist: requirements.txt
	python3 -m venv $@
	source python-dist/bin/activate && pip3 install -r requirements.txt

update-requirements:
	source python-dist/bin/activate && pip3 freeze > requirements.txt

test:
	source python-dist/bin/activate && python3 -m http.server

clean:
	$(RM) index.html
	$(RM) -r s/

.PHONY: all clean install update-requirements test
