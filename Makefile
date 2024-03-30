.DEFAULT_GOAL := help

.PHONY: help
help: ## List targets & descriptions
	@cat Makefile* | grep -E '^[a-zA-Z\/_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: docs
docs: ## Build helm chart documentation
	@docker run --rm --volume "$$(pwd):/helm-docs" -u $$(id -u) jnorwood/helm-docs:latest
