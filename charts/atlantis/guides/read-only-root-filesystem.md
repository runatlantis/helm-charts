# Enabling a read-only root filesystem

`readOnlyRootFilesystem` is **not** on by default, because Atlantis writes to its home directory at runtime: `~/.git-credentials` is written on startup when `--write-git-creds` is set and rewritten by the GitHub App token rotator on every token rotation, and `git config --global` writes `~/.gitconfig`.

The chart already handles this for you. Setting the flag is enough -- the StatefulSet then mounts `emptyDir` volumes at `/home/atlantis` and `/tmp` automatically, so you do not need to add any `extraVolumes` of your own:

```yaml
containerSecurityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  seccompProfile:
    type: RuntimeDefault
```

Test it against your own setup before rolling it out: custom workflows, Terraform providers and plugin caches may need writable paths beyond the home directory and `/tmp`.
