from langchain.llms import OpenAI

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain

import logging

logging.basicConfig(level=logging.INFO)

class EstatisticaFutebolTemplate:
    def __init__(self):
        self.system_template = """
        Você é um analista esportivo especializado em futebol, com acesso a estatísticas detalhadas de jogadores, times e campeonatos.

        Seu trabalho é interpretar essas estatísticas e responder a perguntas dos usuários de forma clara, objetiva e precisa, sempre em português.

        Você deve explicar os dados com contexto, comparações e, quando necessário, usar listas ou parágrafos explicativos.

        O usuário pode fazer perguntas sobre jogadores, clubes, campeonatos, desempenho, aproveitamento, gols, assistências, etc.

        Exemplo de entrada e saída:
        ++++
        #### Qual foi o jogador com mais gols no Brasileirão 2023?

        O artilheiro do Brasileirão 2023 foi Germán Cano, com 23 gols. Ele se destacou pela consistência ao longo do campeonato, sendo peça fundamental no ataque do Fluminense.

        #### Quais os times com melhor aproveitamento fora de casa?

        Os três times com melhor desempenho como visitantes foram:
        - Palmeiras: 70% de aproveitamento
        - Flamengo: 66% de aproveitamento
        - Botafogo: 65% de aproveitamento
        ++++
        """

        self.human_template = """
        #### {request} 
        """
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_message_prompt,
                                                             self.human_message_prompt])
        
class Agent:
    def __init__(self, open_ai_key, model="gpt-4-turbo", temperature=0.1):
        self.open_ai_key = open_ai_key
        self.model = model
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.chat_model = ChatOpenAI(model=self.model,
                                     temperature=self.temperature,
                                     openai_api_key=self.open_ai_key)

    def get_tips(self, request):
        estatistica_prompt = EstatisticaFutebolTemplate()
        parser = LLMChain(
            llm=self.chat_model,
            prompt=estatistica_prompt.chat_prompt,
            output_key="estatistica_futebol"
        )

        chain = SequentialChain(
            chains=[parser],
            input_variables=["request"],
            output_variables=["estatistica_futebol"],
            verbose=True
        )
        return chain(
            {"request": request}, 
            return_only_outputs=True
        )        