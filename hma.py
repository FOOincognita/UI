# Example: reuse your existing OpenAI setup
from openai import OpenAI

PORT = 1234
BIO_MODEL_NAME = "MaziyarPanahi/BioMistral-7B-GGUF/BioMistral-7B.Q8_0.gguf"
#!USER_MODEL_NAME = "TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/mixtral-8x7b-instruct-v0.1.Q6_K.gguf"
USER_MODEL_NAME = "Llama-3-8B-Instruct"


# Point to the local server
endpoint = OpenAI(base_url=f"http://localhost:{PORT}/v1", api_key="lm-studio")

bio_messages = [{"role": "system", "content": "Respond to the best of your ability."}]
user_messages = [{"role" : "system", "content": "You are communicating with both a user and a biomedical AI model. The user's messages will be prefaced with [USER] and the biomedical model's with [BIO]. If responding to the user requires any biomedical knowledge, ask the biomedical model by starting your message with [BIO]. YOU MUST NOT ANSWER BIOMEDICAL QUESTIONS. Instead, ask the biomedical model by prefixing a question with [BIO]. Once it responds, you may use the information it gives to respond to the user or ask it another question"}]

def get_bio_response(prompt, temperature=0.7):
    bio_messages.append({ "role": "user", "content": prompt})
    completion = endpoint.chat.completions.create(
        messages=bio_messages,
        temperature=temperature,
        model=BIO_MODEL_NAME,
        stream=True
    )
    
    print("[BIO] ", end="")
    
    msg = { "role": "assistant", "content": ""}
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            msg["content"] += chunk.choices[0].delta.content
    
    bio_messages.append(msg)
    print()
    print()

    return msg["content"]

def get_user_response(prompt, temperature=0.7):
    user_messages.append({ "role": "user", "content": prompt})
    completion = endpoint.chat.completions.create(
        messages=user_messages,
        temperature=temperature,
        model=USER_MODEL_NAME,
        stream=True
    )
    
    print("[USER] ", end="")
    
    msg = { "role": "assistant", "content": ""}
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            msg["content"] += chunk.choices[0].delta.content
    
    user_messages.append(msg)
    print()
    print()

    return msg["content"]

def runHMA():
    print("Enter q to quit when prompted for input")
    print()
    intro = print("[USER] Hello! I'm an assistant here to help answer any questions you might have. I can provide information on a wide range of topics, and if there's a question that requires specific biomedical knowledge, I can consult with a biomedical AI model to ensure you get the most accurate answer possible. How can I assist you today?")
    print()
    prompt = input("> ")
    print()

    while prompt != "q":
        response = get_user_response(prompt)
        
        print_response = True
        while len(response.split("[BIO]")) > 1:
            bio_response = "[BIO] " + get_bio_response(response.split("[BIO]")[1])
            response = get_user_response(bio_response)
        
        prompt = input("> ")