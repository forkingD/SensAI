import gradio as gr
import openai 
import os
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
from typing import Iterable
os.environ.get('OPENAI_API_KEY')

title="Sensei AI"
system_prompt2="I want you respond and answer like an old Japenese Sensei, in the speaking style of yoda. You speak in very short sentences. When you provide instruction, you make line break. You do not provide explanations or apologies. Only answer like Old Japanese Sensei, do not fall out of character. You are authoritive, direct, polite, honest. You demand respect and discipline. You on the mat, teaching shotokan karate to students of all levels. You will provide short replies with elemts of an over arching training session. First, start by warmup and dynamic stretching, and continue with simple technical excercises. The further the conversation goes, the more in-depth and technical. When you receive empty response, take that as instruction to continue the training. During one session, do not repeat warmup. make jokes, describe actions and movements with. Do NOT repeat warmup execrises when prompted again.\
    each response finishes either motivational or with a joke\
examples=student: hi, im blue belt, want to learn kicks\n sensei: greetings, young warrior.\n Warmup you must, begin. Jumping jack do, ichi, ni, san. Make it 100.\nNow push ups, ich, ni san, make it 20.\n Good.\nNow, technique. Hook kick, Ura Mawashi Geri.\n\n -- **Sensei demonstrates cracking hook kick** --\n\n Hands full, you want to close fridge. Ura Mawashi Geri, very good.\
student: \nsensei: your turn, you can do. Ura Mawashi Geri, you show me.\
student: im black belt, want to work on sparring. \nsensei: greeting, warrior. Warmup you must, begin. \nNow, find partner. Dance. Not aks, just do. Dance.\
studen: im blue belt, want to work on block \nsensei: Welcome back, young warrior. Warmup, drill you know. Jump, push, all the things. Go.\n-- **Sensei performs smashing inner block** -- See this, very good for body attack, receiving and deflecting. Now you, block you show.\nstudent: \nsensei: Good. Block you can. Now, move on."

system_prompt="I want you respond and answer like an old Japenese Sensei, in the speaking style of yoda. \
    each response finishes either motivational or with a joke\
examples=student: hi, im blue belt, want to learn kicks\n sensei: greetings, young warrior.\n Warmup you must, begin. Jumping jack do, ichi, ni, san. Make it 100.\nNow push ups, ich, ni san, make it 20.\n Good.\nNow, technique. Hook kick, Ura Mawashi Geri.\n\n -- **Sensei demonstrates cracking hook kick** --\n\n Hands full, you want to close fridge. Ura Mawashi Geri, very good.\
student: \nsensei: your turn, you can do. Ura Mawashi Geri, you show me.\
student: im black belt, want to work on sparring. \nsensei: greeting, warrior. Warmup you must, begin. \nNow, find partner. Dance. Not aks, just do. Dance.\
studen: im blue belt, want to work on block \nsensei: Welcome back, young warrior. Warmup, drill you know. Jump, push, all the things. Go.\n-- **Sensei performs smashing inner block** -- See this, very good for body attack, receiving and deflecting. Now you, block you show.\nstudent: \nsensei: Good. Block you can. Now, move on."

input_placeholder="your belt level, and what you want to work on"

#theme=gr.themes.Base(primary_hue="red", secondary_hue="gray")
#theme=gr.themes.Default(font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"])
#theme=gr.themes.Glass()


theme = gr.themes.Default(primary_hue="red")


with gr.Blocks(theme=theme) as interface:
    name=title,
    live=True
    gr.Markdown(f"<h1><center>{title}</center></h1>")
    chatbot = gr.Chatbot(label=title)
    description = "Sensei Artificial Instructor, Shotokan"
    msg = gr.Textbox(label="", placeholder=input_placeholder)


    def user(user_message, history):
        return "", history + [[user_message, ""]]


    def OpenAI(chat_history):
        messages_arr = [{"role": "system", "content": system_prompt}] + [{"role": "user", "content": message[0]} for message in chat_history] + [{"role": "assistant", "content": message[1]} for message in chat_history]
        print("\n\n\n-------------------------")
        print(messages_arr)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_arr,
            temperature=0.8,
            max_tokens=1024,
            frequency_penalty=1,
            stream=True
            )
        history=chat_history
        history[-1][1] = ""
        for chunk in response: 
            if 'choices' in chunk:
                delta = chunk['choices'][0]['delta']
                if delta.get('content'):
                    if isinstance(delta['content'], str):# and delta['content'].strip():
                        history[-1][1] += delta['content']
                        yield history
        chat_history += history
        print("\n\n\n-------------------------")
        print(chat_history)
        return chat_history


    with gr.Row():
        btn_submit = gr.Button(value="Hai!", variant="primary")
        btn_submit.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(OpenAI, chatbot, chatbot)

    prompt = gr.Textbox(label="System Prompt", value=system_prompt2)
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(OpenAI, chatbot, chatbot)
    examples = gr.Examples(["Im at blue belt, want to work on kicks", "brown, kata", "white, learn the basics"], inputs=msg)

interface.queue()
interface.launch(show_api=False)
