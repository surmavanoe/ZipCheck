# ZipCheck

Vultr Agent Rush Hackathon — C2, Powering the Future of Work.

## Live demo

[Open ZipCheck](https://209.250.247.89/). Scan your own ZIP or try either built-in sample.

## Local demo

From this folder, run `python app.py` and open http://127.0.0.1:8000.
Try both sample buttons, then upload your own ZIP to recheck.

## Deploy on Vultr

1. Create a Shared CPU Cloud Compute instance with Ubuntu and your SSH public key. Enable a public IPv4 address.
2. Connect with SSH and install Python, its venv package, and Nginx.
3. Copy app.py and index.html onto the VM, or clone the public GitHub repo.
4. From the project directory, run:

```sh
python3 -m venv .venv
.venv/bin/pip install gunicorn
.venv/bin/gunicorn --bind 127.0.0.1:8000 app:application
```

5. Use systemd to keep that Gunicorn command running. Configure Nginx to proxy to http://127.0.0.1:8000 and set client_max_body_size to 8m. Allow HTTP/HTTPS through your Vultr firewall and configure HTTPS before using real archives.

## How Vultr powers the demo

The VM serves the interface and runs the Windows path checks on uploaded ZIP archives. ZipCheck reads the archive's directory without extracting files or keeping uploads. It checks common Windows naming problems. A clean scan only covers the implemented checks.
