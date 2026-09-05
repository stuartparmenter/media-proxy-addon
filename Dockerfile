ARG BUILD_FROM

# The add-on consumes the same portable binary as standalone Linux users.
FROM alpine:3.24 AS fetch
ARG APP_REPO
ARG APP_REF
ARG BUILD_ARCH
RUN apk add --no-cache curl
WORKDIR /download
RUN case "$BUILD_ARCH" in \
      amd64) target=x86_64-unknown-linux-musl ;; \
      aarch64) target=aarch64-unknown-linux-musl ;; \
      *) echo "Unsupported architecture: $BUILD_ARCH" >&2; exit 1 ;; \
    esac \
 && version="${APP_REF#v}" \
 && asset="media-proxy-${version}-${target}.tar.gz" \
 && base="${APP_REPO}/releases/download/${APP_REF}" \
 && curl --fail --location --retry 3 -o "$asset" "$base/$asset" \
 && curl --fail --location --retry 3 -o "$asset.sha256" "$base/$asset.sha256" \
 && sha256sum -c "$asset.sha256" \
 && tar -xzf "$asset" media-proxy LICENSE THIRD_PARTY_LICENSES.md

FROM $BUILD_FROM AS runtime
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 \
    PATH="/opt/venv/bin:${PATH}" \
    DENO_DIR=/data/deno XDG_CACHE_HOME=/data/cache

# Stay on the base's stable Alpine release; no edge repository mixing.
RUN apk add --no-cache python3 py3-pip ffmpeg deno ca-certificates \
      libdrm libva libva-utils mesa-va-gallium \
 && if [ "$(uname -m)" = "x86_64" ]; then apk add --no-cache intel-media-driver; fi

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install -r /tmp/requirements.txt \
 && /opt/venv/bin/pip check \
 && python3 -c 'import yt_dlp, yt_dlp_ejs' \
 && deno --version \
 && python3 -c 'import subprocess; v=subprocess.check_output(["deno", "--version"], text=True).split()[1]; assert tuple(map(int, v.split("."))) >= (2, 6, 6), v' \
 && yt-dlp --version \
 && ffmpeg -version \
 && ffprobe -version

COPY --from=fetch /download/media-proxy /usr/local/bin/media-proxy
COPY --from=fetch /download/LICENSE /download/THIRD_PARTY_LICENSES.md /usr/share/licenses/media-proxy/
RUN media-proxy --version
COPY run.py /run.py
CMD ["python3", "/run.py"]
