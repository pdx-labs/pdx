import os
from pdx import Prompt, PromptChain
from pdx.models.openai.audio.transcription import AudioTranscriptionModel

file_name = 'test_prompt_chain_multimodal.wav'
assets_folder = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), 'assets')
file = os.path.join(assets_folder, file_name)


if __name__ == '__main__':

    audio_prompt = Prompt(file=file)
    ai_prompt = Prompt('the content is in english with an indian accent.')
    prompt_chain = PromptChain(prompts=[audio_prompt, ai_prompt])

    openai_key = os.environ['OPENAI_API_KEY']
    model = AudioTranscriptionModel(api_key=openai_key)
    _ps = prompt_chain.execute()
    _r = model.execute(_ps)
