import click

from dbtcontractgen.connection.postgresql import PostgreSQLConnection
from dbtcontractgen.connection.redshift import RedshiftConnection
from dbtcontractgen.utils.dbt import generate_source_yml, get_credentials
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
@click.option(
    "-o",
    "--output",
    type=str,
    help="Specify the path of the output file",
)
def extract(schema, table, database, profile, target, filepath, output):
    click.echo(f"Generating data contract for schema: {schema} containing the following tables: {table}")

    if database == "postgresql":
        credentials = get_credentials(profile_name=profile, target_name=target, profiles_path=filepath)
        with PostgreSQLConnection(**credentials) as conn:
            result = conn.run_query(FETCH_METADATA_QUERY.format(schema=schema))
            generate_source_yml(metadata=result, schema=schema, file_path=output)

    elif database == "redshift":
        credentials = get_credentials(profile_name=profile, target_name=target, profiles_path=filepath)
        with RedshiftConnection(**credentials) as conn:
            result = conn.run_query(FETCH_METADATA_QUERY.format(schema=schema))
            generate_source_yml(metadata=result, schema=schema, file_path=output)


cli.add_command(extract)
