import logging
from typing import AsyncGenerator

from httpx import AsyncClient
from langgraph.checkpoint.base import BaseCheckpointSaver

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
    def __init__(self, user_id: int):
        self.model = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY,
            http_async_client=AsyncClient(proxy=settings.PROXY_URL)
        )
        self.memory = self._get_memory(user_id)
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
        self, query: str, formatted_context: str = None,
    ) -> AsyncGenerator[str, None]:
        try:
            query_dict = {
                "input": query,
                "context": formatted_context,
                "history": self.memory.load_memory_variables({})["history"]
            }
            logger.info(f"Начинаем стриминг ответа для запроса: {query}")
            output_text = ""
            async for chunk in self.llm_chain.astream(query_dict):
                text_chunk = chunk.get("text")
                if text_chunk:  # Пропускаем пустые куски
                    logger.debug(f"Получен чанк: {text_chunk[:50]}...")
                    yield text_chunk
                    output_text += text_chunk

            await self.memory.asave_context({"inputs": query}, {"output": output_text})
            logger.info("Стриминг ответа завершен, история чата сохранена")
        except Exception as e:
            logger.error(f"Ошибка при стриминге ответа: {e}")
            yield "Произошла ошибка при стриминге ответа."


# # TODO Убрать потом, написал для тестирования сервиса
# if __name__ == "__main__":
#     async def main(q):
#         ai_chat = AIService(123)
#         response = ""
#         async for r in ai_chat.astream_response(q):
#             response += r
#         return response
#
#
#     import asyncio
#     from backend.core.log_settings import setup_logging
#     q_1 = "Меня зовут Владимир. Что ты умеешь?"
#     text = asyncio.run(main(q_1))
#     print(text)
#     q_2 = "Напомни, как меня зовут?"
#     text = asyncio.run(main(q_2))
#     print(text)
