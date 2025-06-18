import logging
from typing import AsyncGenerator

from httpx import AsyncClient

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_openai import ChatOpenAI

from backend.core.config import settings

logger = logging.getLogger(settings.NAME_LOGGER)


class AIService:
    """
    Сервис для взаимодействия с ИИ
    Функционал:
        - получение ответа от ИИ
        - хранение диалога в памяти (Redis)
    Тех. долг:
        - переписать с использованием langgraph для дальнейшей гибкости в настройке ИИ
        - добавить подгрузку промта из БД (PostgreSQL)
        - добавить RAG
    """
    def __init__(self):
        self.model = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY,
            http_async_client=AsyncClient(proxy=settings.PROXY_URL)
        )
        self.prompt = PromptTemplate(
            input_variables=["history", "context", "input"],
            template="""
                Ты — ассистент по семейным вопросам проекта СемьСов. 
                Отвечаешь по делу без лишних вступлений. 
                Свой ответ, в первую очередь, ориентируй на переданный контекст.
                
                Контекст:
                {context}
                
                История диалога:
                {history}
                
                Текущий запрос:
                {input}
                
                Ответ:
                """
        )
        self.llm_chain = LLMChain(
            llm=self.model,
            prompt=self.prompt,
            verbose=False
        )


    def _get_memory(self, user_id: int):
        return ConversationBufferMemory(
            memory_key="history",
            chat_memory=self.__get_history(user_id)
        )

    @staticmethod
    def __get_history(user_id: int):
        session_id = f"chat_session:{user_id}"
        return RedisChatMessageHistory(
            session_id=session_id,
            url=settings.redis_url,
            key_prefix="ai_assistant:",
            ttl=60 * 60 * 24 * 7  # 7 дней хранения
        )

    async def astream_response(
        self, user_id: int, query: str, formatted_context: str = None,
    ) -> AsyncGenerator[str, None]:
        try:
            memory = self._get_memory(user_id)
            query_dict = {
                "input": query,
                "context": formatted_context,
                "history": memory.load_memory_variables({})["history"]
            }
            logger.info(f"Начинаем стриминг ответа для запроса: {query}")
            output_text = ""
            async for chunk in self.llm_chain.astream(query_dict):
                text_chunk = chunk.get("text")
                if text_chunk:  # Пропускаем пустые куски
                    logger.debug(f"Получен чанк: {text_chunk[:50]}...")
                    yield text_chunk
                    output_text += text_chunk

            await memory.asave_context({"inputs": query}, {"output": output_text})
            logger.info("Стриминг ответа завершен, история чата сохранена")
        except Exception as e:
            logger.error(f"Ошибка при стриминге ответа: {e}")
            yield "Произошла ошибка при стриминге ответа."

    async def ainvoke_response(
        self, user_id: int, query: str, formatted_context: str = None,
    ) -> str:
        try:
            memory = self._get_memory(user_id)
            query_dict = {
                "input": query,
                "context": formatted_context,
                "history": memory.load_memory_variables({})["history"]
            }
            logger.info(f"Получение ответа для запроса: {query}")
            ai_response = await self.llm_chain.ainvoke(query_dict)
            output_text = ai_response.get("text")
            await memory.asave_context({"inputs": query}, {"output": output_text})
            logger.info(f"Ответ получен: {output_text}")
            return output_text
        except Exception as e:
            logger.error(f"Ошибка при получении ответа: {e}")
            return "Произошла ошибка при получении ответа."
