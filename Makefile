activate:
	source .env/bin/activate
init:

test:
	coverage run -m nose2 -v
	coverage report --omit '.env/*,tests/*'
test-report:
	coverage html --omit '.env/*,tests/*'
	open htmlcov/index.html

