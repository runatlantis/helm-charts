# Trusting additional CA certificates

Behind a TLS-inspecting proxy or when talking to services signed by a private CA, Atlantis and the tools it runs (`terraform`, `git`, `curl`, Python `requests`-based tools) fail with `x509: certificate signed by unknown authority`.

The `customPem` value *replaces* `/etc/ssl/certs/ca-certificates.crt` in the container, which drops every public CA shipped in the image. To keep the public CAs and **append** your own, build a merged bundle in an init container and point the trust environment variables at it. This works as the default non-root user and needs no `update-ca-certificates`, `runAsUser: 0` or `hostPath`.

First create a Secret holding your CA certificate(s) as PEM files with a `.crt` suffix:

```sh
kubectl create secret generic atlantis-custom-ca --namespace atlantis --from-file=corp-ca.crt=./corp-ca.crt
```

Then add the following to your values. The init container uses the Atlantis image so the public CAs always match the version you run; keep its tag in line with `image.tag` (or `appVersion`):

```yaml
extraVolumes:
  - name: custom-ca-certs
    secret:
      secretName: atlantis-custom-ca
  - name: ca-bundle
    emptyDir: {}

extraVolumeMounts:
  - name: ca-bundle
    mountPath: /etc/ssl/custom
    readOnly: true

initContainers:
  - name: build-ca-bundle
    image: ghcr.io/runatlantis/atlantis:v0.49.0
    command:
      - sh
      - -c
      - |
        cp /etc/ssl/certs/ca-certificates.crt /ca-bundle/ca-certificates.crt
        for f in /custom-ca/*.crt; do
          echo >> /ca-bundle/ca-certificates.crt
          cat "$f" >> /ca-bundle/ca-certificates.crt
        done
    volumeMounts:
      - name: custom-ca-certs
        mountPath: /custom-ca
        readOnly: true
      - name: ca-bundle
        mountPath: /ca-bundle
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: [ALL]

environment:
  # Go (atlantis, terraform), OpenSSL and the Python standard library
  SSL_CERT_FILE: /etc/ssl/custom/ca-certificates.crt
  # git
  GIT_SSL_CAINFO: /etc/ssl/custom/ca-certificates.crt
  # curl and wget
  CURL_CA_BUNDLE: /etc/ssl/custom/ca-certificates.crt
  # Python requests (e.g. checkov, az)
  REQUESTS_CA_BUNDLE: /etc/ssl/custom/ca-certificates.crt
```

Notes:

- Set further trust variables in `environment` for any other runtime in a custom image; point them at the same `/etc/ssl/custom/ca-certificates.crt` file.
- Certificates without a trailing newline are fine: the script inserts one before each file.
- The bundle is rebuilt each time the pod starts, so rotating the Secret takes effect on the next restart.
- If your `initContainers` already contain entries, append this one to your list.
