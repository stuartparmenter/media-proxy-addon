# Media Proxy for Home Assistant

This add-on runs [Media Proxy](https://github.com/pavlov-net/media-proxy) to stream
images and video to displays over DDP. It installs the architecture-specific
release binary, FFmpeg/ffprobe, yt-dlp with EJS, and Deno. Supported architectures
are listed in [config.yaml](config.yaml).

## Installation

1. Add `https://github.com/stuartparmenter/homeassistant-addons` to the Home Assistant
   add-on store's repositories.
2. Install **Media Proxy**, configure its host/port/log-level options, and start it.
3. Connect a display through the [control API](https://github.com/pavlov-net/media-proxy/blob/main/docs/api.md).
   For ESPHome integration, see [ddp-esphome](https://github.com/pavlov-net/ddp-esphome).

## Configuration

The launcher reads Home Assistant options from `/data/options.json` and passes
them to the server. It also loads `/config/config.yaml` when present.

On the Home Assistant host, that file is
`/addon_configs/2b3c960e_media_proxy/config.yaml`. Edit it through SSH or a file editor
with access to the add-on configuration directory. See the core
[configuration reference](https://github.com/pavlov-net/media-proxy/blob/main/docs/configuration.md)
for settings. The add-on does not rewrite this file.

## Publish a version

[build.yaml](build.yaml) pins the core release and base images;
[requirements.txt](requirements.txt) pins yt-dlp and its default extras. Core archives
must exist before the add-on image builds. Both architecture checks must pass.

Use a tag matching the unpublished version in `config.yaml`. Publish it as a
prerelease, wait for both versioned images and runtime checks, then test an upgrade
on Home Assistant with a display. Take an add-on backup before testing; verify
playback, reconnect, shutdown and backup restore. Promote the same release to
stable after validation.

The catalog updater independently discovers stable releases, so both images must
exist before promotion. The release workflow publishes `latest` and dispatches
`update` to `stuartparmenter/homeassistant-addons` after both architectures pass.
Prereleases do neither.

Core release notifications require the core repository variable
`ADDON_RELEASE_DISPATCH_ENABLED=true`. They open dependency PRs for review.

## Support and license

Report issues in [Media Proxy](https://github.com/pavlov-net/media-proxy/issues).
See [LICENSE](LICENSE) for the MIT license.
