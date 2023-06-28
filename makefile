.ONESHELL:

.PHONY: publish
publish:
	@poetry publish --build --username __token__ --password $(PYPI_MODELSTAR_KEY).SILENT: --build --skip-existing