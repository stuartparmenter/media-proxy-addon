# must be first so FROM can use it
ARG BUILD_FROM

# ----- Stage 1: fetch the app from the repo -----
FROM alpine/git:2.45.2 AS fetch
ARG APP_REPO
ARG APP_REF

RUN git clone --depth 1 --branch "${APP_REF}" "${APP_REPO}" /src

# ----- Stage 2: Home Assistant base runtime (Alpine/musl) -----
FROM $BUILD_FROM AS runtime
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# Runtime deps
# Runtime deps (+ HW decode support for Intel iGPU on x86 platforms)
RUN apk add --no-cache \
      python3 \
      py3-pip \
      ffmpeg \
      libdrm \
      libva \
      libva-utils \
      mesa-va-gallium \
      lcms2 \
      libjpeg-turbo \
      libwebp \
      tiff \
      zlib \
 && if [ "$(uname -m)" = "x86_64" ] || [ "$(uname -m)" = "i386" ]; then \
      apk add --no-cache intel-media-driver; \
    fi

WORKDIR /app

# Copy entire repo from stage 1 (includes pyproject.toml)
COPY --from=fetch /src/ /app/

# Build-only deps for wheels + create venv + pip install into venv, then clean
RUN apk add --no-cache --virtual .build-deps \
      build-base python3-dev linux-headers ffmpeg-dev pkgconf zlib-dev \
 && python3 -m venv /opt/venv \
 && . /opt/venv/bin/activate \
 && pip install --upgrade pip \
 && pip install /app \
 && apk del .build-deps

# Use the venv's python/pip by default
ENV PATH="/opt/venv/bin:${PATH}"

# Launcher
COPY run.py /run.py
CMD ["python3", "/run.py"]
