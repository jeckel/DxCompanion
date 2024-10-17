import subprocess


def composer_updatable(path: str) -> dict[str, str]:
    with subprocess.Popen(
        ["composer", "update", "--dry-run"],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        output = process.stderr.read().strip()
        # Split the output into lines
        lines = output.strip().split("\n")
        packages: dict[str, str] = {}

        # Processing lines for packages
        for line in lines:
            if line.startswith("  - Upgrading"):
                # Extract package name and target version
                parts = line.split("(")
                package_name = line.strip().split(" ")[2]  # Get the package name
                version_info = (
                    parts[1].strip().rstrip(")")
                )  # Get the version info (v2.2.9 => v2.3.0)
                target_version = version_info.split("=>")[
                    -1
                ].strip()  # Get the target version

                # Append to the packages list as a dictionary
                packages[package_name] = target_version
        return packages
