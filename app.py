import streamlit as st 
from pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os 

# Lets configure the model 
gemini_api_key=os.getenv('Google-API-Key1')
model=ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite',
                             api_key=gemini_api_key,
                             temperature=0.9,)


# Lets create the sidebar to uppload the resume 
st.sidebar.title(':orange[UPLOAD YOUR RESUME(ONLY PDF)]')
file=st.sidebar.file_uploader('Resume',type=['pdf'])
if file:
    file_text=text_extractor(file)
    st.sidebar.success('File Uploaded Successfuly')


# Create the main page of the application 
st.title(':blue[SKILL MATCH:-] :yellow[AI Assited Skill Matching Tool]',width='content')
st.markdown('#### :green[This Application will match and analyze your resume and the job description 📄]',width='content')
tips='''
Follow these steps:-
1. Upload your resume (PDF Only) in side bar.

2.Copy and paste the Job Description below.

3.Click on submit to run the application.
'''
st.write(tips)

job_desc=st.text_area(':red[Copy and paste your Job Description over here]',max_chars=50000)

if st.button('SUBMIT'):
    prompt=f'''
    <Role> You are an expert in analyzing the resume and matching it with job description.
    <Goal> Match the resume and job description provided by the applicant and create a report.
    <Context> The following content has been provided by the applicant:
    * Resume:{file_text}
    * Job Description:{job_desc}
    <Format> The report should follow these steps:
    * Give a brief description of the applicant in 3 to 5 lines.
    * Describe in percentage what are the chances of this resume getting selected.
    * Need not to be exact percentage , you can give interval of percentage.
    * Give the expected ATS Score along with matching and non matching keywords.
    * Perform SWOT Analaysis and explain each parameter ie strength, weakness, opportunity and threat.
    * Give what all section in the current resume that are required to be changed in order to improve the ATS Score and selection percentage.
    * Show both current version and improved version of the section in the resume.
    * Create two sample resume which can maximise the ATS Score and selection percentage.

    <Instruction>
    * Use bullet points to explaination wherever possible.
    * Create table for description wherever required.
    * Strictly do not add any new skill in sample resume.
    * The format of sample resumes should be in such a way that they can be coppied and pasted in word.
    '''

    response=model.invoke(prompt)
    st.write(response.content)