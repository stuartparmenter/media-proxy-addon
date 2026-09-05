# Home Assistant Add-on: Media Proxy

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

_WebSocket-controlled media proxy that outputs DDP (UDP)_

## About

Stream videos, GIFs, still images, and YouTube content to tiny LED/LCD displays (e.g., ESPHome devices using DDP) with smart resizing, optional color-range expansion, and packet pacing.

This Home Assistant add-on provides a WebSocket control API and pushes pixel data over UDP using the DDP format, designed to work with ESPHome devices and other LED/LCD displays.

## Documentation

For complete documentation, configuration options, API reference, and usage examples, see the main repository:

**📖 [Full Documentation](https://github.com/pavlov-net/media-proxy)**

## Installation

This add-on is part of the Stuart Parmenter Home Assistant Add-ons repository. To install:

1. Add the repository URL to your Home Assistant instance:
   [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.][add-repo-shield]][add-repo]

2. Search for the "Media Proxy" add-on and click it.
3. Click on the "INSTALL" button.

## Quick Start

1. Start the add-on
2. The WebSocket control API will be available at `ws://your-ha-ip:8788/control`
3. Use the API to stream content to your LED/LCD displays
4. See the [main documentation](https://github.com/pavlov-net/media-proxy) for API details and ESPHome integration examples

## Custom Configuration

The addon reads configuration files from `/addon_configs/2b3c960e_media_proxy/` on your Home Assistant host. To create and edit these files:

1. Install the **File Editor** addon from the Home Assistant addon store (found under Official add-ons)
2. Go to the File Editor addon configuration
3. Turn off **"Enforce Basepath"** to allow navigation outside the `/homeassistant` directory
4. Navigate to `/addon_configs/2b3c960e_media_proxy/`
5. Create a `config.yaml` file in this directory with your custom configuration

For configuration file format and options, see: [Configuration Documentation](https://github.com/pavlov-net/media-proxy?tab=readme-ov-file#configuration)

Alternatively, you can access these files directly if you have SSH access to your Home Assistant host.

## ESPHome Integration

For ESPHome device integration examples, see: [ddp-esphome](https://github.com/pavlov-net/ddp-esphome)

## Support

[GitHub Issues](https://github.com/pavlov-net/media-proxy/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[add-repo-shield]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[add-repo]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fstuartparmenter%2Fhomeassistant-addons
## Rust release migration

The add-on installs the standalone Rust release for its architecture, verifies
its SHA-256 checksum, and provides FFmpeg/ffprobe, yt-dlp with its bundled EJS
solver, and Deno. No Rust compiler or media-proxy Python package is installed in
the runtime. Alpine 3.24 supplies Deno on both amd64 and aarch64 without using edge
repositories. yt-dlp is pinned in `requirements.txt` and updated through dependency PRs.

Existing `host`, `port`, and `log_level` options, the add-on slug, host networking,
and `/config/config.yaml` location are retained. Existing display clients keep
using `/control` and DDP. Home Assistant entity/template drawing was intentionally
removed in the Rust core; source URLs using that feature need to be replaced.

Before upgrading, take a Home Assistant backup including the add-on and record
its current image version. Test a still image, an animation, a video, YouTube,
stop/start, and a client reconnect on the actual display. Restore that backup if
you need to return to Python; the add-on does not migrate or rewrite your config.

Maintainers: this branch targets core `v1.0.0`. Merge/release the core compatibility
and binary-packaging changes first, verify both release assets exist, then require
both add-on architecture builds and `tests/smoke_container.py` before publishing.
Repository dispatch opens a dependency PR; it no longer enables automatic merging.

For the first migration, leave the core repository variable
`ADDON_RELEASE_DISPATCH_ENABLED` unset until this add-on migration is merged;
otherwise the old add-on workflow could auto-merge a Rust version into the
Python image build. Enable it afterward for future dependency PRs.

Use a new add-on version and tag matching `config.yaml` (for example `v0.5.12`),
publish that release with the **prerelease** checkbox enabled, and wait for both
versioned images before promoting the release to stable. The add-on catalog has
an independent daily updater that discovers stable releases, so a stable release
must already have both images available. Prerelease builds do not update the
`latest` image tag or dispatch the catalog updater.
