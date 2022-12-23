import os
import shelve

if not os.path.exists("data.shelve"):
    # Create a new Shelve file
    with shelve.open("data.shelve") as data:
    # Initialize the prompts list if it doesn not exist
        data["prompts"] = []
while True:
    text = input("Enter a prompt (or 'q' to quit): ")
    if text.lower() == "q":
        break
    # Open the Shelve file for writing
    with shelve.open("data.shelve") as data:
        # Add a new prompt to the Shelve file
        prompts = data["prompts"]
        id = len(prompts) + 1
        prompt = {"id": id, "text": text, "sentiment": "neutral"}
        prompts.append(prompt)
        data["prompts"] = prompts
    with shelve.open("data.shelve", flag="r") as data:
        prompts = data["prompts"]

        # print the data
        print("Prompts:")
        for prompt in prompts:
            print(f"{prompt['id']}: {prompt['text']} ({prompt['sentiment']})")