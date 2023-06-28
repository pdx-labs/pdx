import os
import click
from pdx import __version__
from pdx.logger import logger
from pdx.agent import AgentBuilder
from pdx.agent.tester import AgentTestBuilder
from pdx.settings import Keys, process
from pdx.commands.create import create_agent


@click.group()
@click.option('--version', is_flag=True, show_default=True, default=False, help='Version of the installed `pdx` package.')
@click.pass_context
def main(ctx, version: bool):
    ctx.ensure_object(dict)

    if version:
        click.echo(__version__)


@main.command("create")
@click.argument("agent_name", required=True, type=str)
@click.option('--template', default='simple', show_default=True, help='Creates an agent with a template. Options: `simple`, `chat`, `tree`.')
@click.pass_context
def test(ctx, agent_name: str, template: str):

    if template not in ['simple', 'chat', 'tree']:
        logger.echo(f"Template {template} not found.", "error")
    else:
        _dest = create_agent(agent_name, template)
        logger.echo(f"Agent `{agent_name}` created.")
        logger.echo(f"Agent path: {_dest}")


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
