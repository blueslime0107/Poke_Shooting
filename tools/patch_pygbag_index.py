from pathlib import Path


INDEX_PATH = Path(__file__).resolve().parent.parent / "build" / "web" / "index.html"


def main() -> None:
    content = INDEX_PATH.read_text(encoding="utf-8")
    updated = content.replace(
        "https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js",
        "https://pygame-web.github.io/cdn/0.9.3/browserfs.min.js",
    )
    updated = updated.replace('                allowfullscreen="true"\n', "")
    updated = updated.replace('                webkitallowfullscreen="true"\n', "")
    updated = updated.replace('                msallowfullscreen="true"\n', "")
    updated = updated.replace('                mozallowfullscreen="true"\n', "")
    updated = updated.replace(
        '                allow="autoplay; fullscreen *; geolocation; microphone; camera; midi; monetization; xr-spatial-tracking; gamepad; gyroscope; accelerometer; xr; cross-origin-isolated"',
        '                allow="autoplay; fullscreen *; geolocation; microphone; camera; midi; gamepad; gyroscope; accelerometer; cross-origin-isolated"',
    )

    if updated != content:
        INDEX_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()