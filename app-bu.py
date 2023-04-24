import gradio as gr
import openai 
import os
os.environ.get('OPENAI_API_KEY')

title="Sensei AI"
system_prompt="act as a Shotokan Karate Sensei. the user is your student. \
            if the users input is not karate related, remind them that its now time to focus on karate.\
            give them a few warm up drills, then ask for belt level and what they want to work on, then provide relevant technical exercises.\
            brief instructions and explanations, encourage feedback.\
            for longer instructions, go step by step."

with gr.Blocks() as interface:
    chat_history = [("","Hello, I am your Sensei AI. What is your belt level, and what do you want to work on today?")]
    chatbot = gr.Chatbot(label=title)
    msg = gr.Textbox(label="", placeholder="your belt level, and what you want to work on")
    #clear = gr.Button("Clear")

    def OpenAI(prompt, chat_history):
        messages_arr = [{"role": "system", "content": system_prompt}] + [{"role": "assistant", "content": message} for _, message in chat_history] + [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_arr,
            temperature=0.8,
            max_tokens=1024,
            )
        message = response['choices'][0]['message']['content']
        cost = response['usage']['total_tokens']
        chat_history.append((prompt, message))
        yield "", chat_history

    msg.submit(OpenAI, [msg, chatbot], [msg, chatbot], queue=False)
    #clear.click(lambda: None, None, chatbot, queue=False)

interface.queue()
interface.launch()
