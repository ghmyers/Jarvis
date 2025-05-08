"""
TITLE: LLM Agent
AUTHOR: Harrison Myers
DATE: 2025-05-08
DESCRIPTION: Builds LLM Agent wrapper (Jarvis) from OpenAI that integrates with Slack API.
"""

#!/usr/bin/env python3
import os, json, time
import sys
from openai import OpenAI

# Set project directory dynamically
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(PROJECT_DIR)


# Define subdirectories
DATA_DIR = os.path.join(PROJECT_DIR, 'data')

# Create LLM Agent
class JarvisLLMAgent:
    """
    Lightweight LLM wrapper that can:
      • classify intent
      • generate rich answers
      • call tools when pattern‑matched
    """
    def __init__(
        self,
        model="gpt-4o-mini",
        system_prompt="You are Jarvis, a helpful Slack assistant.",
        tools: dict | None = None,
    ):
        self.client = OpenAI()              
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tools or {}            

    # Intent classification
    def classify(self, text: str) -> str:
        msg = [
            {"role":"system", "content":"Return ONLY one intent label."},
            {"role":"user", "content":text},
        ]
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=msg,
            temperature=0
        )
        return resp.choices[0].message.content.strip()

    # Full conversation mode
    def run(self, text: str, channel: str) -> str:
        # (very bare‑bones: no memory, no threads)
        if any(k in text for k in self.tools):
            key = next(k for k in self.tools if k in text)
            return self.tools[key](channel)     # call your GIF helper
        msg=[{"role":"system","content":self.system_prompt},
             {"role":"user","content":text}]
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=msg,
            temperature=0.7,
            stream=False        # use stream=True for typing indicator
        )
        return resp.choices[0].message.content
