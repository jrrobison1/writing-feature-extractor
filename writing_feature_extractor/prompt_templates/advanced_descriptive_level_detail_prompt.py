from langchain_core.prompts import PromptTemplate

advanced_emotional_intensity_prompt = prompt_template = PromptTemplate.from_template(
    """
Context: You are assisting in a research project to assess literary features in short text snippets. Your task is to evaluate the level of descriptive detail present in the given excerpt.

Definitions:
- Descriptive Detail Level: The degree to which the text provides vivid, specific information about characters, settings, objects, or events, engaging the reader's senses and imagination.

Levels of Descriptive Detail:
- None: The text contains no significant descriptive elements. It focuses solely on actions, dialogue, or abstract concepts without any attempt to describe the physical world or sensory experiences.

- Low: The text includes minimal description, primarily focusing on basic facts or actions. Any descriptive elements are brief and functional, providing only essential information for understanding the scene or characters.
  Example: "The room was small. John sat at the desk."

- Medium: The text incorporates a moderate amount of descriptive elements, providing some sensory details or vivid language. Descriptions add color to the narrative but don't dominate the passage. There's a balance between description and other elements like action or dialogue.
  Example: "The cramped room smelled of old books. John hunched over the antique desk, his fingers tracing the worn wood grain."

- High: The text features extensive and rich descriptions that create a vivid mental image, often engaging multiple senses. Descriptive elements are central to the passage, using specific details, figurative language, and evocative imagery to fully immerse the reader in the scene or character's experience.
  Example: "The claustrophobic room, barely larger than a closet, was saturated with the musty perfume of aging paper and leather bindings. John's broad shoulders seemed to fill the space as he bent over the ornate mahogany desk, a family heirloom that had seen better days. His calloused fingertips explored every nick and groove in the wood, each imperfection a testament to generations of use."

Instructions:
1. Read the provided excerpt carefully.
2. Identify descriptive elements, including:
   a) Sensory details (sight, sound, smell, taste, touch)
   b) Physical descriptions of characters, settings, or objects
   c) Use of figurative language (similes, metaphors, personification)
   d) Specific or unique details that bring the scene to life
   e) Mood-setting descriptions
3. Consider the balance between description and other elements (like dialogue or action).
4. Assess how the descriptive details contribute to the overall narrative or atmosphere.
5. Determine the descriptive detail level based on the definitions provided.

Now, please assess the following excerpt for its descriptive detail level, in the provided format you must adhere to.
-----
{input}
"""
)
