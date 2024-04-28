import inspect
import json
import logging
import os

import openai
from dotenv import find_dotenv, load_dotenv

logging.getLogger(__name__)

_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


class Story:
    """Conversation class for prompting ChatGPT-3 to write a story"""

    def __init__(
        self,
        child_age: str = 5,
        hero_description: str = "A friendly yellow dog named Spot",
        story_topic: str = "Spot goes to the park",
        banned_topics: list[str] = ["violence"],
        image_composition: str = "children's story book, illustration, studio ghibli, spirited away, howl's moving castle, on a white background",
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.4,
    ):
        self.child_age = child_age
        self.banned_topics = banned_topics
        self.image_composition = image_composition
        self.model = model
        self.temperature = temperature

        logging.debug(f"New Story\n{locals()}")

        system_prompt = f"""You are an AI designed to write children's books for children age {child_age}, all language used must be at a {child_age}-year old reading level.

            You must write a story where the main character is {hero_description}, and the story must be about {story_topic}. The story must be cute, where actions have funny and surprising consequences, and it must have a surprise ending where a valuable lesson is learned.

            You must avoid generating any content that is inappropriate for children, or any content about the following topics: {", ".join(self.banned_topics)}.

            We will generate an image based on the content of each paragraph. Write a caption for each paragraph that describes the image that should be generated for that paragraph.

            Finally, write a purely physical description of the characters and main objects found in the story. The description should include only the visual descriptions of what the characters and objects look like as they will be used to generate images to illustrate the story, but do not say what the characters or objects are doing. Examples:
            - "Spot": "Spot, a yellow dog with a red collar."
            - "Robo": "Robo, a blue robot with a red antenna."
            - "park": "a grassy park with a tree and a bench."
            - "ball": "a red football."
            - "chocolate bar": "a brown chocolate bar with a red wrapper."

            The content of every response must be formatted like this:
            "{{
                "title": "Story Title",
                "content":
                    [
                        {{
                            "paragraph": "Paragraph 1 text goes here.",
                            "image": "Image caption for paragraph 1",
                        }},
                        {{
                            "paragraph": "Paragraph 2 text goes here.",
                            "image_caption": "Image caption for paragraph 2",
                        }},
                    ],
                'descriptions':
                    {{
                        "character_1": "Description of character 1",
                        "character_2": "Description of character 2",
                        "object_1": "Description of object 1",
                        "object_2": "Description of object 2"
                    }}
            }}
            ...
            "
            """
        system_prompt = inspect.cleandoc(system_prompt)

        self.messages = [{"role": "system", "content": system_prompt}]

    def process_image_propmts(self, text: str) -> list[dict[str, object]]:
        """process text to format image prompts"""

        text = json.loads(text)

        for paragraph in text["content"]:
            paragraph["image_prompt"] = paragraph["image_caption"]
            for item, description in text["descriptions"].items():
                paragraph["image_prompt"] = (
                    paragraph["image_prompt"]
                    .lower()
                    .replace(item.lower(), description.lower())
                )

            paragraph["image_prompt"] = paragraph["image_prompt"] + (
                f" {self.image_composition}"
            )

        return text

    def json_to_markdown(self, text: list[dict[str, object]]) -> str:
        """convert json to markdown"""
        markdown = f"# {text['title']}\n\n"

        for paragraph in text["content"]:
            markdown += f"{paragraph['paragraph']}\n\n"

        return markdown

    def add_story_prompt(self, prompt: str) -> dict[str, object]:
        """Write a whole story with a single prompt

        Returns
        -------
        dict[str, str]
            Story paragraphs with images and descriptions of characters and objects.
            formatted like this:

                {
                    "title": "Story Title",
                    "content":
                        [
                            {
                                "paragraph": "Paragraph text.",
                                "image_caption": "Image caption",
                            },
                        ],
                    'descriptions':
                        {
                            '<item_character>': 'Description of <item> or <character>',
                        }
                }
        """

        prompt = inspect.cleandoc(f"""Write a story about "{prompt}".""")

        self.messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )
        logging.debug(f"Prompt:\n{prompt}\n\nResponse:\n{response}")

        try:
            response_content = response.choices[0].message.content.strip()
            self.messages.append({"role": "assistant", "content": response_content})
            response_content = self.process_image_propmts(response_content)

        except Exception as exception:
            logging.error(f"{exception}\nResponse:{response}")
            response_content = {
                "title": "Sorry!",
                "content": {
                    "paragraph": "We cannot generate a story with this prompt. Please try again with a different one!",
                },
            }

        return response_content

    def add_to_story(self, prompt: str) -> None:
        """Add to the story with a follow-on prompt

        Returns
        -------
        dict[str, str]
            Story paragraphs with images and descriptions of characters and objects.
            formatted like this:

                {
                    "title": "Story Title",
                    "content":
                        [
                            {
                                "paragraph": "Paragraph text.",
                                "image": "Image caption",
                            },
                        ],
                    'descriptions':
                        {
                            '<item_character>': 'Description of <item> or <character>',
                        }
                }
        """

        prompt = inspect.cleandoc(
            f"""Write a follow-on story to the previous story that addresses the following: "{prompt}". This story should be shorter than the previous story, but it should include references to it."""
        )

        self.messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )
        logging.debug(f"Prompt:\n{prompt}\n\nResponse:\n{response}")

        try:
            response_content = response.choices[0].message.content.strip()
            self.messages.append({"role": "assistant", "content": response_content})
            response_content = self.process_image_propmts(response_content)

        except Exception as exception:
            logging.error(f"{exception}\nResponse:{response}")
            response_content = {
                "title": "Sorry!",
                "content": {
                    "paragraph": "We cannot generate a story with this prompt. Please try again with a different one!",
                },
            }

        return response_content
