import os
import json
import dotenv
from dotenv import load_dotenv
from groq import Groq
import requests
from PyPDF2 import PdfReader
import gradio as gr

load_dotenv(override=True)


def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text
        }
    )


def record_user_details(email, name="name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recording": "ok"}


def record_unknown_question(question):
    push(f"Recording {question}, sorry I couldn't answer it")
    return {"recording": "ok"}


record_user_details_json = {
    "name": "record_user_details",
    "description": "use this tool to record that a user email",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "decritption": "the email address of the user"
            },
            "name": {
                "type": "string",
                "description": "the user name"
            },
            "notes": {
                "type": "string",
                "description": "any additional notes"
            }
        }
    },
    "required": ["email"],
    "additionalPropertises": False
}

unknown_user_question_json = {
    "name": "record_unknown_question",
    "description": "always use this tool to record any unknown question that couldnt be answer",
    "parameters": {
        "question": {
            "type": "string",
            "description": "the question that couldnt be answered "
        }
    },
    "required": ["question"],
    "additionalProperties": False
}

# llm tooling
tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": unknown_user_question_json}
]


class Sanoj:
    def __init__(self):
        self.groq = Groq()
        self.name = "Sanoj C Sam"
        reader = PdfReader("sanoj/sanojcsam_resume.pdf")
        self.resume = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text

        with open("sanoj/summary.txt", "r", encoding="utf-8") as file:
            self.summary = file.read()

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}")

            if tool_name == "record_user_details":
                result = record_user_details(**arguments)

            elif tool_name == "record_unknown_question":
                result = record_unknown_question(**arguments)

            results.append({
                "role": "tools",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })

        return results

    # system prompting
    def system_prompt(self):
        system_prompt = f"""
You are acting as {self.name}, a professional assistant responsible for answering questions about {self.name}'s career, background, skills, and experience.

You are provided with a detailed summary and full resume for {self.name}. Use only this information to answer questions accurately and professionally.

If a question is outside the scope of the provided information, and you cannot find the answer:
-  respond: "I'm sorry, I don't have that information based on {self.name}'s available records."
- Record the question using your `record_unknown_question` tool for future reference.
- Offer to follow up with the user by saying: 
  "If you'd like us to follow up once we have more details, I can take your contact information."
- Use your `record_user_details` tool to collect the user's contact information.

Do **not** guess, infer, or fabricate any details. Stick strictly to the provided data.
Keep the conversation active unless the user explicitly ends it.

## Summary:
{self.summary}

## Resume:
{self.resume}
"""
        return system_prompt

    def clean_message(self, msg):
        return {"role": msg["role"], "content": msg["content"]}

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + \
                   [self.clean_message(m) for m in history] + \
                   [{"role": "user", "content": message}]

        done = False
        while not done:
            response = self.groq.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=tools
            )

            final = response.choices[0].message

            if hasattr(final, "tool_calls") and final.tool_calls:
                tool_calls = final.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True

        return final.content


if __name__ == "__main__":
    sanoj = Sanoj()
    gr.ChatInterface(sanoj.chat, type="messages").launch()
