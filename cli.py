import click

import money_lib


@click.group()
def cli():
    pass

@click.command()
@click.option('--example', is_flag=True, default=False)
def mortgage_calculation(example):
    if example:
        mort = money_lib.MortgageCalculate().example()
        mort.pay_mortgage()

cli.add_command(mortgage_calculation)

if __name__ == "__main__":
    cli()