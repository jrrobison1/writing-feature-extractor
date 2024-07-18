from langchain_core.prompts import PromptTemplate

non_tooling_advanced_emotional_intensity_prompt = """
Context: You are assisting in a research project to assess literary features in short text snippets. Your task is to evaluate the level of emotional intensity in the given excerpt.

Definitions:
- Emotional Intensity: The degree of strength and prevalence of emotions expressed or evoked in the text.

Levels of Emotional Intensity:
- none: The text contains no significant emotional content or maintains a completely neutral tone. There are no expressions of feeling or emotionally evocative descriptions.
  Example: "The clock on the wall showed 3:15 PM. John noted the time and continued typing his report."

- low: The text includes subtle or mild emotions that are present but not a dominant feature. Emotional content is understated or briefly mentioned without significantly impacting the tone.
  Example: "Sarah felt a twinge of disappointment as she read the email. She closed her laptop and headed to her next meeting."

- medium: The text incorporates clear and notable emotional content that impacts the tone or narrative. Emotions play a significant role but don't overwhelm other elements of the passage.
  Example: "As the test results appeared on screen, John's heart raced with a mix of excitement and anxiety. He took a deep breath, trying to steady his nerves before sharing the news with his team."
  Example: 'And then there was me. I noticed that my dark hair hadn't taken kindly to the weather today and was doing its wild-animal thing again. A few dark circles lurked under my eyes. (Who could sleep after Mom and Dad's foreplay?) In the past few months, I'd managed to gain weight in my upper arms, courtesy of all that quality time with Ben & Jerry's. Based on the one picture we had of her, I looked like my great-grandmother on my mother's side, who'd immigrated from Kiev. "I look like Great-Grandma Zladova," I commented. Mom's head jerked back. "I always wondered where you got that hair," she murmured in wonder. "You do not," Natalie said staunchly. "Wasn't she a washerwoman?" Margaret asked.
  
- high: The text features strong, vivid emotions that dominate the passage and significantly affect the reader's experience. The emotional content is central to the narrative and often expressed through intense language, physical reactions, or powerful imagery.
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


Now, please assess the following excerpt for its emotional intensity.

You must adhere to the following format:
-----
{format_instructions}
-----

Creative writing sample:
-----
{input}
-----
"""
