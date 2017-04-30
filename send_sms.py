import click

from twilio.rest import Client

from source import twilio_secrets


def send_msg(body, to):
    client = Client(twilio_secrets.ACCOUNT_SID, twilio_secrets.AUTH_TOKEN)
    client.messages.create(to=to,
                           from_=twilio_secrets.PHONE_NUMBER,
                           body=body)


@click.command()
@click.option("--body", prompt="Body")
@click.option("--to", prompt="Send to")
def main(body, to):
    send_msg(body, to)


if __name__ == "__main__":
    main()
