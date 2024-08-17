# dbt-contract-gen

## Overview

**dbt-contract-gen** is a command-line interface (CLI) tool designed to streamline the process of generating dbt
contracts directly from your database. By connecting to your database, this tool automatically inspects the tables
present and generates dbt contracts that can be seamlessly integrated into your dbt project.

## Installation

You can install **dbt-contract-gen** using one of the following methods:

### Using pip:

```bash
pip install dbt-contract-gen
```

### Using pipx:

```bash
pipx install dbt-contract-gen
```

### Using Homebrew:

```bash
brew install dbt-contract-gen
```

## Usage

To use **dbt-contract-gen**, ensure that you have an existing dbt project with a properly configured database
connection. The tool relies on this connection to generate the contracts.

### Basic Command

The primary command provided by **dbt-contract-gen** is the `extract` command, which connects to your database and
generates the contracts.

```bash
dbt-contract-gen extract <your-schema>
```

This command will:

1. Connect to the database specified in your dbt project.
2. Analyze the schema and tables (optional) provided.
3. Generate dbt contracts based on the detected structures.

### Example

```bash
dbt-contract-gen extract my_schema -t my_table
```

This command will generate the contracts and place them in the `contracts/` directory.

## Configuration

**dbt-contract-gen** does not require any additional configuration beyond an existing dbt project with a working
database connection. Ensure your `profiles.yml` is correctly configured for the target database you want to generate
contracts for.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

Please make sure to update tests as appropriate and adhere to the coding standards used in the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors and Acknowledgments

- **Arnaud Caldow** - Initial work

Special thanks to the dbt community for providing excellent tools and support.

## Contact Information

If you have any questions, issues, or suggestions, feel free to open an issue on the GitHub repository or find me:

- [Email](mailto:arnaud.caldow@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/arnaud-caldow-384423142/)
