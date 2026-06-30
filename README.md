# Toy-Bank

A simple toy project for practising GitLab Flow and CI/CD

## Stack

![Devcontainer](https://img.shields.io/badge/-Devcontainer-1a2a40?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-1a2a40?style=for-the-badge&logo=pandas&logoColor=white)
![Pydantic](https://img.shields.io/badge/-Pydantic-1a2a40?style=for-the-badge&logo=pydantic&logoColor=white)
![Pytest](https://img.shields.io/badge/-Pytest-1a2a40?style=for-the-badge&logo=pytest&logoColor=white)
![Python](https://img.shields.io/badge/-Python-1a2a40?style=for-the-badge&logo=python&logoColor=white)
![Ruff](https://img.shields.io/badge/-Ruff-1a2a40?style=for-the-badge&logo=ruff&logoColor=white)
![UV](https://img.shields.io/badge/-UV-1a2a40?style=for-the-badge&logo=uv&logoColor=white)

- **Python:** Main Language
- **UV:** Project dependency manager
- **Pandas:** For database simulation using CSV
- **Pydantic:** For creating DTOs
- **Pytest:** For unit testing
- **Ruff:** For linter and formatting Python code
- **Devcontainer:** Docker container for standardising the development environment

## Pre-Run

- Install docker
- Install devcontainer on VS Code
- Clone the repo
- Reopen in container

## Run

### Local

```sh
make run
```

API disponível em `http://localhost:8000`

### Docker

```sh
docker pull dinorahfariasc/toy-bank:latest
docker run -p 8080:8080 dinorahfariasc/toy-bank:latest
```

API disponível em `http://localhost:8080`

Imagem no Docker Hub: https://hub.docker.com/r/dinorahfariasc/toy-bank

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/banco/conta/` | Criar conta |
| `GET` | `/banco/conta/{account_id}` | Buscar conta |
| `GET` | `/banco/conta/{account_id}/saldo` | Consultar saldo |
| `PUT` | `/banco/conta/{account_id}/credito` | Realizar crédito |
| `PUT` | `/banco/conta/{account_id}/debito` | Realizar débito |
| `PUT` | `/banco/conta/transferencia` | Transferência entre contas |
| `PUT` | `/banco/conta/rendimento` | Aplicar rendimento |

Documentação interativa: `http://localhost:8080/docs`

## Authors

- **Dinorah Farias:** [dinorahfariasc](https://github.com/dinorahfariasc)
- **Rodrigo Faustino:** [RodrigoFaustin0](https://github.com/RodrigoFaustin0)
- **Rômulo Alves:** [romuloAMR](https://github.com/romuloAMR)