import os
import asyncio
from pdx import Prompt, PromptChain
from pdx.settings import process
from pdx.models.openai.audio.transcription import AudioTranscriptionModel
from pdx.models.openai.image.generation import ImageGenerationModel
from pdx.models.openai.completion import CompletionModel
from pdx.models.elevenlabs.tts import TextToSpeechModel

ASSETS_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'assets')

process.verbose = True

# file_name = os.path.join(ASSETS_PATH, 'audio_en.wav')
# audio_prompt = Prompt(file=file_name)
# ai_prompt = Prompt('the content is in english.')
# prompt_chain = PromptChain(prompts=[audio_prompt, ai_prompt])

# openai_key = os.environ['OPENAI_API_KEY']
# model = AudioTranscriptionModel(api_key=openai_key, response_format='json')

# elevenlabs_key = os.environ['ELEVENLABS_API_KEY']
# openai_key = os.environ['OPENAI_API_KEY']
# # model = TextToSpeechModel(api_key=elevenlabs_key)
# model = ImageGenerationModel(api_key=openai_key)
# prompt = Prompt('An astronaut riding a horse in photorealistic style.')
# prompt_chain = PromptChain(prompts=[prompt])

openai_key = os.environ['OPENAI_API_KEY']
model = CompletionModel(api_key=openai_key, model='text-davinci-003')
prompt = Prompt('What is prompt engineering for multimodal AI?')
prompt_chain = PromptChain(prompts=[prompt])


async def main():
    _ps = prompt_chain.execute()
    response = await model.aexecute(_ps)
    print(response)


if __name__ == '__main__':
    asyncio.run(main())
