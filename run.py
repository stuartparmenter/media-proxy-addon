# © Copyright 2025 Stuart Parmenter
# SPDX-License-Identifier: MIT

import json
import os
from pathlib import Path
import shlex

OPTIONS = Path("/data/options.json")
CONFIG = Path("/config/config.yaml")
SERVER = "/usr/local/bin/media-proxy"


def main():
    try:
        with OPTIONS.open(encoding="utf-8") as handle:
            options = json.load(handle)
    except (OSError, ValueError) as error:
        print(f"[addon] options load error: {error}", flush=True)
        options = {}

    cmd = [SERVER, "--host", str(options.get("host", "0.0.0.0")),
           "--port", str(int(options.get("port", 8788))),
           "--log-level", str(options.get("log_level", "INFO")).lower()]
    if CONFIG.exists():
        cmd += ["--config", str(CONFIG)]

    print("[addon] exec:", shlex.join(cmd), flush=True)
    # Replace the launcher so Supervisor's SIGTERM reaches media-proxy directly.
    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    main()
