import json
import os
import google.generativeai as genai

class Chat_ai:

    def __init__(self):
        # genai.configure(api_key='')
        generation_config = {
                            "temperature": 0.2,
                            "top_p": 0.95,
                            "top_k": 40,
                            "max_output_tokens": 8192,
                            "response_mime_type": "application/json",
                            }
        self.instruction_text = open("app/api/question_instruction.txt", "r").read()
        self.model  = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)

    def start_model(self):
        self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.instruction_text],},])

    def formats (self,i):
        no =  (i - 1) // 2 + 1
        if i%2==0:
            return {f'question_{no}':json.loads(self.chat_session.history[i].parts[0].text)['question']}
        else:
            return {f'text_{no}':self.chat_session.history[i].parts[0].text}

    def send_text(self,text):
        response = self.chat_session.send_message(text)

    def get_conversation(self):
        conversation = [self.formats(i) for i in range(1,len(self.chat_session.history)-1)]
        return conversation
    
