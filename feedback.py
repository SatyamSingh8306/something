from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import  PromptTemplate
from dotenv import load_dotenv
from feedbackFormat import create_feedback_schema
import os
load_dotenv()

recruiter_questions = [
        "How well did the candidate explain their previous project?",
        "How confident was the candidate during the interview?",
        "How would you rate the candidate's technical skills?"
    ]

   
DynamicFeedbackModel = create_feedback_schema(recruiter_questions)

model = ChatGroq(
    model=os.environ.get("MODEL_NAME")
)

model = model.with_structured_output(DynamicFeedbackModel)
