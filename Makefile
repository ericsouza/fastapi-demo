USER_UID_GID = $(shell id -u):$(shell id -g)

run: run-db
	@uvicorn fastapi_demo.main:app --reload

run-db:
	@USER_UID_GID=${USER_UID_GID} \
	docker-compose up -d fastapi-demo-db

stop:
	@docker-compose down

format:
	@isort fastapi_demo/ tests/
	@black .

lint:
	@echo "Syntax errors or undefined names:"
	@flake8 ./fastapi_demo --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "Format problems:"
	@flake8 ./fastapi_demo --count --max-complexity=10 --max-line-length=88 --statistic
