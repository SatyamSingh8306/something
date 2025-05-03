from pydantic import BaseModel, Field
from typing import List, Dict

class FeedBack(BaseModel):
    question: str = Field(..., description="The question asked by the recruiter")
    feedback: int = Field(..., gt=0, lt=10, description="Rate the user's answer out of 10")

class FeedBacks(BaseModel):
    feedbacks: List[FeedBack] = Field(..., description="List of feedbacks for multiple questions")


def create_feedback_schema(questions: List[str]) -> Dict:
    """
    Dynamically create a feedback schema based on the list of questions.
    """
    feedback_list = []
    for question in questions:
        feedback_data = {
            "question": question,
            "feedback": Field(..., gt=0, lt=10, description=f"Rate the user's answer out of 10 for this question: {question}")
        }
        feedback_list.append(feedback_data)
    
    # Create a dynamic Pydantic model
    DynamicFeedback = type("DynamicFeedback", (BaseModel,), {"__annotations__": {q: int for q in questions}})
    for q in questions:
        setattr(DynamicFeedback, q, Field(..., gt=0, lt=10, description=f"Rate the user's answer out of 10 for this question: {q}"))
    
    return DynamicFeedback

if __name__ == "__main__":
    
    recruiter_questions = [
        "How well did the candidate explain their previous project?",
        "How confident was the candidate during the interview?",
        "How would you rate the candidate's technical skills?"
    ]

   
    DynamicFeedbackModel = create_feedback_schema(recruiter_questions)

    
    input_data = {
        "How well did the candidate explain their previous project?": 8,
        "How confident was the candidate during the interview?": 7,
        "How would you rate the candidate's technical skills?": 9
    }

    
    try:
        validated_feedback = DynamicFeedbackModel(**input_data)
        print("Validated Feedback:", validated_feedback.dict())
    except Exception as e:
        print("Validation Error:", e)