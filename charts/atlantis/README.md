# Atlantis

[Atlantis](https://www.runatlantis.io/) is a tool for safe collaboration on [Terraform](https://www.terraform.io/) repositories.

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| lkysow |  |  |
| jamengual |  |  |
| chenrui333 |  |  |
| nitrocode |  |  |
| genpage |  |  |
| gmartinez-sisti |  |  |

## Links

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Required Configuration](#required-configuration)
- [Additional manifests](#additional-manifests)
- [Values](#values)
- [Upgrading](#upgrading)
  - [From `4.*` to `5.*`](#from-4-to-5)
  - [From `2.*` to `3.*`](#from-2-to-3)
  - [From `1.*` to `2.*`](#from-1-to-2)
- [Testing the Deployment](#testing-the-deployment)
- [Update documentation](#update-documentation)
- [Run unit tests](#run-unit-tests)

## Introduction

This chart creates a single pod in a StatefulSet running Atlantis. Atlantis persists Terraform [plan files](https://www.terraform.io/docs/commands/plan.html) and [lockfiles](https://www.terraform.io/docs/state/locking.html) to disk for the duration of a Pull/Merge Request. These files are stored in a PersistentVolumeClaim to survive Pod failures.

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
      name: ".Release.Name-test"
    spec:
      securityPolicy:
        name: "gcp-cloud-armor-policy-test"
```

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| allowDraftPRs | bool | `false` | Enables atlantis to run on a draft Pull Requests. |
| allowForkPRs | bool | `false` | Enables atlantis to run on a fork Pull Requests. |
| api | object | `{}` | Optionally specify an API secret to enable the API. Check values.yaml for examples. |
| apiSecretName | string | `""` | If managing secrets outside the chart for the API secret, use this variable to reference the secret name. |
| atlantisDataDirectory | string | `"/atlantis-data"` | Path to the data directory for the volumeMount. |
| atlantisUrl | string | `""` | An option to override the atlantis url, if not using an ingress, set it to the external IP. Check values.yaml for examples. |
| aws | object | `{}` | To specify AWS credentials to be mapped to ~/.aws or to aws.directory. Check values.yaml for examples. |
| awsSecretName | string | `""` | To reference an already existing Secret object with AWS credentials |
| azuredevops | object | `{}` | If using Azure DevOps, please enter your values as follows. The chart will perform the base64 encoding for you for values that are stored in secrets. Check values.yaml for examples. |
| basicAuth | object | `{"password":"","username":""}` | Optionally specify an username and a password for basic authentication. |
| basicAuthSecretName | string | `""` | If managing secrets outside the chart for the Basic Auth secret, use this variable to reference the secret name. |
| bitbucket | object | `{}` | If using Bitbucket, there are two approaches: Bitbucket Server, deployed in your own infrastructure and Cloud available at (https://Bitbucket.org). The chart will perform the base64 encoding for you for values that are stored in secrets. Check values.yaml for examples. |
| command | list | `[]` | Override the command field of the Atlantis container. |
| commonLabels | object | `{}` | Common Labels for all resources created by this chart. |
| config | string | `""` | Override atlantis main configuration by config map, ref: https://www.runatlantis.io/docs/using-slack-hooks.html#configuring-atlantis. Check values.yaml for examples. |
| containerSecurityContext | object | `{}` | Check values.yaml for examples. |
| customPem | string | `""` | Allows to override the /etc/ssl/certs/ca-certificates.cer with your custom one. You have to create a secret with the specified name. |
| dataStorage | string | `""` | DEPRECATED - Disk space available to check out repositories. Example: 5Gi. |
| defaultTFVersion | string | `""` | Sets the default terraform version to be used in atlantis server. Check values.yaml for examples. |
| disableApply | bool | `false` | Disables running `atlantis apply` regardless of which flags are sent with it. |
| disableApplyAll | bool | `false` | Disables running `atlantis apply` without any flags. |
| disableRepoLocking | bool | `false` | Stops atlantis locking projects and or workspaces when running terraform. |
| enableDiffMarkdownFormat | bool | `false` | Use Diff Markdown Format for color coding diffs. |
| enableKubernetesBackend | bool | `false` | Optionally deploy rbac to allow for the serviceAccount to manage terraform state via the kubernetes backend. |
| environment | object | `{}` | Environtment values to add to the Atlantis pod. Check values.yaml for examples. |
| environmentRaw | list | `[]` | Optionally specify additional environment variables in raw yaml format. Useful to specify variables refering to k8s objects. Check values.yaml for examples. |
| environmentSecrets | list | `[]` | Optionally specify additional environment variables to be populated from Kubernetes secrets. Useful for passing in TF_VAR_foo or other secret environment variables from Kubernetes secrets. Check values.yaml for examples. |
| extraAnnotations | object | `{}` |  |
| extraArgs | list | `[]` | Optionally specify extra arguments for the Atlantis pod. Check values.yaml for examples. |
| extraContainers | list | `[]` | Optionally specify extra containers for the Atlantis pod. Check values.yaml for examples. |
| extraManifests | list | `[]` | Optionally specify additional manifests to be created. Check values.yaml for examples. |
| extraVolumeMounts | list | `[]` | Optionally specify additional volume mounts for the container. Check values.yaml for examples. |
| extraVolumes | list | `[]` | Optionally specify additional volumes for the pod. Check values.yaml for examples. |
| fullnameOverride | string | `""` | Provide a name to substitute for the full names of resources. |
| gitconfig | string | `""` | When referencing Terraform modules in private repositories, it may be helpful (necessary?) to use redirection in a .gitconfig. Check values.yaml for examples. |
| gitconfigSecretName | string | `""` | If managing secrets outside the chart for the gitconfig, use this variable to reference the secret name |
| github | object | `{}` | If using GitHub, please enter your values as follows. The chart will perform the base64 encoding for values that are stored in secrets. The 'hostname' key is exclusive to GitHub Enterprise installations. Check values.yaml for examples. |
| githubApp | object | `{}` | If using a GitHub App, please enter your values as follows. The chart will perform the base64 encoding for you for values that are stored in secrets. Check values.yaml for examples. |
| gitlab | object | `{}` | If using GitLab, please enter your values as follows. The 'hostname' key is exclusive to GitLab Enterprise installations. The chart will perform the base64 encoding for you for values that are stored in secrets. Check values.yaml for examples. |
| googleServiceAccountSecrets | list | `[]` | Optionally specify google service account credentials as Kubernetes secrets. If you are using the terraform google provider you can specify the credentials as "${file("/var/secrets/some-secret-name/key.json")}". Check values.yaml for examples. |
| hidePrevPlanComments | bool | `false` | Enables atlantis to hide previous plan comments. |
| hideUnchangedPlanComments | bool | `false` | Enables atlantis to hide no-changes plan comments from the pull request. |
| hostAliases | list | `[]` | Optionally specify hostAliases for the Atlantis pod. Check values.yaml for examples. |
| hostNetwork | bool | `false` |  |
| image.pullPolicy | string | `"Always"` |  |
| image.repository | string | `"ghcr.io/runatlantis/atlantis"` |  |
| image.tag | string | `""` | If not set appVersion field from Chart.yaml is used |
| imagePullSecrets | list | `[]` | Optionally specify an array of imagePullSecrets. Secrets must be manually created in the namespace. ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/. Check values.yaml for examples. |
| ingress.annotations | object | `{}` | Check values.yaml for examples. |
| ingress.apiVersion | string | `""` |  |
| ingress.enabled | bool | `true` |  |
| ingress.host | string | `""` |  |
| ingress.hosts | list | `[]` | Used when several hosts are required. Check values.yaml for examples. |
| ingress.ingressClassName | string | `nil` |  |
| ingress.labels | object | `{}` |  |
| ingress.path | string | `"/*"` | Use / for nginx. |
| ingress.pathType | string | `"ImplementationSpecific"` |  |
| ingress.paths | list | `[]` | Used when several paths under the same host, with different backend services, are required. Check values.yaml for examples. |
| ingress.tls | list | `[]` | Check values.yaml for examples. |
| initConfig.enabled | bool | `false` | Install providers/plugins into a path shared with the Atlantis pod. |
| initConfig.image | string | `"alpine:latest"` |  |
| initConfig.imagePullPolicy | string | `"IfNotPresent"` |  |
| initConfig.script | string | Check values.yaml. | Script to run on the init container. |
| initConfig.securityContext | object | `{}` | Security context for the container. |
| initConfig.sharedDir | string | `"/plugins"` | SharedDir is set as env var INIT_SHARED_DIR. |
| initConfig.sharedDirReadOnly | bool | `true` |  |
| initConfig.sizeLimit | string | `"100Mi"` | Size for the shared volume. |
| initConfig.workDir | string | `"/tmp"` |  |
| initContainers | list | `[]` | Optionally specify init containers manifests to be added to the Atlantis pod. Check values.yaml for examples. |
| lifecycle | object | `{}` | Set lifecycle hooks. https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/. |
| livenessProbe.enabled | bool | `true` |  |
| livenessProbe.failureThreshold | int | `5` |  |
| livenessProbe.initialDelaySeconds | int | `5` |  |
| livenessProbe.periodSeconds | int | `60` | We only need to check every 60s since Atlantis is not a high-throughput service. |
| livenessProbe.scheme | string | `"HTTP"` |  |
| livenessProbe.successThreshold | int | `1` |  |
| livenessProbe.timeoutSeconds | int | `5` |  |
| loadEnvFromConfigMaps | list | `[]` | Optionally specify additional Kubernetes ConfigMaps to load environment variables from. All key-value pairs within these ConfigMaps will be set as environment variables. Note that any variables set here will be ignored if also defined in the env block of the atlantis statefulset. For example, providing ATLANTIS_ALLOW_FORK_PRS here and defining a value for allowForkPRs will result in the allowForkPRs value being used. Check values.yaml for examples. |
| loadEnvFromSecrets | list | `[]` | Optionally specify additional Kubernetes secrets to load environment variables from. All key-value pairs within these secrets will be set as environment variables. Note that any variables set here will be ignored if also defined in the env block of the atlantis statefulset. For example, providing ATLANTIS_GH_USER here and defining a value for github.user will result in the github.user value being used. Check values.yaml for examples. |
| lockingDbType | string | `""` | Set the desired Locking DB type Accepts boltdb or redis. |
| logLevel | string | `""` | Specify the log level for Atlantis. Accepts: debug, info, warn, or error. |
| nameOverride | string | `""` | Provide a name to substitute for the name of the chart. |
| netrc | string | `""` | When referencing Terraform modules in private repositories or registries (such as Artfactory) configuing a .netrc file for authentication may be required. Check values.yaml for examples. |
| netrcSecretName | string | `""` | If managing secrets outside the chart for the netrc file, use this variable to reference the secret name |
| nodeSelector | object | `{}` |  |
| orgAllowlist | string | `"<replace-me>"` | Replace this with your own repo allowlist. |
| orgWhitelist | string | `"<deprecated>"` | Deprecated in favor of orgAllowlist. |
| podMonitor | object | `{"enabled":false,"interval":"30s"}` | Enable this if you're using Google Managed Prometheus. |
| podTemplate.annotations | object | `{}` | Check values.yaml for examples. |
| podTemplate.labels | object | `{}` |  |
| readinessProbe.enabled | bool | `true` |  |
| readinessProbe.failureThreshold | int | `5` |  |
| readinessProbe.initialDelaySeconds | int | `5` |  |
| readinessProbe.periodSeconds | int | `60` |  |
| readinessProbe.scheme | string | `"HTTP"` |  |
| readinessProbe.successThreshold | int | `1` |  |
| readinessProbe.timeoutSeconds | int | `5` |  |
| redis | object | `{}` | Configure Redis Locking DB. lockingDbType value must be redis for the config to take effect. Check values.yaml for examples. |
| redisSecretName | string | `""` | When managing secrets outside the chart for the Redis secret, use this variable to reference the secret name. |
| replicaCount | int | `1` | Replica count for Atlantis pods. |
| repoConfig | string | `""` | Use Server Side Repo Config, ref: https://www.runatlantis.io/docs/server-side-repo-config.html. Check values.yaml for examples. |
| resources | object | `{}` | Resources for Atlantis. Check values.yaml for examples. |
| service.annotations | object | `{}` |  |
| service.loadBalancerIP | string | `nil` |  |
| service.loadBalancerSourceRanges | list | `[]` |  |
| service.nodePort | string | `nil` |  |
| service.port | int | `80` |  |
| service.targetPort | int | `4141` |  |
| service.type | string | `"NodePort"` |  |
| serviceAccount.annotations | object | `{}` | Annotations for the Service Account. Check values.yaml for examples. |
| serviceAccount.create | bool | `true` | Specifies whether a ServiceAccount should be created. |
| serviceAccount.mount | bool | `true` | If false, no kubernetes service account token will be mounted to the pod. |
| serviceAccount.name | string | `nil` | The name of the ServiceAccount to use. If not set and create is true, a name is generated using the fullname template. |
| serviceAccountSecrets | object | `{}` | To keep backwards compatibility only. Deprecated (see googleServiceAccountSecrets). To be used for mounting credential files (when using google provider). Check values.yaml for examples. |
| servicemonitor.additionalLabels | object | `{}` | Prometheus ServiceMonitor labels. |
| servicemonitor.auth.basicAuth | object | `{"enabled":false}` | If auth is enabled on Atlantis, use one of the following mechanism. |
| servicemonitor.auth.basicAuth.enabled | bool | `false` | Authentication from the secret generated with the basicAuth values   this will reference the username and password keys   from the atlantis-basic-auth secret. |
| servicemonitor.auth.externalSecret.enabled | bool | `false` | Authentication based on an external secret |
| servicemonitor.auth.externalSecret.keys | object | `{}` | Check values.yaml for examples. |
| servicemonitor.auth.externalSecret.name | string | `""` |  |
| servicemonitor.enabled | bool | `false` | To enable a Prometheus servicemonitor, set enabled to true,   and enable the metrics in this file's repoConfig   by setting a value for metrics.prometheus.endpoint. |
| servicemonitor.interval | string | `"30s"` |  |
| servicemonitor.path | string | `"/metrics"` |  |
| statefulSet.annotations | object | `{}` |  |
| statefulSet.labels | object | `{}` |  |
| statefulSet.priorityClassName | string | `""` |  |
| statefulSet.securityContext.fsGroup | int | `1000` |  |
| statefulSet.securityContext.fsGroupChangePolicy | string | `"OnRootMismatch"` |  |
| statefulSet.securityContext.runAsUser | int | `100` | It is not recommended to run atlantis as root. |
| statefulSet.shareProcessNamespace | bool | `false` | Option to share process namespace with atlantis container. |
| statefulSet.updateStrategy | object | `{}` |  |
| storageClassName | string | `""` | DEPRECATED - Storage class name for Atlantis disk. |
| terminationGracePeriodSeconds | int | default depends on the kubernetes version. | Optionally customize the termination grace period in seconds. |
| test.annotations | object | `{}` |  |
| test.enabled | bool | `true` | Enables test container. |
| test.image | string | `"bats/bats"` |  |
| test.imageTag | string | `"1.9.0"` |  |
| tlsSecretName | string | `""` | TLS Secret Name for Atlantis pod. |
| tolerations | list | `[]` |  |
| topologySpreadConstraints | list | `[]` | You can use topology spread constraints to control how Pods are spread across your cluster among failure-domains such as regions, zones, nodes, and other user-defined topology domains. (requires Kubernetes >= 1.19). Check values.yaml for examples. |
| vcsSecretName | string | `""` | If managing secrets outside the chart for the webhook, use this variable to reference the secret name |
| volumeClaim.accessModes[0] | string | `"ReadWriteOnce"` |  |
| volumeClaim.dataStorage | string | `"5Gi"` | Disk space available to check out repositories. |
| volumeClaim.enabled | bool | `true` |  |
| volumeClaim.storageClassName | string | `""` | Storage class name (if possible, use a resizable one). |
| webhook_ingress.annotations | object | `{}` | Check values.yaml for examples. |
| webhook_ingress.apiVersion | string | `""` |  |
| webhook_ingress.enabled | bool | `false` | When true creates a secondary webhook. |
| webhook_ingress.host | string | `""` |  |
| webhook_ingress.hosts | list | `[]` | Used when several hosts are required. Check values.yaml for examples. |
| webhook_ingress.ingressClassName | string | `nil` |  |
| webhook_ingress.labels | object | `{}` |  |
| webhook_ingress.path | string | `"/*"` | Use / for nginx. |
| webhook_ingress.pathType | string | `"ImplementationSpecific"` |  |
| webhook_ingress.paths | list | `[]` | Used when several paths under the same host, with different backend services, are required. Check values.yaml for examples. |
| webhook_ingress.tls | list | `[]` | TLS configuration. Check values.yaml for examples. |

## Upgrading

### From `4.*` to `5.*`

A breaking change was merged on [#304](https://github.com/runatlantis/helm-charts/pull/304).
This change moves the atlantis data volume to a separate PVC to allow changing the volume size without removing the statefulset.
Unmistakingly, this change only bumped the minor version, released as `4.22.0`, instead of incrementing the major version. The release `5.0.0` addresses this issue. Please find the required upgrade manual steps below.

#### Upgrade steps

Trying to upgrade the release directly will return the following error:

> Error: UPGRADE FAILED: cannot patch "atlantis" with kind StatefulSet: StatefulSet.apps "atlantis" is invalid: spec: Forbidden: updates to statefulset spec for fields other than 'replicas', 'ordinals', 'template', 'updateStrategy', 'persistentVolumeClaimRetentionPolicy' and 'minReadySeconds' are forbidden

To allow the upgrade to proceed, first we need to remove the statefulset controller, copy all the data from the old volume to the new one and then cleanup.

NOTE: These steps will ensure no data is lost, however during the copy process the atlantis server is unavailable and any webhooks sent to atlantis during that window are missed and won't be processed.

Upgrade steps:

1. For atlantis deployments managed by GitOps solutions such as ArgoCD, disabling the automatic synchronization is required

1. Create a temporary helm configuration file named `migration-4-to-5.yaml`, the configuration includes the required settings to allow the atlantis data to be copied to the new volume before the atlantis server is started. The suggested configuration implies that the default command for atlantis has not been customized. If required, adjust the `persistentVolumeClaim.claimName` value.

    ```yaml
    command:
      - sh
      - -c
      - 'cp -Rv /atlantis-data-old/* "${ATLANTIS_DATA_DIR}" && exec /usr/local/bin/docker-entrypoint.sh server'

    extraVolumes:
      - name: atlantis-data-old
        persistentVolumeClaim:
          claimName: atlantis-data-atlantis-0

    extraVolumeMounts:
      - name: atlantis-data-old
        mountPath: /atlantis-data-old
    ```

1. Delete the current statefulset without removing the atlantis pod. This can be achieved with the parameter [--cascade=orphan](https://kubernetes.io/docs/tasks/administer-cluster/use-cascading-deletion/#set-orphan-deletion-policy):

    NOTE: If required, adjust the namespace and the statefulset name.

    ```sh
    kubectl delete statefulsets.apps atlantis --namespace atlantis --cascade=orphan
    ```

1. Deploy the new atlantis version, this will recreate the statefulset and update the atlantis pod acordingly. E.g.:

    ```sh
    helm upgrade -i atlantis runatlantis/atlantis --version 5.0.0 -f my-config.yaml -f migration-4-to-5.yaml
    ```

1. Check the logs for the atlantis pod, it should show the copy process followed by start of the atlantis server. E.g.:

    ```json
    '/atlantis-data-old/atlantis.db' -> '/atlantis-data/atlantis.db'
    '/atlantis-data-old/bin' -> '/atlantis-data/bin'
    '/atlantis-data-old/existing-data.example' -> '/atlantis-data/existing-data.example'
    '/atlantis-data-old/plugin-cache' -> '/atlantis-data/plugin-cache'
    No files found in /docker-entrypoint.d/, skipping
    {"level":"info","ts":"2024-05-01T17:17:03.406Z","caller":"server/server.go:447","msg":"Utilizing BoltDB","json":{}}
    {"level":"info","ts":"2024-05-01T17:17:03.411Z","caller":"policy/conftest_client.go:153","msg":"failed to get default conftest version. Will attempt request scoped lazy loads DEFAULT_CONFTEST_VERSION not set","json":{}}
    {"level":"info","ts":"2024-05-01T17:17:03.413Z","caller":"server/server.go:985","msg":"Atlantis started - listening on port 4141","json":{}}
    {"level":"info","ts":"2024-05-01T17:17:03.413Z","caller":"scheduled/executor_service.go:51","msg":"Scheduled Executor Service started","json":{}}
    ```

1. Run a second deployment without the extra configuration file. E.g.:

    ```sh
    helm upgrade -i atlantis runatlantis/atlantis --version 5.0.0 -f my-config.yaml
    ```

1. Remove the old `persistentVolumeClaim`:

    ```sh
    kubectl delete persistentvolumeclaims atlantis-data-atlantis-0 --namespace atlantis
    ```

1. For atlantis deployments managed by GitOps solutions such as ArgoCD, the automatic synchronization can now be enabled

### From `4.0.*` to `4.1.*`

- The following value are deprecated:
  - `dataStorage`
  - `storageClassName`

- In favor of the new working way:
  - `volumeClaim.enabled`
  - `volumeClaim.dataStorage`
  - `volumeClaim.storageClassName`

### From `2.*` to `3.*`

- The following value names have been removed. They are replaced by [Server-side Repository Configuration](https://www.runatlantis.io/docs/server-side-repo-config.html)
  - `requireApproval`
  - `requireMergeable`
  - `allowRepoConfig`

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

- The following value names have changed:
  - `allow_repo_config` => `allowRepoConfig`
  - `atlantis_data_storage` => `dataStorage` **NOTE: more than just a snake_case change**
  - `atlantis_data_storageClass` => `storageClassName` **NOTE: more than just a snake_case change**
  - `bitbucket.base_url` => `bitbucket.baseURL`

## Testing the Deployment

To perform a smoke test of the deployment (i.e. ensure that the Atlantis UI is up and running):

1. Install the chart. Supply your own values file or use `test-values.yaml`, which has a minimal set of values required in order for Atlantis to start.

    ```bash
    helm repo add runatlantis https://runatlantis.github.io/helm-charts
    helm install -f test-values.yaml my-atlantis runatlantis/atlantis --debug
    ```

1. Run the tests:

    ```bash
    helm test my-atlantis
    ```

## Update documentation

Documentation is auto-generated using [helm-docs](https://github.com/norwoodj/helm-docs).

To update run the following (from the root path of the repository):

1. If required, update `charts/atlantis/README.md.gotmpl`
2. Run `make docs`

## Run unit tests

From the root of the repository, run:

```sh
make unit-test-run-atlantis
```

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.13.1](https://github.com/norwoodj/helm-docs/releases/v1.13.1)
