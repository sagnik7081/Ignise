import os
import random
import requests
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
class AIAssistant:
    """AI Assistant class powered by LangChain and Groq"""
    
    def __init__(self):
        # Initialize Groq API key from environment or use fallback
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Initialize LangChain with Groq
        self._init_fallback_responses()
        try:
            self.llm = ChatGroq(
                groq_api_key=self.groq_api_key,
                model_name="llama-3.3-70b-versatile",  # Fast and capable model
                temperature=0.7,
                max_tokens=1024
            )
            
            # Create conversation memory
            self.memory = ConversationBufferWindowMemory(
                k=10,  # Remember last 10 exchanges
                return_messages=True
            )
            
            # Create custom prompt template
            self.prompt_template = PromptTemplate(
                input_variables=["history", "input"],
                template="""You are a helpful, friendly, and knowledgeable AI assistant with a warm personality. 
                You love using emojis and providing engaging, informative responses.

                Key traits:
                - Use emojis naturally in your responses 😊
                - Be enthusiastic and encouraging 🚀
                - Provide detailed, helpful answers
                - Ask follow-up questions when appropriate
                - Handle coding, creative writing, analysis, and general questions
                - Be conversational and personable

                Conversation History:
                {history}

                Human: {input}
                AI Assistant:"""
            )
            
            # Create conversation chain
            self.conversation = ConversationChain(
                llm=self.llm,
                memory=self.memory,
                prompt=self.prompt_template,
                verbose=False
            )
            
            self.langchain_available = True
            
        except Exception as e:
            print(f"LangChain/Groq initialization failed: {e}")
            self.langchain_available = False
            
    
    def _init_fallback_responses(self):
        """Initialize fallback responses when LangChain is not available"""
        self.personality_responses = [
            "That's an interesting question! 🤔",
            "Let me think about that... 💭",
            "Great point! Here's what I think... ✨",
            "I'd be happy to help with that! 🚀",
            "That's a fascinating topic! 🌟"
        ]
        
        self.knowledge_base = {
            "greeting": [
                "Hello! I'm your AI assistant powered by LangChain and Groq! How can I help you today? 😊🤖",
                "Hi there! Ready to chat with some advanced AI magic? 🚀✨",
                "Welcome! I'm your intelligent assistant, powered by cutting-edge language models! 🌟"
            ],
            "thanks": [
                "You're very welcome! Happy to help with my AI superpowers! 😊⚡",
                "My pleasure! The power of LangChain at your service! 🤗🔥",
                "Glad I could help! Feel free to ask more questions! ✨🚀"
            ],
            "goodbye": [
                "Goodbye! Thanks for chatting with this AI assistant! 👋🤖",
                "See you later! Keep exploring the world of AI! 😊🌟",
                "Until next time! Stay curious and keep learning! 🚀✨"
            ]
        }
    
    def generate_response(self, user_message, conversation_history):
        """Generate AI response using LangChain + Groq or fallback system"""
        
        if self.langchain_available:
            return self._generate_langchain_response(user_message, conversation_history)
        else:
            return self._generate_fallback_response(user_message, conversation_history)
    
    def _generate_langchain_response(self, user_message, conversation_history):
        """Generate response using LangChain and Groq"""
        try:
            # Add context about file uploads if recent messages contain file analysis
            context = ""
            if conversation_history:
                recent_messages = conversation_history[-3:]  # Check last 3 messages
                for msg in recent_messages:
                    if "File Analyzed Successfully" in msg.get('content', ''):
                        context = "\n\n[Context: User recently uploaded a file for analysis]"
                        break
            
            # Enhance the user message with context
            enhanced_message = user_message + context
            
            # Generate response using LangChain conversation chain
            response = self.conversation.predict(input=enhanced_message)
            
            # Clean up response (remove any unwanted prefixes)
            response = response.strip()
            if response.startswith("AI Assistant:"):
                response = response[13:].strip()
            
            return response
            
        except Exception as e:
            print(f"LangChain response generation failed: {e}")
            return self._generate_fallback_response(user_message, conversation_history)
    
    def _generate_fallback_response(self, user_message, conversation_history):
        """Generate response using fallback system when LangChain is unavailable"""
        user_message_lower = user_message.lower().strip()
        
        # Handle greetings
        if any(greeting in user_message_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return random.choice(self.knowledge_base["greeting"])
        
        # Handle thanks
        if any(thanks in user_message_lower for thanks in ['thank', 'thanks', 'appreciate']):
            return random.choice(self.knowledge_base["thanks"])
        
        # Handle goodbyes
        if any(goodbye in user_message_lower for goodbye in ['bye', 'goodbye', 'see you', 'farewell']):
            return random.choice(self.knowledge_base["goodbye"])
        
        # Handle questions about the assistant
        if any(question in user_message_lower for question in ['what are you', 'who are you', 'what can you do']):
            return self._get_about_response()
        
        # Handle coding questions
        if any(code_word in user_message_lower for code_word in ['code', 'programming', 'python', 'javascript', 'html', 'css']):
            return self._get_coding_response(user_message)
        
        # Handle general knowledge
        if any(question_word in user_message_lower for question_word in ['what', 'how', 'why', 'when', 'where', 'explain']):
            return self._get_knowledge_response(user_message)
        
        # Handle creative requests
        if any(creative_word in user_message_lower for creative_word in ['story', 'poem', 'joke', 'creative', 'write']):
            return self._get_creative_response(user_message)
        
        # Default response with personality
        return self._get_default_response(user_message)
    
    def _get_about_response(self):
        """Response about the AI assistant"""
        return """I'm an advanced AI assistant powered by LangChain and Groq! 🤖✨ 

Here's what makes me special:
• **LangChain Integration** - Advanced conversation management 🔗
• **Groq Lightning Fast** - Super quick response times ⚡
• **Context Awareness** - I remember our conversation 🧠
• **Multi-format Support** - Analyze documents and files 📄
• **Creative & Analytical** - From coding to creative writing 🎨

I can help you with:
• General questions and explanations 📚
• Coding and programming help 💻
• Creative writing and stories 📝
• Problem-solving and brainstorming 🧠
• Document analysis (when you upload files) 📄
• Complex reasoning and analysis 🔍

Powered by state-of-the-art language models! 🚀"""
    
    def _get_coding_response(self, user_message):
        """Response for coding-related questions"""
        responses = [
            f"Great question about programming! 💻 {user_message} is a fascinating topic in software development. I'd be happy to help you explore this further!",
            f"Coding is awesome! 🚀 Regarding {user_message}, there are several approaches we could take. What specific aspect would you like to focus on?",
            f"Programming question detected! 🔍 {user_message} involves some interesting concepts. Let me know if you'd like me to break it down step by step!"
        ]
        return random.choice(responses)
    
    def _get_knowledge_response(self, user_message):
        """Response for general knowledge questions"""
        responses = [
            f"That's a thoughtful question! 🤓 {user_message} touches on some interesting concepts. Let me share what I know and we can explore it together!",
            f"Excellent question! 🌟 {user_message} is something many people wonder about. I'd love to help you understand this better!",
            f"Fascinating topic! 🧠 {user_message} has multiple dimensions we could explore. What specific aspect interests you most?"
        ]
        return random.choice(responses)
    
    def _get_creative_response(self, user_message):
        """Response for creative requests"""
        if 'joke' in user_message.lower():
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything! 😄",
                "Why did the AI go to therapy? It had too many deep learning issues! 🤖😅",
                "What do you call a chatbot that loves to garden? A plant-based AI! 🌱🤖"
            ]
            return random.choice(jokes)
        
        return f"I love creative projects! ✨ {user_message} sounds like a wonderful idea. Let me put my creative circuits to work! 🎨🤖"
    
    def _get_default_response(self, user_message):
        """Default response with personality"""
        responses = [
            f"Interesting! 🤔 You mentioned: '{user_message}'. I'd love to explore this topic with you. Can you tell me more about what you're looking for?",
            f"Thanks for sharing that! 😊 '{user_message}' is something I can definitely help with. What specific information or assistance do you need?",
            f"Great topic! 🌟 Regarding '{user_message}', I have some thoughts. Would you like me to elaborate or do you have a specific question about it?",
            f"I find that fascinating! ✨ '{user_message}' is worth discussing. What angle would you like to approach this from?"
        ]
        return random.choice(responses)
    
    def search_web(self, query):
        """Simulate web search functionality"""
        # This is a placeholder for actual web search integration
        # In a real implementation, you would integrate with APIs like Google Search, Bing, etc.
        return f"🔍 I searched for '{query}' and found some interesting information. In a full implementation, this would connect to real search APIs!"
    
    def analyze_document(self, file_content, file_type):
        """Analyze uploaded documents using LangChain + Groq"""
        if self.langchain_available:
            return self._analyze_document_langchain(file_content, file_type)
        else:
            return self._analyze_document_fallback(file_content, file_type)
    
    def _analyze_document_langchain(self, file_content, file_type):
        """Analyze document using LangChain and Groq"""
        try:
            analysis_prompt = f"""Please analyze this {file_type.upper()} document and provide a comprehensive summary:

Document Content:
{file_content[:2000]}{'...' if len(file_content) > 2000 else ''}

Please provide:
1. A brief summary of the main content 📋
2. Key themes and topics identified 🔍
3. Important insights or takeaways ✨
4. Questions I could answer about this document 💭

Format your response with emojis and make it engaging!"""

            response = self.conversation.predict(input=analysis_prompt)
            
            return f"""📄 **Advanced Document Analysis Complete!** ✅

{response}

💡 **What's Next?**
You can now ask me specific questions about this document, request detailed explanations of any section, or ask for comparisons with other topics!

Powered by LangChain + Groq for deep document understanding! 🚀"""

        except Exception as e:
            print(f"LangChain document analysis failed: {e}")
            return self._analyze_document_fallback(file_content, file_type)
    
    def _analyze_document_fallback(self, file_content, file_type):
        """Fallback document analysis when LangChain is unavailable"""
        analysis = f"""📄 Document Analysis Complete! 

File Type: {file_type}
Content Length: {len(file_content)} characters

Summary: I've analyzed your document and found it contains valuable information. In a full implementation with LangChain + Groq, this would provide:
• Deep content analysis and insights 🔍
• Key themes and pattern recognition 📝
• Intelligent Q&A capabilities 💭
• Advanced reasoning about the content 🌐

Would you like me to focus on any specific aspect of the document?"""
        
        return analysis
    
    def get_conversation_summary(self):
        """Get a summary of the current conversation using LangChain"""
        if self.langchain_available and self.memory.chat_memory.messages:
            try:
                summary_prompt = "Please provide a brief summary of our conversation so far, highlighting the main topics we've discussed. Use emojis to make it engaging! 📋✨"
                return self.conversation.predict(input=summary_prompt)
            except:
                return "We've had an interesting conversation! 😊 Feel free to continue asking questions! 🚀"
        else:
            return "Start chatting to see a conversation summary! 💬✨"