import openai
import os
from profanity_check import predict_prob

class OpenAICompletion:
  def __init__(self, 
              engine="babbage",
              temperature=0.77,
              max_tokens=50,
              top_p=0.95,
              best_of=3,
              frequency_penalty=0.7,
              presence_penalty=0.57):
    self.engine = engine
    self.temperature = temperature
    self.max_tokens = max_tokens
    self.top_p = top_p 
    self.best_of = best_of
    self.frequency_penalty = frequency_penalty
    self.presence_penalty = presence_penalty
    openai.api_key = # Add your API Key here

  def suggestions(self, prompt="two dogs playing in snow"):  
    """
    Split openai completion based on newlines and return list of strings 
    """
    response = openai.Completion.create(
      prompt=prompt,
      engine=self.engine,
      temperature=self.temperature,
      max_tokens=self.max_tokens,
      top_p=self.top_p,
      best_of=self.best_of,
      frequency_penalty=self.frequency_penalty,
      presence_penalty=self.presence_penalty
    )
    result = response["choices"][0]["text"].strip("\n")
    result = result.split(". ")
    result = [s.replace("\n", "") for s in result if len(s) > 10]
    return result
