import re
import textstat


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


def combine_short_strings(strings: list[str], minimum_words=5) -> list[str]:
    i = 0
    while i < len(strings) - 1:
        if (len(strings[i].split()) < minimum_words) and (len(strings[i]) > 0):
            print(f"Combining [{strings[i]}] and [{strings[i + 1]}]")
            strings[i + 1] = strings[i] + " " + strings[i + 1]
            strings.pop(i)
        else:
            i += 1
    return strings


def get_text_statistics(text: str) -> dict[str]:
    text_statistics = dict()
    dialogue_percentage = calculate_dialogue_percentage(text)
    dp_as_string = f"{dialogue_percentage:.2f}%"
    text_statistics["dialogue_percentage"] = dp_as_string
    text_statistics["readability_ease"] = textstat.flesch_reading_ease(text)
    text_statistics["readability_grade"] = textstat.flesch_kincaid_grade(text)
    text_statistics["sentence_count"] = textstat.sentence_count(text)
    text_statistics["word_count"] = textstat.lexicon_count(text, removepunct=True)

    return text_statistics
