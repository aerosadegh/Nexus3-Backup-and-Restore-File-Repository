# Nexus Repository Backup and Restore

This project provides a set of commands to backup and restore files in a Nexus Repository. It uses the Typer library to create a command-line interface (CLI).

## Installation

Before running the commands, make sure you have Python 3.12 or later installed. Then, install the required libraries with pip:

```bash
pip install -r requirements.txt
```

## Usage

The CLI provides three commands: `repo-list`, `download`, and `upload`.

### repo-list

The `repo-list` command retrieves a list of repositories from a Nexus server.

```bash
python scripts repo-list --nexus-base-url http://example.com:8081 --username <username> --password <password>
```

### download

The `download` command downloads components from a Nexus repository to a local directory.

```bash
python scripts download --nexus-base-url http://example.com:8081 --repo-name <repository-name> --username <username> --password <password> --destination <path>
```

#### Download Command Options

| Option         | Default Value       | Description                       |
|----------------|---------------------|-----------------------------------|
| nexus-base-url | <http://localhost:8081> | The repository URL                |
| repo-name      | pypi-all            | The repository name               |
| username       | admin               | The username for authentication   |
| password       | admin123            | The password for authentication   |
| destination    | backup              | The destination for backup        |

### upload

The `upload` command uploads components from a local directory to a Nexus repository.

```bash
python scripts upload --nexus-base-url http://example.com:8081 --repo-name <repository-name> --username <username> --password <password> --source_directory <path>
```

#### Upload Command Options

| Option           | Default Value       | Description                       |
|------------------|---------------------|-----------------------------------|
| nexus-base-url   | http://localhost:8081 | The repository URL                |
| repo-name        | pypi-all            | The repository name               |
| username         | admin               | The username for authentication   |
| password         | admin123            | The password for authentication   |
| source-directory | backup              | The source directory for restore  |

In these commands, replace `http://example.com:8081`, `<repository-name>`, `<username>`, `<password>`, and `<path>` with your Nexus server URL, repository name, username, password, and the path to the local directory, respectively.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
