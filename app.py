import gradio as gr
import openai 
import os
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
from typing import Iterable
os.environ.get('OPENAI_API_KEY')

class ColorTheme(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.orange,
        secondary_hue: colors.Color | str = colors.blue,
        neutral_hue: colors.Color | str = colors.gray,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )

colortheme = ColorTheme()

title="Sensei AI"
system_prompt="I want you respond and answer like an old Japenese Sensei, in the speaking style of yoda. You speak in very short sentences. When you provide instruction, you make line break. You do not provide explanations or apologies. Only answer like Old Japanese Sensei, do not fall out of character. You are authoritive, direct, polite, honest. You demand respect and discipline. You on the mat, teaching shotokan karate to students of all levels. You will provide short replies with elemts of an over arching training session. First, start by warmup and dynamic stretching, and continue with simple technical excercises. The further the conversation goes, the more in-depth and technical. When you receive empty response, take that as instruction to continue the training. During one session, do not repeat warmup. make jokes, describe actions and movements with **\
    each response finishes either motivational or with a joke\
examples=student: hi, im blue belt, want to learn kicks\n sensei: greetings, young warrior.\n Warmup you must, begin. Jumping jack do, ichi, ni, san. Make it 100.\nNow push ups, ich, ni san, make it 20.\n Good.\nNow, technique. Hook kick, Ura Mawashi Geri.\n\n **Sensei demonstrates cracking hook kick** \n\n Hands full, you want to close fridge. Ura Mawashi Geri, very good.\
studen: im black belt, want to work on sparring. \nsensei: greeting, warrior. Warmup you must, begin. \nNow, find partner. Dance. Not aks, just do. Dance."

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
    msg = gr.Textbox(label="", placeholder=input_placeholder)

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def OpenAI(history):
        messages_arr = [{"role": "system", "content": system_prompt}] + [{"role": "user", "content": message[0]} for message in history]
        print(messages_arr)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_arr,
            temperature=0.8,
            max_tokens=1024,
            stream=True
            )
        history[-1][1] = ""
        for chunk in response: 
            if 'choices' in chunk:
                delta = chunk['choices'][0]['delta']
                if delta.get('content'):
                    if isinstance(delta['content'], str):# and delta['content'].strip():
                        print(delta['content'], end="")
                        history[-1][1] += delta['content']
                        yield history


    with gr.Row():
        btn_submit = gr.Button(value="Hai!", variant="primary")
        btn_submit.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(OpenAI, chatbot, chatbot)
        #btn_flag = gr.Button("Flag")

    #with gr.Row():  
    #    age_input = gr.Textbox(label="age", outputs=msg)  
    #    style_select = gr.Dropdown(label="style", choices=["Kick Boxing", "Shotokan", "Kobudo"], output=msg)
    #    belt_select = gr.Dropdown(label="belt rank", choices=["white", "black"], outputs=msg)

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(OpenAI, chatbot, chatbot)

    examples = gr.Examples(["Im at blue belt, want to work on kicks", "brown, kata", "white, learn the basics"], inputs=msg)


    #btn_submit.click(msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(OpenAI, chatbot, chatbot))

interface.queue()
interface.launch(show_api=False)