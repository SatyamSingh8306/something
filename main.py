from textEditing import loader,chaining
from resume_format import create_resume,load_json_data

if __name__ == "__main__":
    content = loader("./pdfs")
    print(content)
    result = chaining(text=content,
                    domain="machine learning",
                    job_title="AI Engineer",
                    job_description="You must know machine learning ,deep learning , rag ,ai ,cnn and neural networks along with profiency in Python , Java, Javascript")
    output_file = "AI_Enhanced_CV.json"
    with open(output_file, "w") as f:
        f.write(result.model_dump_json(indent=4))
    data = load_json_data(output_file)  
    # data = result.model_dump_json(indent=4)
    resume = create_resume(data)
    resume.save("./output/finalResume.docx")