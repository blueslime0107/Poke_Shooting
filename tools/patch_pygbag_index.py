import re
from pathlib import Path


INDEX_PATH = Path(__file__).resolve().parent.parent / "build" / "web" / "index.html"


def main() -> None:
    content = INDEX_PATH.read_text(encoding="utf-8")
    updated = content.replace(
        "https://pygame-web.github.io/cdn/0.9.3//browserfs.min.js",
        "https://cdn.jsdelivr.net/npm/browserfs/dist/browserfs.min.js",
    )

    archive_block_pattern = re.compile(
        r"    # unpack filesystem from compressed archive into work dir\\n"
        r"    if platform\\.window\\.location\\.host\\.find\\('\\.itch\\.zone'\\)>0:\\n"
        r"        import zipfile\\n"
        r"        async with platform\\.fopen\\(\"poke_shooting\\.apk\", \"rb\"\\) as archive:\\n"
        r"            with zipfile\\.ZipFile\\(archive\\) as zip_ref:\\n"
        r"                zip_ref\\.extractall\\(appdir\\.as_posix\\(\\)\\)\\n"
        r"    else:\\n"
        r"        import tarfile\\n"
        r"        async with platform\\.fopen\\(\"poke_shooting\\.tar\\.gz\", \"rb\"\\) as archive:\\n"
        r"            tar = tarfile\\.open\\(fileobj=archive, mode=\"r:gz\"\\)\\n"
        r"            tar\\.extractall\\(path=appdir\\.as_posix\\(\\), filter='tar'\\)\\n"
        r"            tar\\.close\\(\\)\\n"
    )

    archive_block_replacement = (
        "    # unpack filesystem from compressed archive into work dir\\n"
        "    async def extract_apk():\\n"
        "        import zipfile\\n"
        "        async with platform.fopen(\\\"poke_shooting.apk\\\", \\\"rb\\\") as archive:\\n"
        "            with zipfile.ZipFile(archive) as zip_ref:\\n"
        "                zip_ref.extractall(appdir.as_posix())\\n"
        "\\n"
        "    async def extract_targz():\\n"
        "        import tarfile\\n"
        "        async with platform.fopen(\\\"poke_shooting.tar.gz\\\", \\\"rb\\\") as archive:\\n"
        "            tar = tarfile.open(fileobj=archive, mode=\\\"r:gz\\\")\\n"
        "            tar.extractall(path=appdir.as_posix(), filter='tar')\\n"
        "            tar.close()\\n"
        "\\n"
        "    try:\\n"
        "        await extract_apk()\\n"
        "    except Exception as exc:\\n"
        "        print(f\\\"apk load failed, fallback to tar.gz: {exc}\\\")\\n"
        "        await extract_targz()\\n"
    )
    updated = archive_block_pattern.sub(archive_block_replacement, updated, count=1)

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