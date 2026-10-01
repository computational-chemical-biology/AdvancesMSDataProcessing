"""JupyterHub configuration for the Advances in MS Data Processing course.

Launches one Docker container per user (DockerSpawner) on the shared
`jupyterhub-net` network. Each user gets their own named volume for `/home/jovyan`,
a read-only view of the Jupyter Book notebooks (`jupyterhub-notebooks/`) and a
writable per-user copy seeded into `/home/jovyan/work` (see entrypoint.sh).

Values that vary per deployment (image tags, limits, notebook path) are read
from environment variables so docker-compose.yml stays the single place to tweak.
"""
import os

c = get_config()


# ---------------------------------------------------------------------------
# Users & authentication
# ---------------------------------------------------------------------------
# NativeAuthenticator: signup page, admin-managed accounts.
# Keep `open_signup` ON during the enrollment period, then turn it OFF so that
# only existing accounts can log in (the hub is behind a public hostname).
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"
c.NativeAuthenticator.open_signup = True
c.NativeAuthenticator.admin_users = {"admin"}
c.NativeAuthenticator.minimum_password_length = 6
# Anyone who authenticates can use the hub (course server).
c.Authenticator.allow_all = True

# ---------------------------------------------------------------------------
# Spawning: one Docker container per user
# ---------------------------------------------------------------------------
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

c.DockerSpawner.network_name = "jupyterhub-net"
c.DockerSpawner.remove = True
# Seeding entrypoint: mirrors the read-only course-notebooks into a writable
# /home/jovyan/work per user, then starts the server (see entrypoint.sh).
c.DockerSpawner.cmd = ["bash", "/usr/local/bin/seed-entrypoint.sh"]
# The slim image's WORKDIR is /work, but course notebooks + user volumes live
# under /home/jovyan -> single-user server root is the user's home so the file
# browser shows `course-notebooks/` and `work/`.
c.DockerSpawner.notebook_dir = "/home/jovyan"

# THIS HOSTS' Docker 19.03 default seccomp profile blocks Node 18 / Python
# worker-thread creation (uv_thread_create/clone) -> run user containers
# seccomp-unconfined, same as the hub itself (see docker-compose.yml).
c.DockerSpawner.extra_host_config = {"security_opt": ["seccomp=unconfined"]}

SLIM_IMG = os.environ.get("SPAWN_IMAGE_SLIM", "ams-data-slim:latest")
FULL_IMG = os.environ.get("SPAWN_IMAGE_FULL", "ams-data-processing:latest")
c.DockerSpawner.image = SLIM_IMG
c.DockerSpawner.allowed_images = {
    "General course (light)": SLIM_IMG,
    "Full stack (PyTorch / TensorFlow)": FULL_IMG,
}

# Per-user resources. Raise SPAWN_MEM_LIMIT (e.g. to 6G) when running the
# heavy torch/tensorflow lessons; the "Full stack" image needs ~2-3 GB just to
# import those libraries.
c.DockerSpawner.mem_limit = os.environ.get("SPAWN_MEM_LIMIT", "2G")
c.DockerSpawner.cpu_limit = float(os.environ.get("SPAWN_CPU_LIMIT", "1"))

# Each user keeps their work in a persistent named volume; the course notebooks
# are shared read-only; the seed entrypoint is mounted read-only too.
c.DockerSpawner.volumes = {
    "jupyterhub-user-{username}": {"bind": "/home/jovyan", "mode": "rw"},
    os.environ.get("COURSE_NOTEBOOKS_DIR", "/home/rsilva/AdvancesMSDataProcessing/jupyterhub-notebooks"):
        {"bind": "/home/jovyan/course-notebooks", "mode": "ro"},
    "/home/rsilva/AdvancesMSDataProcessing/jupyterhub/entrypoint.sh":
        {"bind": "/usr/local/bin/seed-entrypoint.sh", "mode": "ro"},
}

# ---------------------------------------------------------------------------
# Hub server
# ---------------------------------------------------------------------------
c.JupyterHub.ip = "0.0.0.0"
c.JupyterHub.port = 8000
# User containers must reach the hub over the shared docker network, not
# 127.0.0.1:8081: point them at the hub container name on `jupyterhub-net`.
# The hub's internal API stays on port 8081 but is bound on all interfaces.
c.JupyterHub.hub_bind_url = "http://0.0.0.0:8081/"
c.DockerSpawner.hub_ip_connect = "jupyterhub"
# Modern equivalent of hub_ip_connect: tells the hub how to reach user servers
# (and how the hub itself appears on the docker network), so spawned single-user
# servers get a real ip. Without it, "The 'ip' trait of a Server instance
# expected a unicode string, not the NoneType None" on spawn.
c.JupyterHub.hub_connect_ip = "jupyterhub"
# The read-only course-notebooks mount is fine for reading, but many notebooks
# (git clone, pip install -e ...) write next to themselves. Open the lab on the
# writable per-user copy seeded into /home/jovyan/work.
c.Spawner.default_url = "/lab/tree/work"
c.Spawner.http_timeout = 120
c.Spawner.start_timeout = 300