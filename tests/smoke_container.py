#!/usr/bin/env python3
"""Run after building/loading the add-on image; no Supervisor is required."""
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request


def check(image):
    subprocess.run(['docker', 'run', '--rm', '--entrypoint', '/bin/sh', image, '-ec',
                    'media-proxy --version; ffmpeg -version; ffprobe -version; '
                    'yt-dlp --version; python3 -c "import yt_dlp_ejs"; '
                    'deno eval "if (1 + 1 !== 2) Deno.exit(1)"'], check=True)
    with tempfile.TemporaryDirectory(prefix='addon-smoke-') as directory:
        root = Path(directory)
        data, config = root / 'data', root / 'config'
        data.mkdir()
        config.mkdir()
        with socket.socket() as reserve:
            reserve.bind(('127.0.0.1', 0))
            port = reserve.getsockname()[1]
        (data / 'options.json').write_text(json.dumps(dict(host='127.0.0.1', port=port, log_level='INFO')))
        original = 'youtube:\n  60fps: false\nlog:\n  level: INFO\n'
        (config / 'config.yaml').write_text(original)
        container = subprocess.check_output([
            'docker', 'run', '-d', '--network', 'host',
            '-v', f'{data}:/data', '-v', f'{config}:/config', image], text=True).strip()
        try:
            for _ in range(100):
                try:
                    with urllib.request.urlopen(f'http://127.0.0.1:{port}/api/system/health', timeout=1) as response:
                        assert json.load(response)['status'] == 'ok'
                    break
                except (OSError, urllib.error.URLError):
                    time.sleep(0.1)
            else:
                raise AssertionError('add-on failed to start')
            logs = subprocess.check_output(['docker', 'logs', container], stderr=subprocess.STDOUT, text=True)
            assert 'resolver: yt-dlp subprocess' in logs, logs
            assert (config / 'config.yaml').read_text() == original
            subprocess.run(['docker', 'stop', '--time', '10', container], check=True)
            state = json.loads(subprocess.check_output(['docker', 'inspect', container], text=True))[0]['State']
            assert state['ExitCode'] == 0, state
            print('PASS: bundled runtime, legacy options/config, local resolver detection, SIGTERM')
        finally:
            subprocess.run(['docker', 'logs', container], check=False)
            subprocess.run(['docker', 'rm', '-f', container], check=False)


if __name__ == '__main__':
    check(sys.argv[1])
