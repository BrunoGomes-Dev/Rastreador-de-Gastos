import rastreador_de_gastos as rg
import click, csv
from rich.table import Table
from rich.console import Console

@click.group()
def cli():
    pass

categorys = ["1. Alimentação", "2. Transporte", "3. Moradia", "4. Saúde", "5. Outros"]
categorys2 = {
    "Alimentação" : 1,
    "Transporte"  : 2,
    "Moradia" : 3,
    "Saúde" : 4,
    "Outros" : 5
}
months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

@cli.command(help="Adicionar uma nova despesa.")
def add():

    date = click.prompt("Digite a data (DD/MM/YYYY)")

    date = rg.confirme_datetime(date, "%d/%m/%Y", "DD/MM/YYYY", click.prompt)

    description = click.prompt("Digite a descrição")
    value = click.prompt("Digite o valor")

    value = rg.confirmer_value(value, click.prompt)
    
    click.echo("Escolha a categoria:")
    rg.print_list(categorys, click.echo)
    choice_category = click.prompt("Digite o número correspondente")

    choice_category = rg.confirme_number_in_interval(choice_category, 1, 5, click.prompt)
    
    id = 0

    with open("database/id.txt", "r+") as arquivo:
        id = int(arquivo.read().strip())
        arquivo.seek(0)
        arquivo.write(str(id+1))
        arquivo.truncate()

    with open("database/despesas.csv", "a", newline='', encoding="utf-8") as arquivo:
        dados = csv.writer(arquivo)
        dados.writerow([id, date, description, value, choice_category])

    click.echo(f"Despesa com ID {id} adicionada com sucesso!")

@cli.command(help="Editar uma despesa existente.")
@click.argument("id")
def edit(id):
    with open("database/despesas.csv", "r+", encoding="utf-8", newline="") as arquivo:
        dados = csv.DictReader(arquivo)
        linhas = list(dados)

        exist = rg.binary_search(0, len(linhas) - 1, id, linhas)
        
        if exist == -1:
            click.echo("Nenhuma despesa encontrada com o ID fornecido.")
        else:
            click.echo(f"Editando despesa com ID: {id}")
            final_msg = "ou pressione Enter para manter"

            date = click.prompt(f"Data Atual: {linhas[exist]["Data"]}. Digite a nova data (DD/MM/YYYY) {final_msg}", 
            default = linhas[exist]["Data"], show_default = False)
            
            date = rg.confirme_datetime(date, "%d/%m/%Y", "DD/MM/YYYY",click.prompt)

            description = click.prompt(f"Descrição atual: {linhas[exist]["Descrição"]}. Digite a nova descrição ou pressione Enter para manter", 
            default = linhas[exist]["Descrição"], show_default = False)

            value = click.prompt(f"Valor atual: {float(linhas[exist]["Valor"]):.2f}. Digite o novo valor {final_msg}",
            default = linhas[exist]["Valor"], show_default = False)

            value = rg.confirmer_value(value, click.prompt)

            click.echo(f"Categoria atual: {linhas[exist]["Categoria"]}. Escolha uma nova categoria {final_msg}")
            rg.print_list(categorys, click.echo)

            choice_category = click.prompt("Digite o número correspondente",
            default = int(linhas[exist]["Categoria"]), show_default = False)

            choice_category = rg.confirme_number_in_interval(choice_category, 1, 5, click.prompt)

            linhas[exist]["Data"] = date
            linhas[exist]["Descrição"] = description
            linhas[exist]["Valor"] = value
            linhas[exist]["Categoria"] = choice_category

            #subscribe
            fieldnames = dados.fieldnames
            arquivo.seek(0)
            escritor = csv.DictWriter(arquivo, fieldnames=fieldnames)
            escritor.writeheader()
            escritor.writerows(linhas)
            arquivo.truncate()

            click.echo("Despesa editada com sucesso!")


@cli.command(help="Deletar uma despesa existente.")
@click.argument("id")
def delete(id):
    with open("database/despesas.csv", "r+", encoding="utf-8", newline="") as arquivo:
        dados = csv.DictReader(arquivo)
        linhas = list(dados)

        exist = rg.binary_search(0, len(linhas) - 1, id, linhas)
        
        if exist == -1:
            click.echo("Nenhuma despesa encontrada com o ID fornecido.")
        else:
            linhas.pop(exist)

            #subscribe
            fieldnames = dados.fieldnames
            arquivo.seek(0)
            escritor = csv.DictWriter(arquivo, fieldnames=fieldnames)
            escritor.writeheader()
            escritor.writerows(linhas)
            arquivo.truncate()

            click.echo(f"Despesa com ID {id} removida com sucesso!")

@cli.command("list", help="Listar todas as despesas registradas.")
@click.option('--category', default = "", help = "Filtra as despesas por categoria.")
@click.option('--month-year', default = "", help = "Filtra as despesas de um mês/ano específico (formato MM/YYYY).")
def list_(category, month_year):
    if month_year != "" and not rg.check_datetime(month_year, "%m/%Y"):
        click.echo("Formato inválido! Use o formato MM/YYYY")
    elif category in categorys2.keys() or category == "":
        if category != "" and not rg.check_at_interval(categorys2[category], 1, 5):
            click.echo("Formato inválido! Escolha uma categoria entre as existentes.")
        else:
            with open("database/despesas.csv", "r+", encoding="utf-8", newline="") as arquivo:
                dados = csv.DictReader(arquivo)
                linhas = list(dados)
                test = "" if category == "" else str(categorys2[category])
                linhas = rg.filter_list(linhas, test, month_year)

                table = Table()

                table.add_column("ID", justify = "left")
                table.add_column("Data", justify = "left")
                table.add_column("Descrição", justify = "left")
                table.add_column("Valor (R$)", justify = "left")
                table.add_column("Categoria", justify = "left")

                total_value = 0

                for temp in linhas:
                    aux = float(temp["Valor"])
                    total_value += aux
                    table.add_row(temp["ID"], temp["Data"], temp["Descrição"], str(round(aux, 2)), categorys[int(temp["Categoria"]) - 1])
                
                table.add_row(*(["───────────"*2]*5))
                table.add_row("Total", "", "", str(round(total_value, 2)), "")

                console = Console()
                console.print(table)
    else:
        click.echo("Formato inválido! Escolha uma categoria entre as existentes.")

@cli.command(help="Exibir o resumo financeiro mensal.")
@click.argument("date")
def resume(date):
    if rg.check_datetime(date, "%m/%Y") == False:
        click.echo("Formato inválido! Use o formato MM/YYYY.")
    else:
        with open("database/despesas.csv", "r+", encoding="utf-8", newline="") as arquivo:
            dados = csv.DictReader(arquivo)
            linhas = list(dados)
            linhas = rg.filter_list(linhas, "", date)
            month = date.split("/")
            Title = "Resumo financeiro: " + months[int(month[0]) - 1] + "/" + month[1]

            table = Table(title = Title)

            table.add_column("Categoria", justify = "left")
            table.add_column("Valor (R$)", justify = "left")
            table.add_column("Percentual", justify = "left")

            categorias = [0, 0, 0, 0, 0, 0]

            for i in linhas:
                categorias[int(i["Categoria"])-1] += float(i["Valor"])
                categorias[5] += float(i["Valor"])

            for i in range(5):
                if categorias[i] > 0:
                    now = categorys[i].split(" ")
                    table.add_row(now[1], str(round(categorias[i], 2)), str(round(categorias[i] * 100 / categorias[5], 1)) + "%")

            table.add_row("Total Geral", str(round(categorias[5], 2)), "100.0%")

            console = Console()
            console.print(table)

@cli.command(hidden=True)
def factorymode():
    with open("database/id.txt", "w") as arquivo:
        arquivo.write("1")
    
    with open("database/despesas.csv", "w", newline="", encoding="utf-8") as arquivo:
        dados = csv.writer(arquivo)
        dados.writerow(["ID", "Data", "Descrição", "Valor", "Categoria"])

if __name__ == "__main__":
    cli()