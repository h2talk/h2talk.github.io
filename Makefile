TEMPLATES := $(shell find templates/ -type f -name "*.html")
CSS := $(shell find css/ -type f -name "*.css")

all: $(TEMPLATES) $(CSS) gen-pages.py
	python-dist/bin/python3 gen-pages.py

install: python-dist

python-dist: requirements.txt
	python3 -m venv $@
	source $@/bin/activate && pip3 install -r requirements.txt

update-requirements:
	source $@/bin/activate && pip3 freeze > requirements.txt

clean:
	$(RM) index.html

.PHONY: all clean install update-requirements
