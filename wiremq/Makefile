TEST_PATH=./tests
PROJ_ROOT_DIR=./wmqlib
.PHONY: init clean-all build clean-pyc clean-build test

requirements:
	python3 -m pip install -r requirements.txt

requirements-user:
	python3 -m pip install -r requirements.txt --user


directories:
	mkdir -p ~/.wiremq/{message_db,domain_sockets,logs}

build:
	pip3 install wiremq-0.0.1-py3-none-any.whl --force-reinstall

clean:
	rm -rf ~/.wiremq/domain_sockets
	rm -rf ~/.wiremq/message_db
	rm -rf ~/.wiremq/logs

help:
	@echo "  requirements"
	@echo "		Install the project requirements"
	@echo "  requirements-user"
	@echo "		Install the project requirements --user flag"
	@echo "  directories"
	@echo "		Initialises WireMQ directories"
	@echo "  build"
	@echo "		Build WireMQ libraries"
	@echo "  clean"
	@echo "		Remove database and socket artifacts"

