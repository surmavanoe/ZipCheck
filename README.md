# ZipCheck

**Check a ZIP for Windows filename conflicts before you share it.**

[Try the live demo](https://209.250.247.89/)

An archive can contain both `Logo.png` and `logo.png`, even though the names can collide when someone extracts it into a typical Windows folder. ZipCheck flags paths like these and suggests how to fix them before you send the archive.

## What it checks

- Paths that may collide on Windows, including names that differ only in capitalization
- Reserved Windows names such as `AUX.txt`
- Unsupported characters and names ending in a dot or space
- Unsafe path components such as `..`

Select a ZIP up to 8 MiB and click **Check ZIP**. You can also try either built-in sample. The sample with issues returns three findings, and the clean sample returns zero.

## Run locally

With Python 3 installed, run `python app.py` from the repository root and open [localhost:8000](http://127.0.0.1:8000/).

## How it works

The live demo runs on a Vultr Ubuntu VM. Nginx handles HTTPS and forwards scan requests to the Python app running under Gunicorn. ZipCheck reads the archive’s file list without extracting its contents and returns flagged paths with suggested fixes. A clean result means the archive passed the checks listed above.

Built for **Vultr Agent Rush Hackathon · C2, Powering the Future of Work**.
