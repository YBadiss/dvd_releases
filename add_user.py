import click

from source.store import Store


@click.command()
@click.option("--number", prompt="Number")
def main(number):
    store = Store()
    store.add_user(number)


if __name__ == "__main__":
    main()
