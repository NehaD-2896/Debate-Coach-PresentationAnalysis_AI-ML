"""Groq-first structured LLM client with optional Gemini fallback.

The presentation module is intentionally provider-agnostic at the API boundary,
but Groq is the primary provider for the advanced implementation.
"""
from typing import TypeVar, Type
from pydantic import BaseModel
from app.config import settings

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    def __init__(self):
        self._groq = None
        self._gemini = None
        self.providers: list[str] = []
        if not settings.PRESENTATION_USE_LLM:
            return
        if settings.GROQ_API_KEY:
            try:
                from langchain_groq import ChatGroq
                self._groq = ChatGroq(
                    model=settings.GROQ_MODEL,
                    api_key=settings.GROQ_API_KEY,
                    temperature=0.15,
                )
                self.providers.append("groq")
            except Exception:
                self._groq = None
        if settings.GEMINI_API_KEY:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                self._gemini = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GEMINI_API_KEY,
                    temperature=0.15,
                )
                self.providers.append("gemini")
            except Exception:
                self._gemini = None

    @property
    def primary_provider(self) -> str | None:
        return self.providers[0] if self.providers else None

    @property
    def primary_model(self) -> str | None:
        if self.primary_provider == "groq":
            return settings.GROQ_MODEL
        if self.primary_provider == "gemini":
            return settings.GEMINI_MODEL
        return None

    async def structured(self, system_prompt: str, user_prompt: str, schema: Type[T]) -> T | None:
        for _name, client in (("groq", self._groq), ("gemini", self._gemini)):
            if client is None:
                continue
            try:
                chain = client.with_structured_output(schema)
                from langchain_core.prompts import ChatPromptTemplate
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("user", "{payload}"),
                ])
                return await (prompt | chain).ainvoke({"payload": user_prompt})
            except Exception:
                continue
        return None
