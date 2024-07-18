from langchain_core.prompts import PromptTemplate

advanced_emotional_intensity_prompt = prompt_template = PromptTemplate.from_template(
    """
Context: You are assisting in a research project to assess literary features in short text snippets. Your task is to evaluate the level of emotional intensity in the given excerpt.

Definitions:
- Emotional Intensity: The degree of strength and prevalence of emotions expressed or evoked in the text.

Levels of Emotional Intensity:
- None: The text contains no significant emotional content or maintains a completely neutral tone. There are no expressions of feeling or emotionally evocative descriptions.
  Example: "The clock on the wall showed 3:15 PM. John noted the time and continued typing his report."

- Low: The text includes subtle or mild emotions that are present but not a dominant feature. Emotional content is understated or briefly mentioned without significantly impacting the tone.
  Example: "Sarah felt a twinge of disappointment as she read the email. She closed her laptop and headed to her next meeting."

- Medium: The text incorporates clear and notable emotional content that impacts the tone or narrative. Emotions play a significant role but don't overwhelm other elements of the passage.
  Example: "As the test results appeared on screen, John's heart raced with a mix of excitement and anxiety. He took a deep breath, trying to steady his nerves before sharing the news with his team."

- High: The text features strong, vivid emotions that dominate the passage and significantly affect the reader's experience. The emotional content is central to the narrative and often expressed through intense language, physical reactions, or powerful imagery.
  Example: "Sarah's world shattered as she read the letter. Her hands trembled uncontrollably, tears blurring her vision. A scream of anguish caught in her throat as the full weight of her loss crashed over her, leaving her gasping for air in a room that suddenly felt devoid of oxygen."

Instructions:
1. Read the provided excerpt carefully.
2. Identify emotional language, including:
   a) Direct statements of emotion (e.g., "She felt overwhelmed with joy")
   b) Descriptive language that implies emotions (e.g., "His hands trembled as he opened the letter")
   c) Dialogue or internal monologue expressing emotions
   d) Imagery or metaphors that evoke emotional responses
3. Consider the overall emotional impact and how it affects the tone of the passage.
4. Assess how the emotions might impact the reader's engagement with the text.
5. Determine the level of emotional intensity based on the definitions provided.


Now, please assess the following excerpt for its emotional intensity, in the provided format you must adhere to.
-----
{input}
"""
)
