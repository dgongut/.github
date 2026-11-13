"""Builds a Docker Hub description from a project's README.

The README is the only source. Two markers, invisible on GitHub, adapt it:

    <!-- dockerhub:skip -->
    Only on GitHub (cloning the repo, local development...)
    <!-- /dockerhub:skip -->

    <!-- dockerhub:only
    Only on Docker Hub (a link to GitHub, notes about tags...)
    -->

Besides that, it rewrites what Docker Hub does not render: GitHub alerts
(> [!NOTE]) and in-page anchors (#section), which become links to the
README on GitHub. Relative links are completed by the publishing action.

Usage: python3 dockerhub_readme.py README.md DOCKERHUB.md https://github.com/owner/repo [es|en]
"""

import re
import sys
from pathlib import Path

# Docker Hub rejects descriptions longer than this
MAX_BYTES = 25000

ALERTS = {
    "es": {
        "NOTE": "ℹ️ **Nota**",
        "TIP": "💡 **Consejo**",
        "IMPORTANT": "❗ **Importante**",
        "WARNING": "⚠️ **Atención**",
        "CAUTION": "🛑 **Cuidado**",
    },
    "en": {
        "NOTE": "ℹ️ **Note**",
        "TIP": "💡 **Tip**",
        "IMPORTANT": "❗ **Important**",
        "WARNING": "⚠️ **Warning**",
        "CAUTION": "🛑 **Caution**",
    },
}


def build(text: str, repo_url: str, lang: str = "es") -> str:
    alerts = ALERTS.get(lang, ALERTS["en"])
    text = re.sub(r"<!-- dockerhub:skip -->.*?<!-- /dockerhub:skip -->\n?", "", text, flags=re.S)
    text = re.sub(r"<!-- dockerhub:only\n?(.*?)-->", r"\1", text, flags=re.S)
    text = re.sub(
        r"^> \[!(\w+)\]\s*$",
        lambda m: "> " + alerts.get(m.group(1).upper(), f"**{m.group(1).title()}**"),
        text,
        flags=re.M,
    )
    text = re.sub(r"\]\(#", f"]({repo_url}#", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def main() -> None:
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    src, dst, repo_url = sys.argv[1:4]
    lang = sys.argv[4] if len(sys.argv) > 4 else "es"
    out = build(Path(src).read_text(encoding="utf-8"), repo_url.rstrip("/"), lang)
    size = len(out.encode("utf-8"))
    if size > MAX_BYTES:
        sys.exit(f"{dst}: {size} bytes, Docker Hub allows {MAX_BYTES}. Mark more of {src} with dockerhub:skip.")
    Path(dst).write_text(out, encoding="utf-8")
    print(f"{dst}: {size}/{MAX_BYTES} bytes")


if __name__ == "__main__":
    main()
