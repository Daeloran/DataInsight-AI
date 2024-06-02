import logging
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain

def interpret_data(formatted_data):
    logging.info("Interprétation des résultats par l'IA")
    llm = Ollama(model='llama3')
    chain = ConversationChain(llm=llm)

    # Question à l'agent IA
    question = (
        f"Voici les résultats de l'analyse des données :\n{formatted_data}\n"
        "Peux-tu les interpréter et me donner un résumé des points clés (en français), "
        "en structurant ta réponse de manière claire et concise ?"
    )
    response = chain.invoke(question)
    return response['response']
