from google import genai
from google.genai import types
import json
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_story(topic: str):
    prompt = f"""
    Create an interactive choose-your-own-path story about {topic} for teenagers learning about financial literacy.

    Structure:
    - Start with an engaging scenario
    - Present 2-3 choices at key decision points
    - Each choice leads to different consequences and learning moments
    - End with a reflection on the choices made

    Format as JSON:
    {{
        "title": "Story title",
        "subtitle": "Brief description",
        "emoji": "��",
        "pages": [
            {{
                "id": "page_1",
                "title": "The Beginning",
                "content": "Story content with markdown...",
                "choices": [
                    {{
                        "text": "Choice A",
                        "next_page": "page_2a",
                        "consequence": "Brief consequence description"
                    }},
                    {{
                        "text": "Choice B", 
                        "next_page": "page_2b",
                        "consequence": "Brief consequence description"
                    }}
                ]
            }},
            {{
                "id": "page_2a",
                "title": "Consequence A",
                "content": "What happens after choice A...",
                "choices": [
                    {{
                        "text": "Continue",
                        "next_page": "page_3a"
                    }}
                ]
            }}
            // ... more pages
        ],
        "topics": ["{topic}"],
        "estimated_read_time": 10
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json", temperature=0.8
        ),
    )

    if response.text:
        return json.loads(response.text)


def generate_lesson(topic: str):
    prompt = f"""
    Create a multi-page educational lesson about {topic} for teenagers.

    Structure:
    - Introduction page
    - 2-4 content pages with different aspects of the topic
    - Interactive elements on each page
    - Summary/quiz page

    Format as JSON:
    {{
        "title": "Lesson title",
        "subtitle": "Brief description", 
        "emoji": "��",
        "pages": [
            {{
                "id": "intro",
                "title": "Introduction",
                "content": "Welcome to the lesson...",
                "type": "intro"
            }},
            {{
                "id": "page_1",
                "title": "Key Concept 1",
                "content": "Detailed explanation...",
                "type": "content",
                "interactive_elements": [
                    {{
                        "type": "quiz",
                        "question": "What is...?",
                        "options": ["A", "B", "C"],
                        "correct": 0
                    }}
                ]
            }},
            {{
                "id": "page_2", 
                "title": "Key Concept 2",
                "content": "More content...",
                "type": "content"
            }},
            {{
                "id": "summary",
                "title": "Summary",
                "content": "Let's review what we learned...",
                "type": "summary"
            }}
        ],
        "learning_objectives": ["Objective 1", "Objective 2"],
        "topics": ["{topic}"],
        "estimated_duration": 8
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json", temperature=0.7
        ),
    )

    if response.text:
        return json.loads(response.text)
