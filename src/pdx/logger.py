import click
from typing import Union
from pdx.settings import process


class Logger:
    '''
    Create a logger context, that can output to the console and also store it in a file.
    '''

    def __init__(self, console_log: bool = True, file_log: bool = False):
        self.options = {
            'console_log': console_log,
            'file_log': file_log,
            'use_click': True,
        }

    def set_options(self, option_value: dict):
        for option, value in option_value.items():
            self.options[option] = value

    def _click_echo(self, msg: Union[str, dict], event: str):
        # green, blue, magenta, cyan, white, red, yellow
        msg = str(msg)

        if 'info' in event:
            click.echo(f'{click.style("PDX::INFO:   ", fg="green")}{msg}')
        elif 'warning' in event:
            click.echo(
                f'{click.style("PDX::WARN:   ", fg="yellow")}{msg}')
        elif 'error' in event:
            click.echo(f'{click.style("PDX::ERROR:  ", fg="red")}{msg}')
        elif 'test' in event:
            click.echo(f'{click.style("PDX::TEST:   ", fg="cyan")}{msg}')
        elif 'dev' in event:
            click.echo(f'{click.style("PDX::DEV:    ", fg="yellow")}\n{msg}')
        else:
            click.echo(f'{click.style("PDX::INFO:   ", fg="cyan")}{msg}')

    def echo(self, msg: Union[str, dict], event: str = 'info'):
        '''
        Example usage:            
            logger.echo(msg="Hello World")
            logger.echo(msg="A warning message", event="warning")
        '''

        if self.options['console_log']:
            if self.options['use_click']:
                self._click_echo(msg=msg, event=event)
            else:
                print(msg)

    def verbose(self, msg: Union[str, dict], event: str = 'verbose'):
        '''
        Example usage:            
            logger.verbose(msg="A verbose message.")
        '''
        if process.verbose:
            if self.options['console_log']:
                if self.options['use_click']:
                    self._click_echo(msg=msg, event=event)
                else:
                    print(msg)


logger = Logger()
