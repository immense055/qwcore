
from click import echo, style


def info(msg):
    echo(msg)


def success(msg):
    echo(style(msg, fg='green'))


def warning(msg):
    echo(style(msg, fg='yellow'))


def error(msg):
    echo(style(msg, fg='red'))
