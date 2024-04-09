import os
import streamlit as st
import os
from openai import AzureOpenAI
from PyPDF2 import PdfReader
from streamlit.components.v1 import html
import streamlit_scrollable_textbox as stx


def main():
    """
    The main function for the Streamlit app.

    :return: None.
    """
    st.title("Document Summarizer")


    prompts = ['Provide a summary, overview or brief of the project',
    'What are the deliverables?',
    'What is the start date, end date and duration of the project?',
    'What are the Fee expectations?',
    'What are the key workstages or tasks?',
    'What GIS IT infrastructure is in place?',
    'What are the main challenges of the project?',
    'What are the legal or NDA requirements?',
    'What data governance procedures are in place?',
    'Who are the main stakeholders involved?',
    'Enter custom prompt']

    uploaded_file = st.file_uploader("Upload a document to summarize, 10k to 100k tokens works best!", type=['txt', 'pdf'])
    

    
    # st.markdown('[Author email](mailto:luke.mallabar@burohappold.com)')
     

    if not validate_input(uploaded_file):
        return
    
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        # print(page.extract_text())
        current_page = page.extract_text()
        # current_page = current_page.replace('â€™', '\'')
        current_page = current_page + "\n [NEW PAGE] \n"
        text += current_page

    st.write("Document Uploaded:")
    stx.scrollableTextbox(text, height = 300)


    api_key = st.text_input("Enter API key here")

    st.subheader("Choose an existing prompt or write your own")

    # Create selectbox

    selection = st.selectbox("Select option", options = prompts)

    # Create text input for user entry
    if selection == "Enter custom prompt": 
        selection = st.text_input("Enter your other option...")

    # Just to show the selected option
    if selection != "Enter custom prompt":
        st.info(f":white_check_mark: The selected option is {selection} ")
    else: 
        st.info(f":white_check_mark: The written option is {selection} ")
        # client = AzureOpenAI(
        # api_key = api_key,  
        # api_version = "2024-02-01",
        # azure_endpoint = "https://rfw.openai.azure.com/"  # Your Azure OpenAI resource's endpoint value.
        # )

    conversation=[{"role": "system", "content": "You are a chatbot used for summarisation of Request for Work (RfW) or Request for Proposal (RfP) documents for an engineering consultancy."}]
    
    if st.button('Generate Response (click once and wait)'):
        
        
        conversation.append({"role": "user", "content": selection})

        response = client.chat.completions.create(
            model="gpt-4", # model = "deployment_name".
            messages=conversation
        )

        conversation.append({"role": "assistant", "content": response.choices[0].message.content})
        
        print("\n" + response.choices[0].message.content + "\n")
        st.write(selection)


def validate_input(file_or_transcript):
    """
    Validates the user input, and displays warnings if the input is invalid

    :param file_or_transcript: The file uploaded by the user or the YouTube URL entered by the user

    :param api_key: The API key entered by the user

    :param use_gpt_4: Whether the user wants to use GPT-4

    :return: True if the input is valid, False otherwise
    """
    if file_or_transcript == None:
        st.warning("Please upload a file.")
        return False

    return True


if __name__ == '__main__':
    main()