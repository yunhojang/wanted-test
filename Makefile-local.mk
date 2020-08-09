
APPS ?= \
	rest_api_service

DOCKER_NETWORK_NAME = wanted_test

INFRA_DOCKER_COMPOSE_FILE = infra/docker-compose-local.yaml

network:
	@docker network inspect ${DOCKER_NETWORK_NAME} >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)

network-clean:
	@docker network rm ${DOCKER_NETWORK_NAME} >/dev/null 2>&1 || true

infra: network
	@LOCAL_NETWORK_NAME=${DOCKER_NETWORK_NAME} docker-compose -f ${INFRA_DOCKER_COMPOSE_FILE} up -d

infra-down:
	@docker-compose -f ${INFRA_DOCKER_COMPOSE_FILE} down

infra-clean:
	@docker-compose -f ${INFRA_DOCKER_COMPOSE_FILE} down --remove-orphans --rmi all 2>/dev/null

insert-sample:
	@cd infra/sample && python insert_company_infos.py ; cd -;

service: network
	@for dir in $(APPS); do \
		cd $$dir && make -f Makefile-local.mk dc-service ; cd -; \
	done

service-clean:
	@for dir in $(APPS); do \
		cd $$dir && make -f Makefile-local.mk dc-clean ; cd -; \
	done

unit-test: clean infra service
	@for dir in $(APPS); do \
		cd $$dir && make -f Makefile-local.mk dc-test ; cd -; \
	done

service-test: clean infra service insert-sample
	@cd postman && make -f Makefile-local.mk test && cd -

clean: service-clean infra-clean network-clean

.PHONY: clean network network-clean infra infra-down infra-clean insert-sample service service-clean service-test postman-test
