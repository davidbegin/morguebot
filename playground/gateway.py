import requests
import click

@click.command()
@click.option('--command', '-c')
def xl_bot(command):
    url = f"https://zl5r1fjaxf.execute-api.us-west-2.amazonaws.com/Stage/xl-bot/{command}"

    response = requests.get(url)
    click.secho(response.text, fg="cyan")

if __name__ == "__main__":
    xl_bot()
