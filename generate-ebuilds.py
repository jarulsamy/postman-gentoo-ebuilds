from pprint import pprint
import requests
from pathlib import Path


def generate_ebuild(item, output_dir=Path("./dist")):
    output_dir.mkdir(exist_ok=True)
    template = r"""
EAPI=8

DESCRIPTION="All-in-one API platform for building and working with APIs."
HOMEPAGE="https://www.postman.com"
SRC_URI="{src_url} -> postman.tar.gz"

LICENSE=""
SLOT="0"
KEYWORDS="amd64"
IUSE=""

DEPEND=""
RDEPEND="${{DEPEND}}"
BDEPEND=""

S="${{WORKDIR}}/Postman"

src_compile() {{
    # Create a .desktop entry
    cat <<-EOF > "${{S}}/postman.desktop"
[Desktop Entry]
Type=Application
Name=Postman
Comment=${{DESCRIPTION}}
Exec=postman
Icon=postman
Terminal=false
Categories=Development
EOF
}}

src_install() {{
    insopts -p
    insinto opt/Postman
    doins -r app
    insopts

    exeinto usr/bin
    newexe - <<-EOF postman
#!/usr/bin/env bash
exec /opt/Postman/app/postman "\$@"
EOF

    # Icon
    insopts -m644
    insinto usr/share/icons/hicolor/128x128/apps
    newins app/icons/icon_128x128.png postman.png

    # Desktop file
    insinto usr/share/applications
    doins postman.desktop
}}
"""

    vers = item["name"]
    if "-" in vers:
        # Skip canary/beta builds
        return

    for i in item["assets"]:
        if "linux" in i["name"] and "x64" in i["name"]:
            src_url = i["url"]
            break
    else:
        print(f"Failed to find amd64 vers for {vers}")
        return

    output_path = output_dir / f"postman-{vers}.ebuild"
    contents = template.format(src_url=src_url)
    output_path.write_text(contents)


if __name__ == "__main__":
    ENDPOINT = "https://dl.pstmn.io/changelog"
    resp = requests.get(ENDPOINT)

    postman_versions = resp.json()["changelog"]
    for i in postman_versions:
        generate_ebuild(i)
