# Multi-user JupyterHub (up to ~50 students)

The `docker compose up` from the README runs a **single shared JupyterLab** — fine for
one person, wrong for a class. For ~50 students this repository also ships a
**JupyterHub** deployment that gives every student their **own Docker container and
notebook server** behind a login page, served at <https://seriema.fcfrp.usp.br>.

- Students log in, get an isolated server, and **never see each other's work**.
- The heavy ML stack (`torch`/`tensorflow`, chemprop, AlphaPept, fermo-core, ms2deepscore)
  is only chosen on demand, so most users run a **light image**.
- The course notebooks are mounted **read-only** (students copy them into their home).

## Architecture

```
students  ─▶ nginx-proxy (443, Let's Encrypt)  seriema.fcfrp.usp.br
                │  nginx-net
                ▼
          jupyterhub (hub, port 8000, docker.sock)
                │  jupyterhub-net
                ▼
   one container per student:  /home/jovyan   <- named volume "jupyterhub-user-<user>"
                               /home/jovyan/course-notebooks  <- host course dir (read-only)
```

Two images are used:

| image                          | contents                                  | usual RAM |
|--------------------------------|-------------------------------------------|-----------|
| `ams-data-slim:latest`         | Jupyter + numpy/pandas/sklearn/matchms/pyOpenMS/RDKit/omicverse/scanpy…  | ~0.5 GB idle, ≤2 GB busy |
| `ams-data-processing:latest`   | everything above + torch/tf, chemprop, AlphaPept, fermo-core, …          | 2–3 GB just to import tf/torch |

At spawn time each user chooses one of the two via a small form.

## Starting

```bash
# 1) images must exist:
#    ams-data-processing:latest   (built earlier, see README / Dockerfile)
#    ams-data-slim:latest         (see "Building the images")
#    jupyterhub-hub:latest        (see "Building the images")

# 2) the reverse proxy network must exist (nginx-proxy already runs on it)
docker network inspect nginx-net >/dev/null || docker network create nginx-net

# 3) the spawner network must exist (compose treats it as external so the name
#    is used verbatim by DockerSpawner). It already exists on seriema; otherwise:
docker network create jupyterhub-net

# 4) start the hub (and the legacy single-user lab if wanted)
docker compose up -d jupyterhub
docker compose logs -f jupyterhub
```

> On **seriema** the Docker Compose plugin is not installed; use the v1 wrapper
> instead: `docker-compose up -d jupyterhub` (identical behaviour).

The hub exposes only on `jupyterhub-net` + `nginx-net`; **no host port is published**,
so traffic must go through nginx-proxy → `https://seriema.fcfrp.usp.br`.
To reach the hub directly for debugging, run it once with a published port:

```bash
docker run --rm -p 8000:8000 --security-opt seccomp=unconfined \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PWD/jupyterhub/jupyterhub_config.py":/etc/jupyterhub/jupyterhub_config.py:ro \
  -v jupyterhub_data:/srv/jupyterhub \
  --network jupyterhub-net \
  jupyterhub-hub:latest
```

If the hub cannot find the `jupyterhub-net` network, create it first:
`docker network create jupyterhub-net`.

## Accounts (NativeAuthenticator)

`jupyterhub_config.py` uses **NativeAuthenticator**:

- During **enrollment**, signup is open: students open the hub and create
  `username + password` themselves.
- The built-in admin is **`admin`**. After the first signup of `admin` you can log in
  and manage users from the *Admin* page (`/hub/admin`).
- **After the course enrolment closes, disable public signup** by setting in
  `jupyterhub/jupyterhub_config.py`:
  ```python
  c.NativeAuthenticator.open_signup = False
  ```
  then `docker compose restart jupyterhub`.
- Alternative auth (quick throwaway, e.g. behind a firewall only): switch
  `c.JupyterHub.authenticator_class` to `"dummy"`.

## Resources and ~50 students

The host (`seriema`) has ~49 GB usable and other services running alongside.
Budget:

- Light image: ~1-2 GB peak per active student → **~20-25 concurrent, computing
  students fit comfortably**.
- Heavy image (`torch`/`tensorflow` import alone is 2-3 GB): **only a handful**.
  Keep `SPAWN_MEM_LIMIT=2G` for the light profile, and raise it (e.g.
  `SPAWN_MEM_LIMIT=6G` in `docker-compose.yml`) only while running the heavy lessons.
- A class of 50 rarely has all 50 computing at once; if they do, bump the host RAM
  or run the heavy lessons on Colab (every notebook has an "Open in Colab" badge).

Per-user limits are set in `docker-compose.yml`:
```
SPAWN_MEM_LIMIT=2G     # per-user RAM cap
SPAWN_CPU_LIMIT=1      # per-user CPU cap
```

## User data

- Every student's home is a **named Docker volume** `jupyterhub-user-<username>`,
  persistent across container restarts.
- Students only see the **Jupyter Book index** (`_toc.yml`). The shared
  `course-notebooks/` mount is generated from that index into
  `jupyterhub-notebooks/` (real copies, ~16 MB) and bind-mounted **read-only**. It
  contains exactly the notebooks listed in the book — no Dockerfiles, requirements
  files, `.env` or hub configuration leak into student containers.
  Re-sync it whenever the book changes:
  ```bash
  python3 jupyterhub/sync_notebooks.py
  ```
  (then restart/re-create each running student server to remount).
- Hub state (database, cookie secret) lives in the `jupyterhub_data` volume
  (`/srv/jupyterhub`).

## Admin day-to-day

```bash
docker compose logs -f jupyterhub        # hub log
docker ps --filter network=jupyterhub-net   # who is running a server right now
docker kill <container>                  # stop a stuck user server
docker start <container>                 # start it again
docker exec jupyterhub jupyterhub token admin   # admin API token
```

## Building the images

On a normal Docker host, plain `docker build` works:

```bash
docker build -t ams-data-processing .            # full stack
docker build -f Dockerfile.slim -t ams-data-slim:latest .
docker build -f jupyterhub/Dockerfile.hub -t jupyterhub-hub:latest .
```

**On `seriema`** (old Docker 19.03, strict seccomp breaks `dpkg` during builds), build
with the run-and-commit workaround:

```bash
# full image (see README): install apt deps + requirements-lock.txt
# slim image:
docker run --name slim-build --security-opt seccomp=unconfined \
  -v "$PWD":/repo python:3.11-slim sh -c '
    export DEBIAN_FRONTEND=noninteractive
    rm -f /etc/apt/apt.conf.d/docker-clean
    apt-get update && apt-get install -y --no-install-recommends \
      build-essential curl fonts-dejavu libxrender1 libxext6 libx11-6 libxt6 \
      libgl1 libglib2.0-0 git wget && rm -rf /var/lib/apt/lists/*
    pip install --no-cache-dir -r /repo/requirements-slim-lock.txt'
# (wait for ALL_STEPS_OK, then:)
# user + notebook-deps enrichment on top of the lock (keeps numpy-1-era ABI):
docker run --name slim-extras --security-opt seccomp=unconfined \
  -v "$PWD":/repo ams-data-slim:latest sh -c '
    useradd -m -u 1000 -s /bin/bash jovyan
    chown -R jovyan:jovyan /home/jovyan
    pip install --no-cache-dir --constraint /repo/constraints-slim.txt \
      -r /repo/requirements-notebooks.txt
    pip install --no-cache-dir --constraint /repo/constraints-slim.txt chemprop==1.6.1'
# then commit BOTH runs with the metadata below; keep extra images untagged:
#   docker commit --change 'WORKDIR /work' \
#     --change 'ENV DEBIAN_FRONTEND=noninteractive JUPYTER_ENABLE_LAB=yes MLFLOW_SKIP_IP_CHECK=1' \
#     --change 'EXPOSE 8888' slim-XXX ams-data-slim:latest
docker commit --change 'WORKDIR /work' \
  --change 'ENV DEBIAN_FRONTEND=noninteractive JUPYTER_ENABLE_LAB=yes MLFLOW_SKIP_IP_CHECK=1' \
  --change 'EXPOSE 8888' slim-build ams-data-slim:latest

# hub (control plane) image:
docker run --name hub-build --security-opt seccomp=unconfined \
  jupyterhub/jupyterhub:5.0 sh -c \
  'pip install --no-cache-dir dockerspawner jupyterhub-nativeauthenticator' \
  # wait for HUB install to finish, then:
docker commit --change 'CMD ["jupyterhub","-f","/etc/jupyterhub/jupyterhub_config.py"]' \
  hub-build jupyterhub-hub:latest
```

## Security notes

- The hub is reachable at a public hostname. NativeAuthenticator signup is open during
  enrollment — **disable it afterwards** (see Accounts).
- Passwords are hashed; home volumes are isolated per user.
- Since the Oct-2026 hardening, spawned kernels run as the shared non-root user
  `jovyan` (uid 1000): `jupyterhub/entrypoint.sh` seeds the writable `work/` copy,
  chowns the volume without descending into the read-only `course-notebooks` mount,
  forces `HOME=/home/jovyan` (runuser preserves the container env, so without this
  singleuser would try to write `/root/.local`), caps `OPENBLAS_NUM_THREADS`, and
  drops privileges via `runuser -u jovyan --preserve-environment`.
- The course mount is read-only to limit damage; `jupyterhub-notebooks/` regenerated
  with `jupyterhub/sync_notebooks.py`.
- Keep `nginx-proxy` / `nginx-proxy-le` up-to-date; they terminate TLS for this hub.
- Deps policy: the slim image's kernel holds all book imports EXCEPT `fermo-core`
  (it forces `matchms 0.24` → `numba<0.58`/`numpy<1.25`, breaking the modern slim
  stack; run the FERMO notebook in the full image, whose env is locked to that older
  set). `requirements-notebooks.txt` + `constraints-slim.txt` document the extras.

## Host quirks (seriema, Docker 19.03) baked into the setup

- **Seccomp breaks worker threads.** The default Docker 19.03 seccomp profile makes
  Node 18's `uv_thread_create` (and some Python thread-pool code) abort with
  `Assertion ... failed` / `can't start new thread`. Both the hub
  (`security_opt: [seccomp=unconfined]` in `docker-compose.yml`) and every user
  container (`extra_host_config.security_opt` in `jupyterhub_config.py`) therefore run
  seccomp-unconfined. Without this the hub's proxy crashes at boot.
- **Hub↔user API address.** User containers reach the hub API at
  `http://jupyterhub:8081/hub/api`, not `127.0.0.1:8081`. This is set via
  `c.DockerSpawner.hub_ip_connect = "jupyterhub"` and
  `c.JupyterHub.hub_bind_url = "http://0.0.0.0:8081/"` in `jupyterhub_config.py`.
  Do not push `hub_port` to 8000 or the hub tries to double-bind port 8000
  (`OSError: [Errno 98] Address already in use`).