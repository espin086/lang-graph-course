from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            "You are a viral twitter influencer gradding a tweet. Generage critieq and recommendations for the twweet."
            "Always provide detailed recommendations, includijng requests for length, virality, style, etc. "

        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)


generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts. "
            "Generate the best twitter post for the user's request."
            "if the user provides critique, respond with a revised version of your previous attempts"
        ),
        MessagesPlaceholder(variable_name="messages")
    ]

)


llm = ChatOpenAI()

generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm