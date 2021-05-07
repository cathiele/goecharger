
.PHONY: activate init test test-report lint

activate:
	echo "Please run: source .env/bin/activate"
init:
	echo "Please run: python -m venv .env"

test:
	coverage run -m nose2 -v
	coverage report --omit '.env/*,tests/*'
test-report:
	coverage html --omit '.env/*,tests/*'
	open htmlcov/index.html
lint:
	flake8 goecharger --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 goecharger --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
