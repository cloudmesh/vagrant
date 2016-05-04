UNAME := $(shell uname)

BROWSER=firefox
ifeq ($(UNAME), Darwin)
BROWSER=open
endif
ifeq ($(UNAME), Windows)
BROWSER=/cygdrive/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe
endif
ifeq ($(UNAME), CYGWIN_NT-6.3)
BROWSER=/cygdrive/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe
endif

doc:
	sphinx-apidoc -f -o docs/source/code cloudmesh_vagrant
	cd docs; make html

test:
	echo $(UNAME)

publish:
	ghp-import -n -p docs/build/html

view:
	$(BROWSER) docs/build/html/index.html


install:
	python setup.py install

setup:
	python setup.py install

dist: clean setup
	python setup.py sdist --formats=gztar,zip
	python setup.py bdist
	python setup.py bdist_wheel

upload_test:
	python setup.py  sdist bdist bdist_wheel upload -r https://testpypi.python.org/pypi

upload:
	python setup.py  sdist bdist bdist_wheel upload -r https://pypi.python.org/pypi

log:
	gitchangelog | fgrep -v ":dev:" | fgrep -v ":new:" > ChangeLog
	git commit -m "chg: dev: Update ChangeLog" ChangeLog
	git push

######################################################################
# TESTING
######################################################################

pytest:
	make -f Makefile clean
	pip install -r requirements.txt
	python setup.py install
	cm register remote
	py.test tests

nosetest:
	make -f Makefile clean
	pip install -r requirements.txt
	python setup.py install
	cm register remote
	nosetests -v --nocapture tests

######################################################################
# CLEANING
######################################################################

clean:
	rm -rf *.zip
	rm -rf *.egg-info
	rm -rf *.eggs
	rm -rf docs/build
	rm -rf build
	rm -rf dist
	find . -name '__pycache__' -delete
	find . -name '*.pyc' -delete
	-pip uninstall cloudmesh_client -y
	rm -rf .tox

######################################################################
# TAGGING
######################################################################

tag:
	bin/new_version.sh

rmtag:
	python setup.py rmtag

