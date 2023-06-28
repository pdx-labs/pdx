import os
import yaml
from pdx.logger import logger
from shutil import copytree
from pdx.templates import TEMPLATES_PATH


def create_agent(agent_name: str, template: str = 'simple') -> str:
    current_working_directory = os.getcwd()
    base_template_path = os.path.join(TEMPLATES_PATH, template)

    agent_folder_path = os.path.join(current_working_directory, agent_name)
    try:
        destination = copytree(base_template_path, agent_folder_path)
        with open(os.path.join(agent_folder_path, 'config.yaml'), 'w') as file:
            file.write('# PDX AGENT CONFIG\n')
            file.write('---\n')
            dump_content = {
                'name': f'{agent_name}',
                'comment': f'Configuration for the PDX Agent {agent_name}.',
                'model': {'id': 'text-davinci-003'},
                'prompt': [{'template': '1_prompt.jinja'}]
            }
            yaml.dump(dump_content, file, indent=4, sort_keys=False)

        os.mkdir(os.path.join(agent_folder_path, '.pdx'))

        return destination

    except FileExistsError as e:
        logger.echo("Agent not created.", event="error")
        logger.echo(
            f"There are folders/files in the current working directory that conflict with the agent creation.", event="error")
        # raise FileExistsError(e)
