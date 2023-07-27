.ONESHELL:

.PHONY: publish
publish:
	@poetry publish --build --username __token__ --password ${PYPI_PDX_KEY} --build --skip-existing

.PHONY: test
test:
	pytest
# make test -s 