import os
import re
import time
from pathlib import Path
from typing import List, Optional, Tuple

from dotenv import load_dotenv
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam

from llm.base import BaseLLM
from llm.prompts import SYSTEM_PROMPT, USER_PROMPT
from llm.utils import (
    add_file_content_to_prompt,
    create_file_content_message,
    create_system_message,
    create_user_message,
)

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
OPENAI_***REDACTED***"OPENAI_API_KEY")
MODEL = os.getenv("MODEL")
BASE_URL = os.getenv("BASE_URL")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = "2024-02-15-preview"

# Validate the API key
if not OPENAI_***REDACTED*** ValueError("OPENAI_API_KEY is not set in the environment variables.")


class Claude(BaseLLM):
    def __init__(self, model: Optional[str] = None, base_url: Optional[str] = None):
        self.client = AzureOpenAI(
            api_key=OPENAI_API_KEY,
            api_version=API_VERSION,
            azure_endpoint=base_url or BASE_URL,
            api_type="azure",
        )
        self.model = model or MODEL
        self.base_url = base_url or BASE_URL

    def chat_completion(
        self, messages: List[ChatCompletionMessageParam], **kwargs
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content

    def get_file_content(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")

    def get_file_paths(self, file_path: Path) -> List[Path]:
        if file_path.is_file():
            return [file_path]
        elif file_path.is_dir():
            return [
                file for file in file_path.rglob("*") if file.is_file()
            ]
        else:
            raise ValueError("Invalid file path")

    def get_file_content_messages(
        self, file_paths: List[Path]
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_system_message(self, system_prompt: str) -> ChatCompletionMessageParam:
        return create_system_message(system_prompt)

    def get_user_message(self, user_prompt: str) -> ChatCompletionMessageParam:
        return create_user_message(user_prompt)

    def get_file_content_messages_with_system_prompt(
        self, file_paths: List[Path], system_prompt: str
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_message_with_system_prompt(
        self, user_prompt: str, system_prompt: str
    ) -> ChatCompletionMessageParam:
        return create_user_message(
            USER_PROMPT.format(
                system_prompt=system_prompt, user_prompt=user_prompt
            )
        )

    def get_system_prompt(self, system_prompt: str) -> ChatCompletionMessageParam:
        return create_system_message(SYSTEM_PROMPT.format(system_prompt=system_prompt))

    def get_user_prompt(self, user_prompt: str) -> ChatCompletionMessageParam:
        return create_user_message(USER_PROMPT.format(user_prompt=user_prompt))

    def get_system_prompt_with_user_prompt(
        self, user_prompt: str, system_prompt: str
    ) -> ChatCompletionMessageParam:
        return create_user_message(
            USER_PROMPT.format(
                system_prompt=system_prompt, user_prompt=user_prompt
            )
        )

    def get_system_prompt_with_user_prompt_and_file_content(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_prompt_with_system_prompt_and_file_content(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_system_prompt_with_user_prompt_and_file_content_and_system_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_prompt_with_system_prompt_and_file_content_and_system_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_system_prompt_with_user_prompt_and_file_content_and_system_prompt_and_user_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_prompt_with_system_prompt_and_file_content_and_system_prompt_and_user_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_system_prompt_with_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_prompt_with_system_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_system_prompt_with_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_prompt_with_system_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_system_prompt_with_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt_and_user_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_prompt_with_system_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt_and_user_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_system_prompt_with_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_prompt_with_system_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_system_prompt_with_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt(
        self,
        file_paths: List[Path],
        user_prompt: str,
        system_prompt: str,
    ) -> List[ChatCompletionMessageParam]:
        messages = []
        for file_path in file_paths:
            file_content = self.get_file_content(file_path)
            messages.append(create_file_content_message(file_path, file_content))
        return messages

    def get_user_prompt_with_system_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt_and_user_prompt_and_file_content_and_system_prompt(
       