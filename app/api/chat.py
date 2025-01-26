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
        self.instruction_text = open("app/api/question_instruction.txt", "r").read()
        self.linkedin_instruction_text = open("app/api/Linkedin_instruction.txt", "r").read()
        self.facebook_instruction_text = open("app/api/Facebook_instruction.txt", "r").read()
        self.x_instruction_text = open("app/api/X_instruction.txt", "r").read()
        self.model  = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)

    def start_model(self):
        self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.instruction_text],},])

    def start_format_model(self,media):
        if media == 'Facebook':
            self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.facebook_instruction_text],},])
        elif media == 'Linkedin':
            self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.linkedin_instruction_text],},])
        elif media == 'X':
            self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.x_instruction_text],},])
        else:
            self.chat_session = self.model.start_chat(history=[{"role": "user","parts": [self.instruction_text],},])
    
    def formats (self,i):
        no =  (i - 1) // 2 + 1
        if i%2==0:
            return {f'question_{no}':json.loads(self.chat_session.history[i].parts[0].text)['question']}
        else:
            return {f'text_{no}':self.chat_session.history[i].parts[0].text}
        

    def create_twitter_threads(self,blog_post, max_chars_per_tweet=280):
        """
        Divides a given blog post into a list of Twitter threads, 
        considering Twitter's character limit.

        Args:
            blog_post: The text of the blog post.
            max_chars_per_tweet: The maximum number of characters allowed per tweet.

        Returns:
            A list of strings, where each string represents a single Twitter thread.
        """

        threads = []
        current_thread = ""

        words = blog_post.split()
        for word in words:
            if len(current_thread) + len(word) + 1 <= max_chars_per_tweet:
                current_thread += f" {word}"
            else:
                threads.append(current_thread.strip())
                current_thread = word

        if current_thread:
            threads.append(current_thread.strip())

        return threads

    def send_text(self,text):
        response = self.chat_session.send_message(text)
        return response.text

    def chat_conversation(self):
        chats = [{'sender':'agent','text':json.loads(self.chat_session.history[i].parts[0].text)['question']} if i%2==0  else {'sender':'user','text':self.chat_session.history[i].parts[0].text} for i in range(1,len(self.chat_session.history)) ]
        return chats

    def get_conversation(self):
        conversation = [self.formats(i) for i in range(1,len(self.chat_session.history)-1)]
        return conversation
    
    def format_text(self,text):
        response = self.chat_session.send_message(text)
        return response.text

    
