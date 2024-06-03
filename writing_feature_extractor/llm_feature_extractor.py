import json
from langchain_groq import ChatGroq
import textstat
import pandas as pd
import matplotlib.pyplot as plt

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from structures import Features, Pace
from utils.text_metrics import calculate_dialogue_percentage


def get_number_for_pace(pace: Pace):
    if pace == Pace.VERY_SLOW:
        return 1
    if pace == Pace.SLOW:
        return 2
    if pace == Pace.MEDIUM_SLOW:
        return 3
    if pace == Pace.MEDIUM:
        return 4
    if pace == Pace.MEDIUM_FAST:
        return 5
    if pace == Pace.FAST:
        return 6
    if pace == Pace.VERY_FAST:
        return 7
    return 0


def get_graph(paragraph_numbers, pace_numbers, paragraphs):
    # Example data
    data = {
        "Paragraph": paragraph_numbers,
        # "Paragraph": [1, 2, 3, 4, 5, 6, 7],
        "Pacing": pace_numbers,
        # "Pacing": [1, 2, 3, 7, 2, 6, 4],
        "Text": paragraphs,
        # "Text": [
        #     "This is a short paragraph.",
        #     "This is a slightly longer paragraph with more words.",
        #     "This is the longest paragraph of all, with even more words than the previous one.",
        #     "Short again.",
        #     "More and more and more and More and more text",
        #     "Wow even more text here. Wow wow wow." "Moderate length paragraph here.",
        #     "Here's some more." "And here's lots and lots and lots and lots of words!",
        # ],
    }

    # Calculate the length of each paragraph
    df = pd.DataFrame(data)
    df["Length"] = df["Text"].apply(lambda x: len(x.split()))

    # Normalize lengths to fit a reasonable bar width range
    max_width = 0.4  # Maximum width of the bars
    min_width = 0.1  # Minimum width of the bars
    df["Width"] = (
        (df["Length"] - df["Length"].min()) / (df["Length"].max() - df["Length"].min())
    ) * (max_width - min_width) + min_width

    # Calculate positions
    positions = [sum(df["Width"][:i]) for i in range(len(df))]
    center_positions = [pos + df["Width"][i] / 2 for i, pos in enumerate(positions)]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot bars with varying widths and black borders
    for index, row in df.iterrows():
        ax.bar(
            positions[index],
            row["Pacing"],
            width=row["Width"],
            color="green",
            edgecolor="black",
            align="edge",
            hatch="//",
        )

    ax.set_xlabel("Paragraph")
    ax.set_ylabel("Pacing")
    ax.set_title("Pacing Changes Throughout the Chapter with Variable Widths")
    ax.set_xticks(center_positions)  # Center x-ticks under each bar
    ax.set_xticklabels(df["Paragraph"])  # Label x-axis with paragraph numbers
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7])
    ax.set_yticklabels(
        [
            "Very Slow",
            "Slow",
            "Medium-Slow",
            "Medium",
            "Medium-Fast",
            "Fast",
            "Very Fast",
        ]
    )  # Label y-axis with pacing categories

    # Turn off horizontal grid lines
    ax.yaxis.grid(False)

    plt.show()


filename = "Death_Drive_73.txt"
with open(filename) as f:
    file_text = f.read()
    f.close()

sections = file_text.split("***")

# def extract_features(text: str) -> dict[str, str]:
prompt_template = PromptTemplate.from_template(
    template="""Extract features from the following creative writing:
-----
{input}
-----
"""
)
# Run LLM to extract features from the text
# llm = ChatAnthropic(
#     model="claude-3-opus-20240229", temperature=0
# ).with_structured_output(Features)
# llm = ChatAnthropic(model_name="claude-3-sonnet-20240229", temperature=0).with_structured_output(Features)
# llm = ChatAnthropic(model_name="claude-3-haiku-20240307", temperature=0).with_structured_output(Features)
# llm = ChatVertexAI(model="gemini-1.5-pro-latest", temperature=0).with_structured_output(Features)
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
# llm = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(Features)
llm = ChatGroq(model_name="llama3-70b-8192", temperature=0).with_structured_output(
    Features
)
raw_data_sections = []
for section in sections:
    try:

        print(f"----------SECTION BEGIN----------")
        paragraph_metadata = []
        this_paragraph_pace_data = []
        paragraphs = section.split("\n")
        for paragraph in paragraphs:
            # if len(paragraph) < 10:
            #     paragraphs.remove(paragraph)
            #     continue
            result = llm.invoke(prompt_template.format(input=paragraph))
            dialogue_percentage = calculate_dialogue_percentage(paragraph)

            dp_as_string = f"{dialogue_percentage:.2f}%"
            as_dict = result.dict()
            as_dict["dialogue_percentage"] = dp_as_string
            as_dict["readability_ease"] = textstat.flesch_reading_ease(paragraph)
            as_dict["readability_grade"] = textstat.flesch_kincaid_grade(paragraph)
            as_dict["sentence_count"] = textstat.sentence_count(paragraph)
            as_dict["word_count"] = textstat.lexicon_count(paragraph, removepunct=True)

            paragraph_metadata.append(as_dict)
            this_paragraph_pace_data.append(get_number_for_pace(as_dict["pace"]))

            # print(json.dumps(as_dict, indent=2))

        for pm in paragraph_metadata:
            print(pm["pace"])
        paragraph_numbers = list(range(len(this_paragraph_pace_data)))

        try:
            get_graph(paragraph_numbers, this_paragraph_pace_data, paragraphs)
        except Exception as e:
            print(e)

        print(f"----------SECTION END----------\n\n")
    except Exception as e:
        print(e)
        continue
# result = llm.invoke(prompt_template.format(creative_writing))
