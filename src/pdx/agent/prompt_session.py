ANTHROPIC_CONSTANTS_HUMAN_PROMPT = '\n\nHuman:'
ANTHROPIC_CONSTANTS_AI_PROMPT = '\n\nAssistant:'


class PromptSession:
    def __init__(self, prompt_type: str = None):
        self.session = []
        self.type = prompt_type

    def add(self, prompt: str, role: str):
        self.session.append({
            'content': prompt,
            'role': role
        })

    def stitch_for_text_completion(self):
        _prompt = ''
        for _session in self.session:
            _prompt += _session['content']
        return _prompt

    def chat_to_text_prompt_openai(self):
        prompt = ''
        for message in self.session:
            if message['role'] == 'user':
                prompt += f"\n\nUSER {message['content']}"
            elif message['role'] == 'assistant':
                prompt += f"\n\nASSISTANT {message['content']}"
            elif message['role'] == 'system':
                prompt += f"\n\nSYSTEM {message['content']}"

        prompt += f"\n\nASSISTANT"
        return prompt

    def text_to_chat_prompt_openai(self):
        prompt = self.stitch_for_text_completion()
        messages = [
            {"role": "user", "content": prompt}
        ]
        return messages

    def session_to_prompt_anthropic(self):
        if self.type == 'chat':
            prompt = ''
            for message in self.session:
                if message['role'] == 'user':
                    prompt += f"{ANTHROPIC_CONSTANTS_HUMAN_PROMPT} {message['content']}"
                elif message['role'] == 'assistant':
                    prompt += f"{ANTHROPIC_CONSTANTS_AI_PROMPT} {message['content']}"
                elif message['role'] == 'system':
                    prompt += f"{ANTHROPIC_CONSTANTS_HUMAN_PROMPT} {message['content']}"

            prompt += f"{ANTHROPIC_CONSTANTS_AI_PROMPT}"
            return prompt
        elif self.type == 'text':
            prompt = self.stitch_for_text_completion()
            return f"{ANTHROPIC_CONSTANTS_HUMAN_PROMPT} {prompt}{ANTHROPIC_CONSTANTS_AI_PROMPT}"
