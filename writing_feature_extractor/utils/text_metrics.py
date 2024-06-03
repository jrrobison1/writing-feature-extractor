import re


def calculate_dialogue_percentage(text):
    # Define a regex pattern to match dialogue enclosed in double quotation marks, including newlines
    dialogue_pattern = r'"[^"]*"'

    # Find all matches of the dialogue pattern in the text using re.DOTALL flag
    dialogues = re.findall(dialogue_pattern, text, re.DOTALL)

    # Calculate the total length of the dialogues
    dialogue_length = sum(len(dialogue) for dialogue in dialogues)

    # Calculate the total length of the text
    total_length = len(text)

    # Calculate the percentage of text that is within dialogue tags
    dialogue_percentage = (
        (dialogue_length / total_length) * 100 if total_length > 0 else 0
    )

    return dialogue_percentage
