# Home Assistant Add-on: Media Proxy

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

_WebSocket-controlled media proxy that outputs DDP (UDP)_

## About

Stream videos, GIFs, still images, and YouTube content to tiny LED/LCD displays (e.g., ESPHome devices using DDP) with smart resizing, optional color-range expansion, and packet pacing.

This Home Assistant add-on provides a WebSocket control API and pushes pixel data over UDP using the DDP format, designed to work with ESPHome devices and other LED/LCD displays.

## Documentation

For complete documentation, configuration options, API reference, and usage examples, see the main repository:

**📖 [Full Documentation](https://github.com/stuartparmenter/media-proxy)**

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
4. See the [main documentation](https://github.com/stuartparmenter/media-proxy) for API details and ESPHome integration examples

## ESPHome Integration

For ESPHome device integration examples, see: [lvgl-ddp-stream](https://github.com/stuartparmenter/lvgl-ddp-stream)

## Support

[GitHub Issues](https://github.com/stuartparmenter/media-proxy/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[add-repo-shield]: https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg
[add-repo]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fstuartparmenter%2Fhomeassistant-addons