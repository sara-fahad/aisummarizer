import os
import openai
import streamlit as st

from PyPDF2 import PdfReader 
from dotenv import load_dotenv 

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def load_files():
    text = ""
    data_dir = os.path.join(os.getcwd(), "data")
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir, filename), "r") as f:
                text += f.read()
    return text     
                


def extract_text_from_pdf(pdf_file):
    #load pdf files and split it into pages
    reader = PdfReader(pdf_file)

    #extract text from pdf
    raw_text = ""
    
    for page in reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content

    return raw_text


def get_response(text):
    prompt = f"""
    You are an expert in summarizing text. You’ll be given a text delimited by four hashtags. 
    Make sure to capture the main points, key arguments, and any supporting evidence presented in the article. 
    Your summary should be informative and well-structured.

    text: ####{text}####
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
        ],
    )
    return response["choices"][0]["message"]["content"]



def main():

    # page configuration
    st.set_page_config(
        page_title="Summarizer",
        page_icon="📚",
    )

    # header 
    st.title("Summaprizer App")
    st.write("This app uses Artifiacial Intellegence to summarize a given text ot PDF file. ")
    st.divider()

    # check if the user wantsn to input text or upload a pdf
    option = st.radio("Select Input Type", ("Text", "PDF"))
    if option == "Text":
        #create a text area for the user to input text 
        user_input = st.text_area("Entre Text", "")

        #create a submit button
        if st.button("Submit") and user_input != "":
            # call the get_response function and display the response
            response = get_response(user_input)
            #display the summary
            st.subheader("Summary")
            st.markdown(f">{response}")
        else:
            st.error("Please entre text.")
    else:
        #create a file uploader to upload a pdf
        uploaded_file = st.file_uploader("Choose s PDF file", type="pdf")

        #create a submit button
        if st.button("Submit") and uploaded_file is not None:
            text = extract_text_from_pdf(uploaded_file)

            #call the get_response function and display the response
            response = get_response(text=text)
            st.subheader("Summary")
            st.markdown(f">{response}")

        else:
            st.error("Please entre PDF file.")


if __name__ == "__main__":
    main()