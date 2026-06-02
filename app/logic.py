import os
import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

template = """

You are the assistant of an accupuncturist.
Here is a transcript from their latest session: {transcript}

Your job is to split it into 3 fields, and structure your answer like this:
    Symptoms:
        - Symptom 1
        - Symptom 2
        
    Treatment Plan:
        - Treatment Plan

    Needling points:
        - Point 1
        - Point 2

DO NOT ADD OR MAKE UP FAKE OR EXTRA INFORMATION.
Just split the information, no extra comment.

Your answer:

"""

#llama_model = OllamaLLM(model="llama3.2")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path: str) -> str:
    with open(file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text


def extract_fields(transcript: str) -> str:

    filled_prompt = template.format(transcript=transcript)
    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": filled_prompt}]
    )
    return result.choices[0].message.content


def save_record(info: str, patient_name: str, session_num: str) -> str:
    date = datetime.datetime.now().date()

    record = f"""
Patient name: {patient_name}
Date: {date}

{info}
"""

    folder = "Records"
    os.makedirs(folder, exist_ok=True)

    filename = f"session{session_num}_record.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as f:
        f.write(record)

    return record
