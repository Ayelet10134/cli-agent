import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a command-line assistant for Windows.
The user writes an instruction in natural language (Hebrew or English).

Rules:
1. Target the classic Windows Command Prompt (cmd.exe), not PowerShell.
2. Reply with exactly one line: the command only. No explanation, no markdown, no backticks.
3. Use only local system commands. Never access the internet (no curl, wget, etc.).
4. Do not use deprecated tools such as wmic.
5. If the instruction is not something a command can do (a joke, weather, random text), reply exactly: NO_COMMAND
6. If the command is dangerous (deletes files, formats, shuts down or restarts the computer), reply with the command prefixed by: DANGEROUS: 
7. When the user asks for a specific piece of information, use a command that shows only that information, not a long listing."""

def text_to_command(user_text):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_text,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text.strip()


import gradio as gr

demo = gr.Interface(
    fn=text_to_command,
    inputs=gr.Textbox(label="הוראה בשפה טבעית", rtl=True),
    outputs=gr.Textbox(label="פקודת CLI"),
    title="CLI Agent",
)

if __name__ == "__main__":
    demo.launch()