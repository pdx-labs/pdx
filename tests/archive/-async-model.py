import os
import asyncio
from pdx import Prompt, PromptChain
from pdx.models.openai.audio.transcription import AudioTranscriptionModel

file_name = '/Users/adithya/projects/pdx-org/pdx/rough_books/test_audio_1.mpeg'
audio_prompt = Prompt(file=file_name)
ai_prompt = Prompt('the content is in english with an indian accent.')
prompt_chain = PromptChain(prompts=[audio_prompt, ai_prompt])

openai_key = os.environ['OPENAI_API_KEY']
model = AudioTranscriptionModel(api_key=openai_key, response_format='json')


async def main():
    _ps = prompt_chain.execute()
    response = await model.aexecute(_ps)
    print(response)


if __name__ == '__main__':
    asyncio.run(main())
