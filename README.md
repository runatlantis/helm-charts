# Atlantis <!-- omit in toc -->

[![Lint Code Base](https://github.com/runatlantis/helm-charts/actions/workflows/linter.yaml/badge.svg)](https://github.com/runatlantis/helm-charts/actions/workflows/linter.yaml)
[![Lint and Test Charts](https://github.com/runatlantis/helm-charts/actions/workflows/lint-test.yaml/badge.svg)](https://github.com/runatlantis/helm-charts/actions/workflows/lint-test.yaml)
[![Release Charts](https://github.com/runatlantis/helm-charts/actions/workflows/release.yaml/badge.svg)](https://github.com/runatlantis/helm-charts/actions/workflows/release.yaml)
[![pages-build-deployment](https://github.com/runatlantis/helm-charts/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/runatlantis/helm-charts/actions/workflows/pages/pages-build-deployment)

[Atlantis](https://www.runatlantis.io/) is a tool for safe collaboration on [Terraform](https://www.terraform.io/) repositories.

## Usage

[Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

Once Helm is set up properly, add the repository as follows:

```console
helm repo add runatlantis https://runatlantis.github.io/helm-charts
```

You can then run `helm search repo runatlantis` to see the charts.

## Commands

Run `make help` to check available commands.

## License

[Apache 2.0 License](../LICENSE).
