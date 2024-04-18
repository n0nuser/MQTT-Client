# MQTT Client

## Description

Python MQTT Client that reads a JSON file with keys, connects to an MQTT server, logs messages and inserts into a DB.

## Table of Contents

- [MQTT Client](#mqtt-client)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Contributing](#contributing)
  - [Getting Started](#getting-started)
    - [What comes in this template?](#what-comes-in-this-template)
    - [Requisites](#requisites)
    - [Docker](#docker)
    - [Development](#development)
  - [Roadmap](#roadmap)

## Contributing

Check the [contributing documentation](.github/CONTRIBUTING.md) for more information.

## Getting Started

### What comes in this template?

- [x] Docker
- [x] Docker Compose
- [x] GitHub Issues Templates
- [x] Pull Request Template
- [x] Contributing Guidelines
- [x] Poetry for dependency management
- [x] Pre-commit hooks
- [x] Linters and formatters
- [x] GitIgnore for Python projects
- [x] Documentation for Poetry, Docker and Recommended Extensions for VSCode

### Requisites

- [Python 3.10 or higher](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/): Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. For documentation refer to [Poetry](https://python-poetry.org/docs/) or to a little guide we made [here](docs/poetry.md).
- [Docker](https://www.docker.com/): Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers. For documentation refer to [Docker](https://docs.docker.com/get-started/).

### Docker

Also, you can use the `docker-compose` to start the application with the following command:

```bash
cd docker
docker-compose up
```

If you don't know how to use Docker, you can check the [Docker documentation](https://docs.docker.com/get-started/) and our [deployment documentation](docs/deployment.md).

### Development

> [!IMPORTANT]
> Be sure to:
>
> - Run `pre-commit install` to install the pre-commit hooks. This will run the linters and formatters before you commit your code. If you don't have pre-commit installed in your system, you can install it with `pip install pre-commit`.
> - Check the [project structure documentation](docs/project-structure.md) for more information.
> - Check the [recommended extensions documentation](docs/recommended-extensions.md) for more information.
> - Check the [contributing documentation](.github/CONTRIBUTING.md) for more information.
> - Check the [deployment documentation](docs/deployment.md) for more information.

## Roadmap

See the open issues for a full list of proposed features (and known issues).
