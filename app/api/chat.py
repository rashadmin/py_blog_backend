import json
import os
import google.generativeai as genai

class Chat_ai:

    def __init__(self):
        genai.configure(api_key='AIzaSyC639sFB_Aiah4DTyDOY8H-GVpJRid_AMk')
        generation_config = {
                            "temperature": 0.2,
                            "top_p": 0.95,
                            "top_k": 40,
                            "max_output_tokens": 8192,
                            "response_mime_type": "application/json",
                            }
        self.instruction_text = open("app/api/instructions/question_instruction.txt", "r").read()
        self.linkedin_instruction_text = open("app/api/instructions/Linkedin_instruction.txt", "r").read()
        self.facebook_instruction_text = open("app/api/instructions/Facebook_instruction.txt", "r").read()
        self.x_instruction_text = open("app/api/instructions/X_instruction.txt", "r").read()
        self.description_text = open("app/api/instructions/description.txt", "r").read()
        self.model  = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)

    def start_model(self):
        self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.instruction_text],},])

    def continue_model(self,chat_sessions):
        self.chat_session = self.model.start_chat(history=chat_sessions)

    def start_format_model(self,media=None):
        if media == 'facebook':
            self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.facebook_instruction_text],},])
        elif media == 'linkedin':
            self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.linkedin_instruction_text],},])
        elif media == 'X':
            self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.x_instruction_text],},])
        else:
            self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.description_text],},])
    
    def send_text(self,text):
        response = self.chat_session.send_message(text)
        return response.text

    def chat_conversation(self,chatbot=True,new_chat=True):
        if new_chat:
            if chatbot :
                chats = [{'sender':'agent','text':json.loads(self.chat_session.history[i].parts[0].text)['question']} if i%2==0  else {'sender':'user','text':self.chat_session.history[i].parts[0].text} for i in range(1,len(self.chat_session.history)) ]
            else:
                chats = [{'role':'model','parts':json.loads(self.chat_session.history[i].parts[0].text)['question']} if (i%2==0 and i!=0)  else {'role':'user','parts':self.chat_session.history[i].parts[0].text} for i in range(len(self.chat_session.history)) ]
                print(self.chat_session.history[-1].parts[0].text)
        else:
            if chatbot :
                chats = [{'sender':'model','text':json.loads(self.chat_session.history[i].parts[0].text)} if (i%2==0 and i==len(self.chat_session.history)-1) else {'sender':'agent','text':self.chat_session.history[i].parts[0].text} if (i%2==0 and i!=0)  else {'sender':'user','text':self.chat_session.history[i].parts[0].text} for i in range(1,len(self.chat_session.history)) ]
                # chats = [{'sender':'agent','text':self.chat_session.history[i].parts[0].text} if i%2==0  else {'sender':'user','text':self.chat_session.history[i].parts[0].text} for i in range(1,len(self.chat_session.history)) ]
            else:
                print(self.chat_session.history[-1].parts[0].text)
                chats = [{'role':'model','parts':json.loads(self.chat_session.history[i].parts[0].text)} if (i%2==0 and i==len(self.chat_session.history)-1) else {'role':'model','parts':self.chat_session.history[i].parts[0].text} if (i%2==0 and i!=0)  else {'role':'user','parts':self.chat_session.history[i].parts[0].text} for i in range(len(self.chat_session.history)) ]
        return chats
    
    
    def generate(self,conversation):
        response = self.chat_session.send_message(conversation)
        return response.text

    
############################################################
'''Return a list of dictionary like object that contain two keys, the sender and the text'''
'''The error is that session.history is returning an object of type content, which can't be serializable, by json'''