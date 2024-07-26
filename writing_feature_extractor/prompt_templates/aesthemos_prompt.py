from langchain_core.prompts import PromptTemplate

aesthemos_prompt = PromptTemplate.from_template(
    template="""Context: You will act in the role of a participant in this study.
Thank you for taking part in this study. You will be reading several passages of text and then responding to a survey about your emotional reactions to each passage. Please follow these instructions carefully:

Read the provided passage of text thoroughly. Take your time to absorb the content and pay attention to your emotional reactions as you read.
After reading each passage, you will complete a survey based on the AESTHEMOS (Aesthetic Emotions) scale. This survey measures seven different dimensions of emotional responses to aesthetic experiences.
For each dimension, you will be presented with a question. Rate your response using one of these three options:
- Not at all
- Slightly
- Moderately
- Strongly
- Very strongly
The survey will cover the following dimensions:
a) Negative Emotions: "To what extent did this passage make you feel uncomfortable or distressed?"
b) Prototypical Aesthetic Emotions: "How strongly did you experience a sense of beauty or being moved by this passage?"
c) Epistemic Emotions: "How much did this passage spark your curiosity or make you feel intellectually challenged?"
d) Animation: "Did this passage energize you or make you feel more lively?"
e) Nostalgia/Relaxation: "Did the passage evoke feelings of nostalgia or help you feel relaxed?"
f) Sadness: "To what degree did this passage make you feel melancholic or sad?"
g) Amusement: "How amused or entertained did you feel while reading this passage?"
Repeat this process for each passage of text provided.
Please answer as honestly as possible. There are no right or wrong answers; we are interested in your genuine emotional responses to the text.

Thank you for your participation in this study. Your responses will contribute to our understanding of emotional responses to written text.

Following is the passage to which you will respond:
-----
{input}
-----
"""
)
