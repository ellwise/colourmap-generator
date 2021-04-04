format:
	black .

lint:
	flake8 --exclude __pycache__,venv .