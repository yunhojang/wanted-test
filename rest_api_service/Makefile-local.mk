
APP_NAME ?= rest_api_service
APP_BUILD_ENV ?= local
DOCKER_COMPOSE_FILE ?= docker-compose-local.yaml

.PHONY: dc-build
dc-build:
	@echo "+ $@"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} build --build-arg BUILD_ENV=${APP_BUILD_ENV}

.PHONY: dc-run
dc-run: dc-build
	@echo "+ $@"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up

.PHONY: dc-service
dc-service: dc-build
	@echo "+ $@"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d

.PHONY: dc-shell
dc-shell: dc-build
	@echo "+ $@"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm --entrypoint bash ${APP_NAME}

.PHONY: dc-test
dc-test: dc-build
	@echo "+ $@"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm ${APP_NAME} -m pytest -v tests

.PHONY: dc-stop
dc-stop:
	@echo "+ $@"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} stop

.PHONY: dc-down
dc-down:
	@echo "+ $@"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} down --remove-orphans

.PHONY: dc-clean
dc-clean:
	@echo "+ $@"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} down --remove-orphans --rmi all 2>/dev/null
