from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model='mistral')

def parse_with_ollama(dom_chunks, parse_description, progress_percentage):
    prompt = ChatPromptTemplate.from_template(template)

    #first call prompt then to model
    chain = prompt | model

    parsed_results = []
    total_chunks = len(dom_chunks)
    #get all chunks from dom and parse
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {'dom_content' : chunk, 'parse_description' : parse_description})
        
        print(f'Parsed batch {i} of {total_chunks}')
        parsed_results.append(response)
        progress_percentage(int((i/total_chunks)*100))

    #join all results and separate with \n
    return('\n'.join(parsed_results))
