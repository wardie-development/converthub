port ?= 8000

run:
	chalice local --port=$(port)

install-requirements:
	pip install -r requirements/base.txt && \
	pip install -r requirements/tests.txt

pip-compile:
	rm -f requirements/base.txt
	rm -f requirements/tests.txt
	rm -f requirements/dev.txt
	rm -f requirements/deploy.txt

	pip-compile requirements/base.in
	pip-compile requirements/tests.in
	pip-compile requirements/dev.in
	pip-compile requirements/deploy.in

build:
	pip install pip-tools
	make install-requirements

test:
	pytest -s -vv $(path) --durations=5 --cov-report term-missing:skip-covered --cov=. -W ignore::DeprecationWarning

check-lint:
	black -S -t py38 -l 79 --check . --exclude '/(\.git|venv|env|build|dist)/'

check-safety:
	safety check -i 52495

lint:
	black -S -t py38 -l 79 . --exclude '/(\.git|venv|env|build|dist)/'

deploy:
	python -m pip install --upgrade pip
	pip install -r requirements/base.txt
	pip install -r requirements/deploy.txt

	aws configure set region us-east-1
	aws configure set output json
	aws configure set aws_access_key_id $(AWS_ACCESS_KEY_ID)
	aws configure set aws_secret_access_key $(AWS_SECRET_ACCESS_KEY)

	pip freeze > requirements.txt

	chalice deploy --stage $(stage)

cf-stack:
	aws cloudformation $(action)-stack \
	--stack-name ChaliceDeployUserStack \
	--template-body file://user-stack.yml \
	--capabilities CAPABILITY_NAMED_IAM
