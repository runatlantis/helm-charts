.DEFAULT_GOAL := help

.PHONY: help
help: ## List targets & descriptions
	@cat Makefile* | grep -E '^[a-zA-Z\/_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: docs
docs: ## Build helm chart documentation
	@docker pull jnorwood/helm-docs:latest
	@docker run --rm --volume "$$(pwd):/helm-docs" -u $$(id -u) jnorwood/helm-docs:latest

.PHONY: unit-test-install
unit-test-install:
	@helm plugin list | grep unittest || helm plugin install --version v1.0.2 https://github.com/helm-unittest/helm-unittest

.PHONY: unit-test-run-atlantis
unit-test-run-atlantis: unit-test-install ## Run unit tests for Atlantis
	@helm unittest ./charts/atlantis
