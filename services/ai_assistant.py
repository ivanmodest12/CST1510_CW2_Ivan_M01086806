"""
AI Assistant Service Class
Provides AI-powered assistance for different domains
"""
import openai
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAssistant:
    """Provides AI-powered assistance across domains"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize AI Assistant with OpenAI API
        
        Args:
            api_key: OpenAI API key (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = """You are a helpful assistant for a Multi-Domain Intelligence Platform.
        You can assist with Cybersecurity, Data Science, IT Operations, and general questions.
        Provide concise, helpful responses."""
        
        if self.api_key:
            try:
                openai.api_key = self.api_key
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
    
    def set_system_prompt(self, prompt: str) -> None:
        """
        Set custom system prompt
        
        Args:
            prompt: New system prompt
        """
        self.system_prompt = prompt
    
    def send_message(self, message: str, domain: str = "general") -> str:
        """
        Send a message to the AI assistant
        
        Args:
            message: User message
            domain: Domain context (cybersecurity, datascience, itops, general)
            
        Returns:
            str: AI response
        """
        if not self.client:
            return "AI Assistant is not configured. Please set OPENAI_API_KEY in .env file."
        
        # Enhance prompt based on domain
        domain_prompts = {
            "cybersecurity": "You are a cybersecurity expert. Provide security advice, incident analysis, and best practices.",
            "datascience": "You are a data science expert. Help with data analysis, visualization, and machine learning questions.",
            "itops": "You are an IT operations expert. Assist with system administration, troubleshooting, and IT support.",
            "general": self.system_prompt
        }
        
        domain_prompt = domain_prompts.get(domain, self.system_prompt)
        
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": domain_prompt},
                *self.conversation_history[-10:],  # Last 10 messages for context
                {"role": "user", "content": message}
            ]
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"Error getting AI response: {str(e)}"
    
    def analyze_incident(self, incident_data: Dict[str, Any]) -> str:
        """
        Analyze a cybersecurity incident
        
        Args:
            incident_data: Dictionary with incident details
            
        Returns:
            str: AI analysis of the incident
        """
        if not self.client:
            return "AI Assistant not available for incident analysis."
        
        prompt = f"""Analyze this cybersecurity incident and provide recommendations:
        
        Incident Details:
        - Title: {incident_data.get('title', 'Unknown')}
        - Severity: {incident_data.get('severity', 'Unknown')}
        - Status: {incident_data.get('status', 'Unknown')}
        - Description: {incident_data.get('description', 'No description')}
        
        Provide:
        1. Risk assessment
        2. Immediate actions
        3. Long-term prevention strategies
        4. Compliance considerations"""
        
        return self.send_message(prompt, "cybersecurity")
    
    def analyze_dataset(self, dataset_data: Dict[str, Any]) -> str:
        """
        Provide insights on a dataset
        
        Args:
            dataset_data: Dictionary with dataset details
            
        Returns:
            str: AI analysis of the dataset
        """
        if not self.client:
            return "AI Assistant not available for dataset analysis."
        
        prompt = f"""Analyze this dataset and provide data science insights:
        
        Dataset Details:
        - Name: {dataset_data.get('name', 'Unknown')}
        - Category: {dataset_data.get('category', 'Unknown')}
        - Size: {dataset_data.get('size', 0)} bytes
        - Description: {dataset_data.get('description', 'No description')}
        
        Provide:
        1. Potential analysis approaches
        2. Visualization suggestions
        3. Machine learning use cases
        4. Data quality considerations"""
        
        return self.send_message(prompt, "datascience")
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get conversation history
        
        Returns:
            List[Dict]: Conversation history
        """
        return self.conversation_history