""" Main module for the project"""

from dotenv import load_dotenv
import os
load_dotenv()


if __name__ == "__main__":
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  
    print(OPENAI_API_KEY)