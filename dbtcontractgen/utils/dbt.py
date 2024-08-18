import sys
from pathlib import Path
from typing import Any

import yaml


def validate_profile(profile: dict[str, Any], target_name: str) -> dict[str, Any]:
    """Validate and extract the Redshift credentials from a profile.

    :param profile: The profile dictionary to validate.
    :param target_name: The target environment within the profile.
    :raises ValueError: If the target or required fields are missing.
    :return: The validated target environment with credentials.
    """
    if target_name not in profile.get("outputs", {}):
        raise ValueError(f"Target '{target_name}' not found in profile")

    target = profile["outputs"][target_name]

    # Ensure that all required fields are present
    required_fields = {
        "host": ["host", "hostname"],
        "dbname": ["dbname", "database", "db"],
        "user": ["user", "username"],
        "password": ["password", "pass"],
    }
    for field, aliases in required_fields.items():
        field_found = False
        for alias in aliases:
            if alias in target:
                target[field] = target[alias]
                field_found = True
                break
        if not field_found:
            raise ValueError(f"Missing required field '{field}' in target '{target_name}'")

    return target


def get_dbt_target(
    profile_name: str, target_name: str = "default", profiles_path: Path | None = None
) -> dict[str, Any]:
    """Load a specific dbt profile and gets a specific target.

    :param profile_name: The name of the dbt profile to use.
    :param target_name: The target environment within the dbt profile, defaults to "default"
    :param profiles_path: The path to the profiles.yaml file, defaults to None
    :raises FileNotFoundError: If the profiles.yaml file does not exist.
    :raises ValueError: If the profile or target environment is not found or is invalid.
    :return: The validated target environment with credentials.
    """
    if profiles_path is None:
        profiles_path = Path.home() / ".dbt" / "profiles.yml"

    if not profiles_path.exists():
        raise FileNotFoundError(f"profiles.yml not found at {profiles_path}")

    with profiles_path.open("r") as file:
        profiles = yaml.safe_load(file)

    if profile_name not in profiles:
        raise ValueError(f"Profile '{profile_name}' not found in profiles.yaml")

    profile = profiles[profile_name]
    return validate_profile(profile, target_name)


def get_credentials(
    profile_name: str, target_name: str = "default", profiles_path: Path | None = None
) -> dict[str, Any]:
    """Extract Redshift credentials from a dbt profile.

    :param profile_name: The name of the dbt profile to use.
    :param target_name: The target environment within the dbt profile, defaults to "default".
    :param profiles_path: The path to the profiles.yaml file, defaults to None
    :return: A dictionary containing the Redshift credentials.
    """
    target = get_dbt_target(profile_name, target_name, profiles_path)

    credentials = {
        "host": target["host"],
        "port": target.get("port", 5439),
        "database": target["dbname"],
        "user": target["user"],
        "password": target["password"],
    }

    return credentials


def generate_source_yml(metadata: list[tuple, any], schema: str, file_path: str | None = None):
    dbt_source = {"version": 2, "models": []}

    tables = {}
    for table, column, dtype in metadata:
        if table not in tables:
            tables[table] = {"name": table, "config": {"contract": {"enforced": True}}, "columns": []}
        tables[table]["columns"].append({"name": column, "data_type": dtype})

    for table in tables.values():
        dbt_source["models"].append(table)

    yaml_str = yaml.safe_dump(
        dbt_source,
        sort_keys=False,
        default_flow_style=False,
    )

    if file_path:
        with open(file_path, "w") as file:
            file.write(yaml_str)
    else:
        sys.stdout.write(yaml_str)
