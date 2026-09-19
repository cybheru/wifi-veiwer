import subprocess

def get_wifi_profiles():
    """Return a list of saved Wi-Fi profile names."""

    try:
        result = subprocess.check_output(
            ["netsh","wlan","show","profiles"],
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        profiles =[]
        for line in result.splitlines():
            if "All User Profile" in line:
                name = line.split(":", 1)[1].strip()

                if name and name not in profiles:
                    profiles.append(name)

        return profiles
    except subprocess.CalledProcessError:
        return []

    except Exception as error:
        print(f"Error:{error}")
        return []

