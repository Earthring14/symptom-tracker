import sys
import os
import datetime
from faster_whisper import WhisperModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import csv

template = """

You are the assistant of an accupuncturist.
Here is a transcript from their latest session: {transcript}

Your job is to split it into 3 fields, and structure your answer like this:
    Sypmtoms:
        - Symptom 1
        - Symptom 2
        etc.
        
    Treatment Plan:
        - Treatment Plan

    Needling points:
        - Point 1
        - Point 2
        etc.

DO NOT ADD OR MAKE UP FAKE OR EXTRA INFORMATION.
Just split the information, no extra comment.

Your answer:

"""

whisper_model = WhisperModel("base.en", compute_type="float32")
llama_model = OllamaLLM(model="llama3.2")

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llama_model

def transcribe(audiofile):
    segments, info = whisper_model.transcribe(audiofile)
    transcript = "".join([seg.text for seg in segments])
    return transcript

def extract_fields(transcript):
    result = chain.invoke({"transcript": transcript})
    return(result)


def format_record(info, patient_name, session_num):

    date = datetime.datetime.now().date()
    record = f"""
Patient name: {patient_name}
Date:  {date}

{info}

"""
    folder = "Records"
    os.makedirs(folder, exist_ok=True)

    filename = f"session{session_num}_record.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as file:
        file.write(record)

    return record
