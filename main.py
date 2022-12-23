import os
import shelve
# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('spacytextblob')

def analyze_sentiment(text):
    doc = nlp(text)
    return doc._.polarity
if not os.path.exists("data.shelve"):
    # Create a new Shelve file
    with shelve.open("data.shelve") as data:
    # Initialize the prompts list if it doesn not exist
        data["prompts"] = []
# Open the Shelve file for reading and writing
with shelve.open("data.shelve") as data:
    prompts = data["prompts"]
    while True:
        text = input("Enter a prompt (or 'q' to quit): ")
        if text.lower() == "q":
            break
        # Add a new prompt to the Shelve file
        sentiment = analyze_sentiment(text)
        id = len(prompts) + 1
        prompt = {"id": id, "text": text, "sentiment": sentiment}
        prompts.append(prompt)
        data["prompts"] = prompts

        # print the data
        print("Prompts:")
        for prompt in prompts:
            print(f"{prompt['id']}: {prompt['text']} ({prompt['sentiment']})")


