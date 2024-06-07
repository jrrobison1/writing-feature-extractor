from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    template="""Extract features from the following creative writing:
-----
{input}
-----
"""
)
