# Atlantis <!-- omit in toc -->

[![Lint Code Base](https://github.com/runatlantis/helm-charts/actions/workflows/linter.yaml/badge.svg)](https://github.com/runatlantis/helm-charts/actions/workflows/linter.yaml)
[![Lint and Test Charts](https://github.com/runatlantis/helm-charts/actions/workflows/lint-test.yaml/badge.svg)](https://github.com/runatlantis/helm-charts/actions/workflows/lint-test.yaml)
[![Release Charts](https://github.com/runatlantis/helm-charts/actions/workflows/release.yaml/badge.svg)](https://github.com/runatlantis/helm-charts/actions/workflows/release.yaml)
[![pages-build-deployment](https://github.com/runatlantis/helm-charts/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/runatlantis/helm-charts/actions/workflows/pages/pages-build-deployment)

[Atlantis](https://www.runatlantis.io/) is a tool for safe collaboration on [Terraform](https://www.terraform.io/) repositories.

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Required Configuration](#required-configuration)
- [Additional manifests](#additional-manifests)
- [Customization](#customization)
- [Upgrading](#upgrading)
  - [From `2.*` to `3.*`](#from-2-to-3)
  - [From `1.*` to `2.*`](#from-1-to-2)
- [Testing the Deployment](#testing-the-deployment)

## Introduction
This chart creates a single pod in a StatefulSet running Atlantis.  Atlantis persists Terraform [plan files](https://www.terraform.io/docs/commands/plan.html) and [lockfiles](https://www.terraform.io/docs/state/locking.html) to disk for the duration of a Pull/Merge Request.  These files are stored in a PersistentVolumeClaim to survive Pod failures.

## Prerequisites
- Kubernetes 1.9+
- PersistentVolume support

## Required Configuration
In order for Atlantis to start and run successfully:
1. At least one of the following sets of credentials must be defined:
    - `github`
    - `gitlab`
    - `bitbucket`
    - `azuredevops`

    Refer to [values.yaml](/charts/atlantis/values.yaml) for detailed examples.
    They can also be provided directly through a Kubernetes `Secret`, use the variable `vcsSecretName` to reference it.

1. Supply a value for `orgAllowlist`, e.g. `github.com/myorg/*`.

## Additional manifests

It is possible to add additional manifests into a deployment, to extend the chart. One of the reason is to deploy a manifest specific to a cloud provider ( BackendConfig on GKE for example ).

```yaml
extraManifests:
  - apiVersion: cloud.google.com/v1beta1
    kind: BackendConfig
    metadata:
      name: "{{ .Release.Name }}-test"
    spec:
      securityPolicy:
        name: "gcp-cloud-armor-policy-test"
```

## Customization
The following options are supported.  See [values.yaml](/charts/atlantis/values.yaml) for more detailed documentation and examples:

| Parameter                                   | Description                                                                                                                                                                                                                                                                                               | Default |
|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `dataStorage`                               | DEPRECATED - Amount of storage available for Atlantis' data directory (mostly used to check out git repositories).                                                                                                                                                                                        | `5Gi`   |
| `volumeClaim.enabled`                       | Activate embedded volume claim for Atlantis' data directory (mostly used to check out git repositories).                                                                                                                                                                                                  | `true`  |
| `volumeClaim.dataStorage`                   | Amount of storage available for embedded Atlantis' data directory                                                                                                                                                                                                                                         | `5Gi`   |
| `volumeClaim.storageClassName`              | Storage class of the embedded volume mounted for the Atlantis data directory.                                                                                                                                                                                                                             | n/a     |
| `atlantisUrl`                               | Base URL of atlantis server. This URL also reflects in pull-requests CI hooks where terraform changes are displayed.                                                                                                                                                                                                     | n/a |
| `aws.config`                                | Contents of a file to be mounted to `~/.aws/config`.                                                                                                                                                                                                                                                      | n/a     |
| `aws.credentials`                           | Contents of a file to be mounted to `~/.aws/credentials`.                                                                                                                                                                                                                                                 | n/a     |
| `awsSecretName`                             | Secret name containing AWS credentials - will override aws.credentials and aws.config. Will be used a volume mount on `$HOME/.aws`, so it needs a `credentials` key. The key `config` is optional. See the file `templates/secret-aws.yml` for more info on the Secret contents.                                                                                                                                     | n/a     |
| `bitbucket.user`                            | Name of the Atlantis Bitbucket user.                                                                                                                                                                                                                                                                      | n/a     |
| `bitbucket.token`                           | Personal access token for the Atlantis Bitbucket user.                                                                                                                                                                                                                                                    | n/a     |
| `bitbucket.secret`                          | Webhook secret for Bitbucket repositories (Bitbucket Server only).                                                                                                                                                                                                                                        | n/a     |
| `bitbucket.baseURL`                         | Base URL of Bitbucket Server installation.                                                                                                                                                                                                                                                                | n/a     |
| `environment`                               | Map of environment variables for the container.                                                                                                                                                                                                                                                           | `{}`    |
| `environmentSecrets`                        | Array of Kubernetes secrets that can be used to set environment variables. See `values.yaml` for example.                                                                                                                                                                                                 | `{}`    |
| `environmentRaw`                            | Array environment variables in plain Kubernetes yaml format. See `values.yaml` for example.                                                                                                                                                                                                               | `[]`    |
| `loadEnvFromSecrets`                        | Array of Kubernetes secrets to set all key-value pairs as environment variables. See `values.yaml` for example.                                                                                                                                                                                           | `[]`    |
| `loadEnvFromConfigMaps`                     | Array of Kubernetes `ConfigMap`s to set all key-value pairs as environment variables. See `values.yaml` for example.                                                                                                                                                                                      | `[]`    |
| `extraVolumes`                              | List of additional volumes available to the pod.                                                                                                                                                                                                                                                          | `[]`    |
| `extraVolumeMounts`                         | List of additional volumes mounted to the container.                                                                                                                                                                                                                                                      | `[]`    |
| `imagePullSecrets`                          | List of secrets for pulling images from private registries.                                                                                                                                                                                                                                               | `[]`    |
| `gitconfig`                                 | Contents of a file to be mounted to `~/.gitconfig`.  Use to allow redirection for Terraform modules in private git repositories.                                                                                                                                                                          | n/a     |
| `gitconfigSecretName`                       | Name of a pre-existing Kubernetes `Secret` containing a `gitconfig` key. Use this instead of `gitconfig` (optional)                                                                                                                                                                           | n/a     |
| `command`                                   | Optionally override the [`command` field](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#container-v1-core) of the Atlantis Docker container. If not set, the default Atlantis `ENTRYPOINT` is used. Must be an array.                                                                                                                                  | n/a     |
| `github.user`                               | Name of the Atlantis GitHub user.                                                                                                                                                                                                                                                                         | n/a     |
| `github.token`                              | Personal access token for the Atlantis GitHub user.                                                                                                                                                                                                                                                       | n/a     |
| `github.secret`                             | Repository or organization-wide webhook secret for the Atlantis GitHub integration. All repositories in GitHub that are to be integrated with Atlantis must share the same value.                                                                                                                         | n/a     |
| `github.hostname`                           | Hostname of your GitHub Enterprise installation.                                                                                                                                                                                                                                                          | n/a     |
| `githubApp.id`                              | GitHub app ID. If set, GitHub authentication will be performed as an [installation](https://developer.github.com/v3/apps/installations/).                                                                                                                                                                 | n/a     |
| `githubApp.key`                             | A GitHub App PEM encoded private key file. If set, GitHub authentication will be performed as an [installation]((https://developer.github.com/v3/apps/installations/)).                                                                                                                                   | n/a     |
| `githubApp.secret`                          | Secret used to validate GitHub webhooks (see [Securing your webhooks](https://developer.github.com/webhooks/securing/)).                                                                                                                                                                                                            | n/a     |
| `gitlab.user`                               | Repository or organization-wide secret for the Atlantis GitLab,integration. All repositories in GitLab that are to be integrated with Atlantis must share the same value.                                                                                                                                 | n/a     |
| `gitlab.token`                              | Personal access token for the Atlantis GitLab user.                                                                                                                                                                                                                                                       | n/a     |
| `gitlab.secret`                             | Webhook secret for the Atlantis GitLab integration. All repositories in GitLab that are to be integrated with Atlantis must share the same value.                                                                                                                                                         | n/a     |
| `gitlab.hostname`                           | Hostname of your GitLab Enterprise installation.                                                                                                                                                                                                                                                          | n/a     |
| `azuredevops.user`                          | Repository or organization-wide secret for the Atlantis Azure DevOps,integration. All repositories in Azure DevOps that are to be integrated with Atlantis must share the same value.                                                                                                                                 | n/a     |
| `azuredevops.token`                         | Personal access token for the Atlantis Azure DevOps user.                                                                                                                                                                                                                                                       | n/a     |
| `azuredevops.webhookUser`                   | Webhook user for the Atlantis Azure DevOps integration.                                                                                                                                                                                                                                                          | n/a     |
| `azuredevops.webhookPassword`               | Webhook password for the Atlantis Azure DevOps integration. All repositories in Azure DevOps that are to be integrated with Atlantis must share the same value.                                                                                                                                                         | n/a     |
| `vcsSecretName`                             | Name of a pre-existing Kubernetes `Secret` containing `token` and `secret` keys set to your VCS provider's API token and webhook secret, respectively. Use this instead of `github.token`/`github.secret`, etc. (optional) | n/a |
| `podTemplate.annotations`                   | Additional annotations to use for the StatefulSet.                                                                                                                                                                                                                                                        | n/a     |
| `podTemplate.annotations`                   | Additional annotations to use for pods. | `{}` |
| `podTemplate.labels`                        | Additional labels to use for pods. | `{}` |
| `statefulSet.annotations`                   | Additional annotations to use for StatefulSet. | `{}` |
| `statefulSet.labels`                        | Additional labels to use for StatefulSet. | `{}` |
| `terminationGracePeriodSeconds`             | Set terminationGracePeriodSeconds for the StatefulSet. | `{}` |
| `statefulSet.securityContext`               | Allow customizing fsGroup/runAsUser. | `{}` |
| `statefulSet.priorityClassName`             | Leverage a PriorityClass to ensure your pods survive resource shortages. | `{}` |
| `logLevel`                                  | Level to use for logging. Either debug, info, warn, or error.                                                                                                                                                                                                                                             | n/a     |
| `orgAllowlist`                              | Allowlist of repositories from which Atlantis will accept webhooks. **This value must be set for Atlantis to function correctly.** Accepts wildcard characters (`*`). Multiple values may be comma-separated.                                                                                             | none    |
| `orgWhitelist`                              | Deprecated (see orgAllowlist) List of repositories from which Atlantis will accept webhooks. Accepts wildcard characters (`*`). Multiple values may be comma-separated.                                                                                                                                   | none    |
| `config`                                    | Override atlantis main configuration by config map. It's allow some additional functionality like slack notifications.                                                                                                                                                                                | n/a     |
| `repoConfig`                                | [Server-side Repository Configuration](https://www.runatlantis.io/docs/server-side-repo-config.html) as a raw YAML string. Configuration is stored in ConfigMap.                                                                                                                                                | n/a     |
| `defaultTFVersion`                          | Default Terraform version to be used by atlantis server                                                                                                                                                                                                                                                   | n/a     |
| `allowForkPRs`                              | Allow atlantis to run on fork Pull Requests                                                                                                                                                                                                                                                               | `false` |
| `allowDraftPRs`                             | Allow atlantis to run on draft Pull Requests                                                                                                                                                                                                                                                              | `false` |
| `hidePrevPlanComments`                      | Allow atlantis to hide previous plan comments                                                                                                                                                                                                                                                             | `false` |
| `disableApply`                              | Disables running `atlantis apply` regardless of what options are specified                                                                                                                                                                                                                                 | `false` |
| `disableApplyAll`                           | Disables running `atlantis apply` without any flags                                                                                                                                                                                                                                                       | `false` |
| `disableRepoLocking`                        | Stops atlantis locking projects and or workspaces when running terraform                                                                                                                                                                                                                                  | `false` |
| `serviceAccount.create`                     | Whether to create a Kubernetes ServiceAccount if no account matching `serviceAccount.name` exists.                                                                                                                                                                                                        | `true`  |
| `serviceAccount.mount`                      | Whether to mount the Kubernetes ServiceAccount into the pod                                                                                                                                                                                                                                               | `true`  |
| `serviceAccount.name`                       | Name of the Kubernetes ServiceAccount under which Atlantis should run. If no value is specified and `serviceAccount.create` is `true`, Atlantis will be run under a ServiceAccount whose name is the FullName of the Helm chart's instance, else Atlantis will be run under the `default` ServiceAccount. | n/a     |
| `serviceAccount.annotations`                | Additional Service Account annotations                                                                           | n/a     |
| `serviceAccountSecrets.credentials`         | Deprecated (see googleServiceAccountSecrets) JSON string representing secrets for a Google Cloud Platform production service account. Only applicable if hosting Atlantis on GKE.                                                                                                                                                                      | n/a     |
| `serviceAccountSecrets.credentials-staging` | Deprecated (see googleServiceAccountSecrets) JSON string representing secrets for a Google Cloud Platform staging service account. Only applicable if hosting Atlantis on GKE.                                                                                                                                                                         | n/a     |
| `googleServiceAccountSecrets`               | An array of Kubernetes secrets containing Google Service Account credentials. See `values.yaml` for examples and additional documentation.                                                                                                                                                                | n/a     |
| `service.port`                              | Port of the `Service`.                                                                                                                                                                                                                                                                                    | `80`    |
| `service.targetPort`                        | Target Port of the `Service`.                                                                                                                                                                                                                                                                             | `4141`  |
| `service.loadBalancerSourceRanges`          | Array of allowlisted IP addresses for the Atlantis Service. If no value is specified, the Service will allow incoming traffic from all IP addresses (0.0.0.0/0).                                                                                                                                          | n/a     |
| `service.loadBalancerIP`                    | Expose this service on the given ip if service.type = `LoadBalancerIP`                                                                                                                           | n/a     |
| `storageClassName`                          | DEPRECATED - Storage class of the volume mounted for the Atlantis data directory.                                                                                                                                                                                                                         | n/a     |
| `tlsSecretName`                             | Name of a Secret for Atlantis' HTTPS certificate containing the following data items `tls.crt` with the public certificate and `tls.key` with the private key.                                                                                                                                            | n/a     |
| `ingress.enabled`                           | Whether to create a Kubernetes Ingress.                                                                                                                                                                                                                                                                   | `true`     |
| `ingress.annotations`                       | Additional annotations to use for the Ingress. | `{}` |
| `ingress.apiVersion`                        | Override ingress apiVersion. Useful in scenarios in which helm can't determine the capabilities of the Kubernetes cluster. | n/a |
| `ingress.labels`                            | Additional labels to use for the Ingress. | `{}` |
| `ingress.path`                              | Path to use in the `Ingress`. Should be set to `/*` if using gce-ingress in Google Cloud.                                                                                                                                                                                                                 | `/`     |
| `ingress.host`                              | Domain name Kubernetes Ingress rule looks for. Set it to the domain Atlantis will be hosted on.                                                                                                                                                                                                           |     |                                                                                                                                                                                                   | `/`     |
| `ingress.hosts[0].host`                     | List of domain names Kubernetes Ingress rule looks for. Set it to the domains in which Atlantis will be hosted on.                                                                                                                                                                                                           | `chart-example.local`     |
| `ingress.hosts[0].paths`                    | List of paths to use in Kubernetes Ingress rules.  Should be set to `/*` if using gce-ingress in Google                                                                                                                                                                                                        | `[/]`     |
| `ingress.tls`                               | Kubernetes tls block. See [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls) for details.                                                                                                                                                                            | `[]`     |
| `test.enabled`                              | Whether to enable the test. | `true` |
| `extraManifests`                            | Add additional manifests to deploy                      | `[]`                      |
| `initContainers`                            | Containers used to initialize context for Atlantis pods                                  | `[]`                              |
| `extraContainers`                           | Additionnal containers to use and depends of use cases. | `[]` |
| `hostAliases[].hostnames`                   | Hostnames for host alias entry                                  | n/a                              |
| `hostAliases[].ip`                          | IP for host alias entry                                  | n/a                               |
| `basicAuth.username`                        | Username for basic authentication                        | n/a                               |
| `basicAuth.password`                        | Password for basic authentication                        | n/a                               |
| `commonLabels`                        | Add Common Labels to all resources | `{}` |
| `containerSecurityContext.allowPrivilegeEscalation` | Whether to enable privilege escalation           | n/a                               |
| `containerSecurityContext.readOnlyRootFilesystem`   | Whether the root file system should be read-only | n/a                               |
| `customPem`   | SecretName of the custom `ca-certificates.cert` to override the `/etc/ssl/certs/ca-certificates.crt` with your custom one (self-signed certificates)<br>Secret has to be created manually and shal contain `ca-certificates.crt: PEM` | n/a                               |
| `api.secret`    | API secret to enable API endpoints                                                                        | n/a        |
| `apiSecretName` | Name of a pre-existing Kubernetes `Secret` containing a `apisecret` key. Use this instead of `api.secret` | n/a        |

**NOTE**: All the [Server Configurations](https://www.runatlantis.io/docs/server-configuration.html) are passed as [Environment Variables](https://www.runatlantis.io/docs/server-configuration.html#environment-variables).

## Upgrading

### From `4.0.*` to `4.1.*`
* The following value are deprecated:
  * `dataStorage`
  * `storageClassName`
* In favor of the new working way:
  * `volumeClaim.enabled`
  * `volumeClaim.dataStorage`
  * `volumeClaim.storageClassName`

### From `2.*` to `3.*`

* The following value names have been removed. They are replaced by [Server-side Repository Configuration](https://www.runatlantis.io/docs/server-side-repo-config.html)
  * `requireApproval`
  * `requireMergeable`
  * `allowRepoConfig`

To replicate your previous configuration, run Atlantis locally with your previous flags and Atlantis will print out the equivalent repo-config, for example:

```bash
$ atlantis server --allow-repo-config --require-approval --require-mergeable --gh-user=foo --gh-token=bar --repo-allowlist='*'
WARNING: Flags --require-approval, --require-mergeable and --allow-repo-config have been deprecated.
Create a --repo-config file with the following config instead:

---
repos:
- id: /.*/
  apply_requirements: [approved, mergeable]
  allowed_overrides: [apply_requirements, workflow]
  allow_custom_workflows: true

or use --repo-config-json='{"repos":[{"id":"/.*/", "apply_requirements":["approved", "mergeable"], "allowed_overrides":["apply_requirements","workflow"], "allow_custom_workflows":true}]}'
```

Then use this YAML in the new repoConfig value:

```yaml
repoConfig: |
  ---
  repos:
  - id: /.*/
    apply_requirements: [approved, mergeable]
    allowed_overrides: [apply_requirements, workflow]
    allow_custom_workflows: true
```

### From `1.*` to `2.*`
* The following value names have changed:
  * `allow_repo_config` => `allowRepoConfig`
  * `atlantis_data_storage` => `dataStorage` **NOTE: more than just a snake_case change**
  * `atlantis_data_storageClass` => `storageClassName` **NOTE: more than just a snake_case change**
  * `bitbucket.base_url` => `bitbucket.baseURL`


## Testing the Deployment
To perform a smoke test of the deployment (i.e. ensure that the Atlantis UI is up and running):

1. Install the chart.  Supply your own values file or use `test-values.yaml`, which has a minimal set of values required in order for Atlantis to start.

    ```bash
    helm repo add runatlantis https://runatlantis.github.io/helm-charts
    helm install -f test-values.yaml my-atlantis runatlantis/atlantis --debug
    ```

1. Run the tests:
    ```bash
    helm test my-atlantis
    ```
