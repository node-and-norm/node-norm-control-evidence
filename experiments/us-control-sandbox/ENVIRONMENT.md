# Execution environment checkpoint

Initial inspection on 2 October 2026 found no Docker, Podman or Colima. The deprecated macOS sandbox-exec path was not used. Colima and Docker were subsequently installed and the restricted environment was verified as described below.

`python3 run_container.py --check` reports runtime readiness and exits 2 when unavailable. The launcher refuses an unisolated fallback. It accepts only a Python image pinned as `python@sha256:<64 hex characters>`. The image digest is now pinned and exercised; see the verified checkpoint below.

Once Docker is available and an appropriate image is verified, invoke the launcher with `--image` and a unique `--run-name`. Restrictions exercised at the recorded checkpoint: no container networking, read-only root filesystem and study source mount, dropped capabilities, no new privileges, non-root host user, resource limits, temporary storage, and a writable run-specific output mount. Only the research-sandbox directory is mounted as source; no home, credentials, source workspace or Docker socket is mounted. The launcher records its command, pinned image, output and exit code.

The launcher has argument/guard tests and a completed restriction probe for the recorded configuration. Repeat effective-configuration verification when the environment changes. A container shares its host kernel and is not a sufficient boundary for arbitrary adversarial code. The current application is authored deterministic code only.

Reference for container settings: https://docs.docker.com/reference/cli/docker/container/run/ . Runtime documentation and enforcement must be verified on the execution host before protocol freeze.

Remaining environment gates: separate outcome/evidence access for any blinded study; assurance for any future adversarial or model-generated code; repeat verification after configuration changes. U.S. application context and formal regulatory participation are separate from execution geography.


## Verified environment, 2 October 2026

Installed through Homebrew: Colima 0.9.1, Docker client 29.2.1, Lima 2.0.3. Profile/context: `node-norm-research` / `colima-node-norm-research`. Linux arm64 VM: 2 CPUs, 2 GiB memory, 10 GiB data disk plus the default 20 GiB root disk (virtual capacities). No login startup service was enabled; the default Docker context was not activated or replaced.

The VM mounts the study folder writable and Colima's own download cache read-only. The container mounts the study folder read-only and one run folder writable. No user home or credentials are exposed to the container. The VM itself can download images; the evaluated container's network is disabled.

Official Python image, resolved from `python:3.12-slim`, pinned for execution:

`python@sha256:dddfd7e07f9d15aeeca61529320492139d21cac7f0070c00609243e51e4e0016`

Observed container Python 3.12.15 and SQLite 3.46.1. Server Docker 28.4.0. Full engine/kernel versions are preserved under `isolation-runs/isolation-001/runtime-versions.json`.

Eight effective-configuration checks and ten runtime probes passed. The probes observed blocked root/source writes, non-root identity, loopback-only networking and unreachable external network, zero effective capabilities, no-new-privileges, and cgroup CPU/memory/process bounds. Writing the probe result established access to the allowed output mount. These checks do not establish general escape resistance.

The nine-case container rehearsal matched the earlier local outcomes exactly at the JSON level. Twelve verification tests also passed inside the same pinned image and restrictions. Records: `isolation-runs/isolation-001/`, `container-runs/isolated-001/`, and `container-runs/isolated-tests-001/`.

To resume after the VM is stopped:

```sh
colima start node-norm-research --activate=false --ssh-config=false
python3 run_container.py --check --context colima-node-norm-research
python3 run_container.py --context colima-node-norm-research --image python@sha256:dddfd7e07f9d15aeeca61529320492139d21cac7f0070c00609243e51e4e0016 --run-name isolated-002
```

Use a new run name each time. The study's full research-sandbox directory is available read-only in this development container, including public expected outcomes. This is not an assessor-blinding boundary. Separate packaging and access control are required before any blinded study.

## Retry/restart checkpoint

Seven additional fixtures ran under the same image and restrictions in `container-runs/recovery-001`. All eight semantic JSON records matched `runs/recovery-001`; both manifests verified twenty-one artifacts. Nineteen tests passed in `container-runs/isolated-tests-002`.

Select `--suite recovery` for these fixtures or `--suite tests` for verification; the default `--suite basic` retains the original nine-case behavior. Always choose a new run name. Worker processes restart inside the container; this does not restart the container or VM and does not simulate power loss. Restriction settings were unchanged by the suite selector.
