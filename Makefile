install:
	pip install -r requirements.txt

run-api:
	uvicorn src.api.main:app --reload

run-cli:
	python src/cli/app.py

run-dashboard:
	python src/ui/dashboard.py

test:
	pytest -q