# TabulateDockerPS

[![MIT License](https://img.shields.io/github/license/viniciusccosta/clipbarcode)](https://choosealicense.com/licenses/mit/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/downloads/release/python-3125/)

TabulateDockerPS é um script Python que transforma a saída do comando docker ps em uma tabela formatada utilizando a biblioteca tabulate. Isso permite que a saída seja visualmente mais organizada e de fácil leitura. O script é simples de usar e pode ser instalado via pipx, tornando-o fácil de integrar em qualquer ambiente de desenvolvimento que utilize Docker.

## Instalação

```bash
pipx install tabulatedockerps
```

## Uso

Para utilizar o script, simplesmente redirecione a saída do comando `docker ps` para o script Python:

```bash
docker ps | tdps [--debug] [--format FORMAT]
```

## Exemplo de Saída

Ao executar o comando docker ps e passar a saída para o TabulateDockerPS, você obtém uma tabela formatada, com destaque para a coluna "Ports", que é dividida em várias linhas para facilitar a leitura dos múltiplos mapeamentos de portas. Veja o exemplo abaixo:

```bash
$ docker ps | tdps

+----------------+---------+--------------------------+----------------+---------------+------------------------+
| CONTAINER ID   | IMAGE   | COMMAND                  | CREATED        | STATUS        | PORTS                  |
+================+=========+==========================+================+===============+========================+
| 874ace075081   | ubuntu  | "bash -c 'while true…"   | 37 minutes ago | Up 37 minutes | 0.0.0.0:8080->8080/tcp |
|                |         |                          |                |               | 0.0.0.0:80->80/tcp     |
+----------------+---------+--------------------------+----------------+---------------+------------------------+
```

## Formatos Suportados

O TabulateDockerPS suporta todos os formatos de saída oferecidos pela biblioteca tabulate. Isso inclui, mas não se limita a:

- plain
- grid
- pipe
- orgtbl
- jira
- presto
- pretty
- html
- latex

Para uma lista completa de formatos, consulte a documentação do [tabulate](https://pypi.org/project/tabulate/).

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias ou correções.

## Licença

Este projeto é distribuído sob a licença MIT. Para mais detalhes, consulte o arquivo LICENSE
