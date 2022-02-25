.PHONY: all help run collect deps migrate freeze
FILENAME := .appname
APPNAME := `cat $(FILENAME)`

# target: run - Runs a dev server on localhost:8000
run:
	manage runserver

# target: migrate - migrate the database
migrate:
	manage makemigrations
	manage migrate

# target: deps - install dependencies from requirements file
deps:
	pip install -r requirements.txt
	pip install -e .	

# target: sh - open django extension's shell plus
sh:
	manage shell_plus

# target: db - open django DB shell
db:
	manage dbshell	

