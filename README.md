# Rastreador de Gastos

Uma ferramenta de terminal que visa rastrear seus gastos, permitindo adicionar, remover, editar, listar e resumir despesas.

## Instalação e pré-requisitos

- Para este projeto funcionar, deve ter Python instalado em seu computador. Para verificar, abra o terminal e digite `python --version`. Se não aparecer nada, instale através da página oficial: [Python](https://www.python.org/downloads/).
- Clone o repositório em seu computador
- Após isto, execute `pip install -r requirements.txt` no terminal.
- Abra o terminal na pasta do projeto e digite: `python main.py`, o programa executará normalmente.

### Uso
O programa contém 6 funções principais, sendo elas:

- `python main.py add`: adicione itens a tua lista;
- `python main.py delete <id>`: delete um item a partir de um ID;
- `python main.py edit <id>`: digite um ID e modifique os dados do item;
- `python main.py list`: lista seus gastos. Pode filtrar a partir de data e categoria. Para mais informações, digite `python main.py list --help` no terminal.
- `python main.py resume`: lista de forma resumida seus gastos em uma data. Para mais informações, digite `python main.py resume --help`
- `python main.py factorymode`: este comando reseta o programa a fase de fábrica, sem nenhum gasto e com ID a partir de 1. Só use se quiser deletar tudo.

### Estrutura do Projeto

```
|── database/
    |── despesas.csv
    |── id.txt
|── rastreador_de_gastos
    |── \__init__.py
    |── check.py
    |── confirme.py
    |── utils.py
|── .gitignore
|── LICENSE
|── main.py
|── README.md
|── requirementx.txt
```

## Licensa

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.