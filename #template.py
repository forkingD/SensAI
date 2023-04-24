import gradio as gr
import openai 
import os
os.environ.get('OPENAI_API_KEY')

with gr.Blocks() as interface:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    #chat_history=[]

    def OpenAI(prompt, chat_history):
        messages_arr = [{"role": "assistant", "content": message} for _, message in chat_history] + [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_arr,
            temperature=0.8,
            max_tokens=1024,
            )
        message = response['choices'][0]['message']['content']
        cost = response['usage']['total_tokens']
        chat_history.append((prompt, message))
        return "", chat_history

    msg.submit(OpenAI, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

interface.launch()
