import click

from dbtcontractgen.connection.postgresql import PostgreSQLConnection
from dbtcontractgen.utils.dbt_profile_parser import get_redshift_credentials
from dbtcontractgen.utils.queries import FETCH_METADATA_QUERY


@click.group()
def cli():
    """
    dbt-contract-gen is an open source CLI tool for generating dbt contracts.
    """


# TODO add command that checks if the cli can connect to Redshift


# TODO modify command so that it runs a query in Redshift and outputs a dbt contract
@click.command(help="Extracts table structure from a database and outputs a dbt contract")
@click.argument(
    "schema",
    type=str,
    nargs=1,
)
@click.option(
    "-t",
    "--table",
    type=str,
    multiple=True,
    help="Table to extract, can be used multiple times to extract more tables",
)
@click.option(
    "-db",
    "--database",
    type=click.Choice(["postgresql", "redshift"], case_sensitive=False),
    required=True,
    help="Specify the type of database to connect to",
)
@click.option(
    "-p",
    "--profile",
    type=str,
    required=True,
    help="Specify the dbt profile to use",
)
@click.option(
    "-tg",
    "--target",
    type=str,
    help="Specify the dbt target to use",
)
@click.option(
    "-f",
    "--filepath",
    type=str,
    help="Specify the path of your dbt profile",
)
def extract(schema, table, database, profile, target, filepath):
    click.echo(f"Schema: {schema}")
    for t in table:
        click.echo(f"Table: {t}")

    if database == "postgresql":
        credentials = get_redshift_credentials(profile_name=profile, target_name=target, profiles_path=filepath)
        with PostgreSQLConnection(**credentials) as conn:
            result = conn.run_query(FETCH_METADATA_QUERY.format(schema=schema))
        print(result)
    elif database == "redshift":
        credentials = get_redshift_credentials(profile_name=profile, target_name=target, profiles_path=filepath)
        print(credentials)


cli.add_command(extract)
