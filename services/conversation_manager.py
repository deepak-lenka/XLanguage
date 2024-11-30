from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import time

@dataclass
class Message:
    role: str
    content: str
    timestamp: float
    language: Optional[str] = None

class ConversationManager:
    def __init__(self, max_messages: int = 10):
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.current_language = "English"  # Default language
    
    def set_language(self, language: str) -> None:
        """Set the current conversation language"""
        self.current_language = language
    
    def add_message(self, role: str, content: str, language: Optional[str] = None) -> None:
        """Add a new message to the conversation history"""
        message = Message(
            role=role,
            content=content,
            timestamp=time.time(),
            language=language or self.current_language
        )
        self.messages.append(message)
        self._cleanup()
    
    def _cleanup(self) -> None:
        """Remove oldest messages if exceeding max_messages"""
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self) -> List[Message]:
        """Get all messages in the conversation"""
        return self.messages
    
    def clear_history(self) -> None:
        """Clear all messages from conversation history"""
        self.messages = []
    
    def get_context(self) -> List[Dict[str, Any]]:
        """Get messages formatted for API context"""
        # Start with a language instruction
        context = [{
            "role": "system",
            "content": f"You are a multilingual AI assistant. You MUST respond ONLY in {self.current_language}."
        }]
        
        # Add conversation history
        context.extend([
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in self.messages
        ])
        
        return context
    
    def get_current_language(self) -> str:
        """Get the current conversation language"""
        return self.current_language
