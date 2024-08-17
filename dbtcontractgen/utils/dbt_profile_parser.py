from pathlib import Path
from typing import Any

import yaml


def load_dbt_profiles(profiles_path: Path) -> dict[str, Any]:
    """Load the dbt profiles.yaml file.

    :param profiles_path: The path to the profiles.yaml file.
    :raises FileNotFoundError: Raises an error if the file doesn't exist
    :return: The contents of the profiles.yaml file as a dictionary.
    """
    if not profiles_path.exists():
        raise FileNotFoundError(f"profiles.yaml not found at {profiles_path}")

    with profiles_path.open("r") as file:
        profiles = yaml.safe_load(file)

    return profiles


def get_redshift_credentials(
    profile_name: str, target_name: str = "default", profiles_path: Path | None = None
) -> dict[str, Any]:
    """Extract Redshift credentials from a dbt profile.

    :param profile_name: The name of the dbt profile to use.
    :param target_name: The target environment within the dbt profile, defaults to "default".
    :param profiles_path: The path to the profiles.yaml file, defaults to None
    :raises ValueError: _description_
    :raises ValueError: _description_
    :return: A dictionary containing the Redshift credentials.
    """
    if profiles_path is None:
        profiles_path = Path.home() / ".dbt" / "profiles.yaml"

    profiles = load_dbt_profiles(profiles_path)

    if profile_name not in profiles:
        raise ValueError(f"Profile '{profile_name}' not found in profiles.yaml")

    profile = profiles[profile_name]

    if target_name not in profile["outputs"]:
        raise ValueError(f"Target '{target_name}' not found in profile '{profile_name}'")

    target = profile["outputs"][target_name]

    credentials = {
        "host": target["host"],
        "port": target.get("port", 5439),
        "database": target["dbname"],
        "user": target["user"],
        "password": target["password"],
    }

    return credentials
