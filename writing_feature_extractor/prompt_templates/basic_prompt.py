from langchain_core.prompts import PromptTemplate

basic_prompt = PromptTemplate.from_template(
    template="""Extract features from the following creative writing:
-----
{input}
-----
"""
)
