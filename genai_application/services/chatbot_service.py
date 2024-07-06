from utils.llm_model import LLMModel
import google.generativeai as genai
import google.generativeai as gemini_client
from dotenv import load_dotenv
import os 
load_dotenv(override=True)
class ChatBotService:
    
    def __init__(self):
        self.model = LLMModel().get_llm_model()

    def get_general_answer(self, user_query):
        prompt = f"""
        You are a e-commerce chatbot assistant, you must answer based on your user query
        User Query: "{user_query.question}"
        """
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings={
                    'HATE': 'BLOCK_NONE',
                    'HARASSMENT': 'BLOCK_NONE',
                    'SEXUAL': 'BLOCK_NONE',
                    'DANGEROUS': 'BLOCK_NONE'
                }
            )

            check_data = response.text            
            if check_data is not None:
                return check_data
            else:
                return "I am just a e-commerce chatbot assistant and I am still learning, please kindly lemme know if I can help you."
            
        except Exception as e:
            print("Error here: ", {e})
            return "I am just a e-commerce chatbot assistant and I am still learning, please kindly lemme know if I can help you."
    
    def check_user_intention(self, user_query):
        prompt = f"""
        Classify the following user query into one of these intents: recommendation, order, general. You must only classify the output only. no need to describe.
        User Query: "{user_query.question}"
        Intent:
        """
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings={
                    'HATE': 'BLOCK_NONE',
                    'HARASSMENT': 'BLOCK_NONE',
                    'SEXUAL': 'BLOCK_NONE',
                    'DANGEROUS': 'BLOCK_NONE'
                }
            )
            intent_response = response.text.strip()
            print(intent_response)
            intent = "general"

            if "recommendation" in intent_response:
                intent = "recommendation"
            elif "order" in intent_response:
                intent = "order"
            elif "general" in intent_response:
                intent = "general"
            return intent
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
        
    def extract_512_dimension_embedding(self, embedding_result):
        return embedding_result['embedding'][:512]
    
    def embedding_user_query(self, user_query):
        user_query = user_query.lower().replace(" ", "").strip()
        
        gemini_client.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        embedding_model_name = os.environ.get("EMBEDDING_MODEL")
        
        embedding_result = gemini_client.embed_content(
            model=embedding_model_name,
            content=user_query,
            task_type="retrieval_document"
        )
        
        embedding = self.extract_512_dimension_embedding(embedding_result)
        return [embedding]
