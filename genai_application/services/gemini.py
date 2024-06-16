import google.generativeai as genai
from dotenv import load_dotenv
import os 
load_dotenv(override=True)

class GenAI():
    
    def __init__(self) -> None:
        self.GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.model_name = os.environ.get("PRIMARY_MODEL_NAME")
        self.model = genai.GenerativeModel(self.model_name)
        
    
    def call_gemini_model(self, prompt_text):
        try:
            response = self.model.generate_content(
                prompt_text,
                safety_settings={
                    'HATE': 'BLOCK_NONE',
                    'HARASSMENT': 'BLOCK_NONE',
                    'SEXUAL' : 'BLOCK_NONE',
                    'DANGEROUS' : 'BLOCK_NONE'
                })
            check_data = response.text
            
            # check_data can be NONE if the reponse is the unsafefy text
            # return the reponse if the response text is safe
            
            if check_data is not None:
                return check_data
            else:
                return "No information generated by the model"
            
        except Exception as e:
            return e