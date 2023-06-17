import os
import click
from pdx import __version__
from pdx.agent import AgentBuilder
from pdx.agent.tester import AgentTestBuilder
from pdx.settings import Keys, process


@click.group()
@click.option('--version', is_flag=True, show_default=True, default=False, help='Version of the installed `pdx` package.')
@click.pass_context
def main(ctx, version: bool):
    ctx.ensure_object(dict)

    if version:
        click.echo(__version__)


@main.command("test")
@click.argument("path", required=True, type=str)
@click.option('--debug', is_flag=True, show_default=True, default=False, help='Enables the logging of all requests and responses to the console.')
@click.pass_context
def test(ctx, path: str, debug: bool):

    if debug:
        process.debug = True

    api_keys = Keys()
    agent_path = os.path.join(os.getcwd(), path)
    _agent = AgentBuilder(agent_path, api_keys)
    _tester = AgentTestBuilder(agent_path, _agent)
    _tester.execute()
