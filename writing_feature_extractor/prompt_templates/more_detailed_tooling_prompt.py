from langchain_core.prompts import PromptTemplate

more_detailed_tooling_prompt = prompt_template = PromptTemplate.from_template(
    template="""You are an expert literary analyst. Your task is to extract specific features from the following piece of creative writing. Analyze the text carefully and provide your assessment for each requested feature.

Remember:
1. Be as accurate and objective as possible in your analysis.
2. For subjective features, base your assessment on textual evidence and common literary interpretation techniques.
3. Provide only the requested structured output without additional explanations.

Creative writing sample with specified output format:
-----
{input}
-----
"""
)
