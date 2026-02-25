import requests
import configparser
from packaging import version

LATEST_CFG_URL = "https://github.com/more-abc/more_abc/raw/master/settings.cfg"

LOCAL_CFG_PATH = "./settings.cfg"

REPO_URL = "https://github.com/more-abc/more_abc"


def _get_version_from_cfg(content):
    """Parse the version number from the CFG content (adapt to the `version` field in the `[version]` section)."""
    cfg = configparser.ConfigParser()
    cfg.read_string(content)
    try:
        return cfg.get("Version", "version").strip() 
    except (configparser.NoSectionError, configparser.NoOptionError):
        print("[Version] section or version field not found in the settings.cfg file.")
        return None
    
def _get_latest_version():
    """Read the `settings.cfg` file from the remote repository to obtain the latest version number."""
    try:
        resp = requests.get(LATEST_CFG_URL, timeout=5)
        resp.raise_for_status()
        return _get_version_from_cfg(resp.text)
    except Exception as e:
        print(f"Failed to get remote settings.cfg: {e}")
        return None

def _get_local_version():
    """Read the version number from the local settings.cfg file"""
    try:
        with open(LOCAL_CFG_PATH, "r", encoding="utf-8") as f:
            return _get_version_from_cfg(f.read())
    except FileNotFoundError:
        print("The local settings.cfg file does not exist")
        return None
    except Exception as e:
        print(f"Failed to read local version.cfg: {e}")
        return None
    
def _check_mod_version():
    """Check the mod version and push the announcement"""
    latest_ver = _get_latest_version()
    local_ver = _get_local_version()

    if not latest_ver or not local_ver:
        return
    
    if version.parse(latest_ver) > version.parse(local_ver):
        print(f"§ notice § The version {local_ver} of more_abc you are currently downloading is not the latest version!")
