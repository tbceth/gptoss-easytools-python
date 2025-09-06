


"""
main.py
=======

Main entry point for running GPT OSS chat orchestration and tool calling.
"""
import os
from dotenv import load_dotenv
from services.chat_service import ChatService


def main():
    """
    Run a sample chat session using ChatService.
    """
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GPT_OSS_API_KEY")
    base_url = os.environ.get("GPT_OSS_BASE_URL", "http://localhost:8080/v1")
    model = os.environ.get("GPT_OSS_MODEL", "gpt-oss-20b")
    chat_service = ChatService(api_key=api_key, base_url=base_url, model=model)
    messages = [
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "What’s the weather in Calgary and then add 41.5 and 0.5?"}
    ]
    final_text = chat_service.chat_completion(messages)
    print(final_text)

if __name__ == "__main__":
    main()
