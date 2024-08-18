import click


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
    nargs=1,
)
@click.option(
    "-t",
    "--table",
    multiple=True,
    help="Table to extract, can be used multiple times to extract more tables",
)
@click.option(
    "-d",
    "--db",
    type=click.Choice(["postgresql", "redshift"], case_sensitive=False),
    required=True,
    help="Specify the type of database to connect to",
)
def extract(schema, table):
    click.echo(f"Schema: {schema}")
    for t in table:
        click.echo(f"Table: {t}")


cli.add_command(extract)
