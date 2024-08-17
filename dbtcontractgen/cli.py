import click


@click.group()
def cli():
    """
    dbt-contract-gen is an open source CLI tool for generating dbt contracts.
    """


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
def extract(schema, table):
    click.echo(f"Schema: {schema}")
    for t in table:
        click.echo(f"Table: {t}")


cli.add_command(extract)
