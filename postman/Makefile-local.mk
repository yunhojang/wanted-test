
TEST_SCRIPTS = $(wildcard *.sh)

test:
	@echo "+ $@"
	@for ts in ${TEST_SCRIPTS} ; do \
		echo "------------------------------------------------" ; \
		echo $$ts ; \
		echo "------------------------------------------------" ; \
		/bin/bash $$ts || true ; \
	done

.PHONY: test
