import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

ASSISTANT_ID = os.getenv("ASSISTANT_ID")

def get_asmr_idea(prompt):
    try:
        # Create a thread
        thread = client.beta.threads.create()

        # Add a message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
        )

        # Wait for the run to complete
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Get the last message from the thread
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        response = messages.data[0].content[0].text.value
        return json.loads(response)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    user_prompt = input("Enter your ASMR video idea prompt: ")
    if user_prompt:
        idea = get_asmr_idea(user_prompt)
        if idea:
            print(json.dumps(idea, indent=2, ensure_ascii=False))
