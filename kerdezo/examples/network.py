import ipaddress
import sys

from kerdezo import Kerdezo

def ipAddressValidator(value, context):
    ipaddress.ip_address(value)  # Raises exception on invalid IP address input

def portNumberValidator(value, context):
    if value < 1 or value > 65535:
        raise ValueError(f"Invalid port number: {value}")

def failHandler(err, context):
    print(f"Error: {err}", file=sys.stderr)

def protocolAnswerHook(value, context):
    pass

if __name__ == "__main__":
    suite = Kerdezo(
        startMessage="""In this suite we will ask for network-related data.
To get help on a question, answer with '?' (without apostrophes)
""",
        failHandler=failHandler
    )

    suite.addQuestion(
        "IP address",
        help="Type an IPv4 or IPv6 address",
        validators=[ipAddressValidator]
    )

    suite.addQuestion(
        "Protocol",
        choices=["http", "https"],
        hooks={
            "answer": protocolAnswerHook
        }
    )

    suite.addQuestion(
        "Port",
        type=int,
        default=8080,
        help="Type a TCP port number",
        validators=[portNumberValidator]
    )

    suite.ask()
