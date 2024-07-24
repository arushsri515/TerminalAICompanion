import speech_recognition as sr
import time
import os
from dotenv import load_dotenv
import google.generativeai as genai
import subprocess

load_dotenv()
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("For all following prompts, please only return the answer with no extra text, information, or warnings")
# response = model.generate_content("Write a prompt to create a new folder in the current directory named hello with no formatting")
# print(response.text)

r = sr.Recognizer()
mic = sr.Microphone()

# while True:

print("Listening...")

with mic as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    


words = r.recognize_google(audio)
print(words)
response = model.generate_content(f"Write a command line prompt to {words} with no markdown formatting and no extra text, information, breakdowns, or warnings except for the prompt")
result = response.text.replace('`','').strip()
print(result)
f = open("script.sh", "a")
f.write(result)
f.close()
promptList = result.split(' ')
print(promptList)
promptList = [term.replace('~/','') for term in promptList]
subprocess.run(promptList)
if promptList[0] != 'cd':
    file = open("script.sh", "r+")
    # Move the pointer (similar to a cursor in a text editor) to the end of the file
    file.seek(0, os.SEEK_END)

    # This code means the following code skips the very last character in the file -
    # i.e. in the case the last line is null we delete the last line
    # and the penultimate one
    pos = file.tell() - 1

    # Read each character in the file one at a time from the penultimate
    # character going backwards, searching for a newline character
    # If we find a new line, exit the search
    while pos > 0 and file.read(1) != "\n":
        pos -= 1
        file.seek(pos, os.SEEK_SET)

    # So long as we're not at the start of the file, delete all the characters ahead
    # of this position
    if pos > 0:
        file.seek(pos, os.SEEK_SET)
        file.truncate()
    file.close()

    # time.sleep(3)
