from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import DirectoryLoader,PyMuPDFLoader
from responseFormat import Response

from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME")


def loader(file_path):
    loader =DirectoryLoader(
        path=file_path,
        glob="*.pdf",
        loader_cls = PyMuPDFLoader
    )
    docs = loader.load()
    content = ""
    for i,doc in enumerate(docs):
        content += doc.page_content 
    return content

def load_model(model_name=os.environ.get("MODEL_NAME")):
    model = ChatGroq(
        model=model_name,
        api_key= os.environ.get("GROQ_API_KEY")
    )
    model = model.with_structured_output(Response)
    return model

def chaining(text,domain,job_title,job_description):
    prompts = PromptTemplate(
        template="""You are an expert HR professional. Your task is to extract information from the given resume text and format it into a structured JSON object matching the following schema:
                Resume Text:{text}
                Domain:{domain}
                Job Title: {job_title}
                Job Description : {job_description}

                Instructions:
                1. Extract relevant information and map it to the appropriate fields in the schema.
                2. If a field cannot be filled directly from the text, infer its value based on context or leave it blank.
                3. Make sure that everything is written perfectly in english.
                4. Add sufficient project according to job title and job description.
                5. Make it ATS Friendly.
                6. make sure to return something with validation of it's type so that i don't get error
                """,
        input_variables=["text", "domain","job_title","job_description"],
    )
    
    model = load_model()
    parser = StrOutputParser()
    chain = prompts | model 
    result = chain.invoke({"text": text, "domain": domain,"job_title":job_title,"job_description":job_description})
    return result


if __name__ == "__main__":
    try:
        content = loader("./pdfs")
        print("Content:", content)

        result = chaining(text=content, 
                          domain="machine learning",
                          job_title="AI Engineer",
                          job_description="You must know machine learning ,deep learning , rag ,ai ,cnn and neural networks along with profiency in Python , Java, Javascript")
        print(type(result))
        # if not isinstance(result, Response):
        #     raise TypeError("Expected result to be an instance of Response.")

        # output_file = "ai_enchanced1.json"
        # with open(output_file, "w") as f:
        #     f.write(result.model_dump_json(indent=4))
        # print(f"Output written to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")