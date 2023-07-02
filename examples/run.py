from text_agent import text_agent
from chat_agent import chat_agent

if __name__ == '__main__':
    _question = 'What are the uses of Glucose?'

    _response_text = text_agent.execute({
        '1_prompt': {'question': _question}
    })
    print(_response_text)

    _response_chat = chat_agent.execute({
        '2_user': {'question': _question}
    })
    print(_response_chat)
