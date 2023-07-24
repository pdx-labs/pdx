from pdx import Prompt

text_prompt = Prompt(
    template="What are the uses of {{compound}}?", pointer="1_prompt")


if __name__ == '__main__':
    _response = text_prompt.execute({'compound': 'Nitrogen'})
    print(_response)
