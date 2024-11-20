from typing import Dict, Any
import random
from transformers import pipeline

class ChatbotResponseGenerator:
    def __init__(self):
        # Use a lightweight open-source language model
        self.generator = pipeline('text-generation', model='distilgpt2')

    def generate_response(
        self, 
        query: str, 
        context: str, 
        personality_config: Dict[float, Any]
    ) -> str:
        """
        Generate contextual response with personality
        
        :param query: User's input
        :param context: Semantic search context
        :param personality_config: Personality configuration dictionary
        :return: Generated response
        """
        # Adjust response based on personality configuration
        temperature = personality_config.get('creativity', 0.5)
        
        # Combine context and query
        prompt = f"Context: {context}\n\nQuery: {query}\n\nResponse:"
        
        # Generate response
        responses = self.generator(
            prompt, 
            max_length=150, 
            num_return_sequences=3,
            temperature=temperature
        )
        
        # Select most relevant response
        best_response = max(responses, key=lambda x: len(x['generated_text']))
        
        return best_response['generated_text'].split('Response:')[-1].strip()

    def adjust_tone(self, response: str, personality_config: Dict[float, Any]) -> str:
        """
        Fine-tune response tone based on personality configuration
        """
        friendliness = personality_config.get('friendliness', 0.5)
        formality = personality_config.get('formality', 0.5)
        
        tone_prefixes = {
            'friendly': ['Hey there!', 'Great question!', 'Sure thing!'],
            'formal': ['Certainly,', 'Allow me to explain,', 'I would like to clarify,']
        }
        
        # Select tone prefix based on personality
        if friendliness > 0.7:
            prefix = random.choice(tone_prefixes['friendly'])
        elif formality > 0.7:
            prefix = random.choice(tone_prefixes['formal'])
        else:
            prefix = ''
        
        return f"{prefix} {response}"
