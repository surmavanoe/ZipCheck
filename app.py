import io
import json
import re
import zipfile
from pathlib import Path
from wsgiref.simple_server import make_server

MAX_BYTES = 8 * 1024 * 1024
RESERVED = re.compile(r"(?:CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])", re.I)
PAGE = Path(__file__).with_name("index.html").read_bytes()


def inspect_zip(data):
    issues = []
    seen = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        for entry in entries:
            path = entry.orig_filename
            parts = path.replace(chr(92), "/").rstrip("/").split("/")
            for index, part in enumerate(parts, 1):
                prefix = "/".join(parts[:index])
                if not part or part in (".", ".."):
                    issues.append(("Unsafe path", path, "Rebuild the ZIP with relative file paths."))
                    break
                if RESERVED.fullmatch(part.split(".")[0].rstrip(" ")):
                    issues.append(("Reserved name", prefix, "Rename this item before rebuilding the ZIP."))
                if part.endswith((".", " ")):
                    issues.append(("Trailing dot or space", prefix, "Remove the trailing dot or space."))
                if any(c in '<>:"|?*' or ord(c) < 32 for c in part):
                    issues.append(("Invalid Windows character", prefix, "Remove the unsupported character."))
                key = "/".join(piece.rstrip(". ").upper() for piece in parts[:index])
                kind = "folder" if index < len(parts) or entry.is_dir() else "file"
                previous = seen.setdefault(key, (prefix, kind))
                if previous != (prefix, kind):
                    issues.append(("Potential Windows path collision", f"{previous[0]} ({previous[1]}) ↔ {prefix} ({kind})", "Give the two items distinct names."))
    return {"entries": len(entries), "issues": list(dict.fromkeys(issues))}


def application(environ, start_response):
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]
    status = "200 OK"
    content_type = "application/json"
    if method == "GET" and path == "/":
        payload = PAGE
        content_type = "text/html; charset=utf-8"
    elif method == "POST" and path == "/scan":
        try:
            size = int(environ.get("CONTENT_LENGTH") or 0)
            if not 0 < size <= MAX_BYTES:
                status = "400 Bad Request"
                result = {"error": "Choose a ZIP file up to 8 MiB."}
            else:
                result = inspect_zip(environ["wsgi.input"].read(size))
        except (zipfile.BadZipFile, ValueError, UnicodeError, NotImplementedError):
            status = "400 Bad Request"
            result = {"error": "This file could not be read as a ZIP archive."}
        payload = json.dumps(result).encode()
    else:
        status = "404 Not Found"
        payload = b'{"error":"Page not found"}'
    start_response(status, [("Content-Type", content_type), ("Content-Length", str(len(payload))), ("Cache-Control", "no-store")])
    return [payload]


if __name__ == "__main__":
    with make_server("127.0.0.1", 8000, application) as server:
        print("ZipCheck is running at http://127.0.0.1:8000")
        server.serve_forever()

