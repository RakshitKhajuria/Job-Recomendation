import streamlit as st
import pandas as pd
import base64,random
import time,datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymongo
client = pymongo.MongoClient("")
db = client.test
database = client["Job-Recomendation"]
collection = database["Resume_from_RESUME_ANALYZER"]
st.set_page_config(layout="wide", page_icon='logo/logo2.png', page_title="RESUME ANALYZER")

import plotly.express as px
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://www.linkpicture.com/q/logo_19.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "TALENT HIVE";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()

ds_course = [['Machine Learning Crash Course by Google [Free]', 'https://developers.google.com/machine-learning/crash-course'],
             ['Machine Learning A-Z by Udemy','https://www.udemy.com/course/machinelearning/'],
             ['Machine Learning by Andrew NG','https://www.coursera.org/learn/machine-learning'],
             ['Data Scientist Master Program of Simplilearn (IBM)','https://www.simplilearn.com/big-data-and-analytics/senior-data-scientist-masters-program-training'],
             ['Data Science Foundations: Fundamentals by LinkedIn','https://www.linkedin.com/learning/data-science-foundations-fundamentals-5'],
             ['Data Scientist with Python','https://www.datacamp.com/tracks/data-scientist-with-python'],
             ['Programming for Data Science with Python','https://www.udacity.com/course/programming-for-data-science-nanodegree--nd104'],
             ['Programming for Data Science with R','https://www.udacity.com/course/programming-for-data-science-nanodegree-with-R--nd118'],
             ['Introduction to Data Science','https://www.udacity.com/course/introduction-to-data-science--cd0017'],
             ['Intro to Machine Learning with TensorFlow','https://www.udacity.com/course/intro-to-machine-learning-with-tensorflow-nanodegree--nd230']]

web_course = [['Django Crash course [Free]','https://youtu.be/e1IyzVyrLSU'],
              ['Python and Django Full Stack Web Developer Bootcamp','https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp'],
              ['React Crash Course [Free]','https://youtu.be/Dorf8i6lCuk'],
              ['ReactJS Project Development Training','https://www.dotnettricks.com/training/masters-program/reactjs-certification-training'],
              ['Full Stack Web Developer - MEAN Stack','https://www.simplilearn.com/full-stack-web-developer-mean-stack-certification-training'],
              ['Node.js and Express.js [Free]','https://youtu.be/Oe421EPjeBE'],
              ['Flask: Develop Web Applications in Python','https://www.educative.io/courses/flask-develop-web-applications-in-python'],
              ['Full Stack Web Developer by Udacity','https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044'],
              ['Front End Web Developer by Udacity','https://www.udacity.com/course/front-end-web-developer-nanodegree--nd0011'],
              ['Become a React Developer by Udacity','https://www.udacity.com/course/react-nanodegree--nd019']]

android_course = [['Android Development for Beginners [Free]','https://youtu.be/fis26HvvDII'],
                  ['Android App Development Specialization','https://www.coursera.org/specializations/android-app-development'],
                  ['Associate Android Developer Certification','https://grow.google/androiddev/#?modal_active=none'],
                  ['Become an Android Kotlin Developer by Udacity','https://www.udacity.com/course/android-kotlin-developer-nanodegree--nd940'],
                  ['Android Basics by Google','https://www.udacity.com/course/android-basics-nanodegree-by-google--nd803'],
                  ['The Complete Android Developer Course','https://www.udemy.com/course/complete-android-n-developer-course/'],
                  ['Building an Android App with Architecture Components','https://www.linkedin.com/learning/building-an-android-app-with-architecture-components'],
                  ['Android App Development Masterclass using Kotlin','https://www.udemy.com/course/android-oreo-kotlin-app-masterclass/'],
                  ['Flutter & Dart - The Complete Flutter App Development Course','https://www.udemy.com/course/flutter-dart-the-complete-flutter-app-development-course/'],
                  ['Flutter App Development Course [Free]','https://youtu.be/rZLR5olMR64']]

ios_course = [['IOS App Development by LinkedIn','https://www.linkedin.com/learning/subscription/topics/ios'],
              ['iOS & Swift - The Complete iOS App Development Bootcamp','https://www.udemy.com/course/ios-13-app-development-bootcamp/'],
              ['Become an iOS Developer','https://www.udacity.com/course/ios-developer-nanodegree--nd003'],
              ['iOS App Development with Swift Specialization','https://www.coursera.org/specializations/app-development'],
              ['Mobile App Development with Swift','https://www.edx.org/professional-certificate/curtinx-mobile-app-development-with-swift'],
              ['Swift Course by LinkedIn','https://www.linkedin.com/learning/subscription/topics/swift-2'],
              ['Objective-C Crash Course for Swift Developers','https://www.udemy.com/course/objectivec/'],
              ['Learn Swift by Codecademy','https://www.codecademy.com/learn/learn-swift'],
              ['Swift Tutorial - Full Course for Beginners [Free]','https://youtu.be/comQ1-x2a1Q'],
              ['Learn Swift Fast - [Free]','https://youtu.be/FcsY1YPBwzQ']]
uiux_course = [['Google UX Design Professional Certificate','https://www.coursera.org/professional-certificates/google-ux-design'],
               ['UI / UX Design Specialization','https://www.coursera.org/specializations/ui-ux-design'],
               ['The Complete App Design Course - UX, UI and Design Thinking','https://www.udemy.com/course/the-complete-app-design-course-ux-and-ui-design/'],
               ['UX & Web Design Master Course: Strategy, Design, Development','https://www.udemy.com/course/ux-web-design-master-course-strategy-design-development/'],
               ['The Complete App Design Course - UX, UI and Design Thinking','https://www.udemy.com/course/the-complete-app-design-course-ux-and-ui-design/'],
               ['DESIGN RULES: Principles + Practices for Great UI Design','https://www.udemy.com/course/design-rules/'],
               ['Become a UX Designer by Udacity','https://www.udacity.com/course/ux-designer-nanodegree--nd578'],
               ['Adobe XD Tutorial: User Experience Design Course [Free]','https://youtu.be/68w2VwalD5w'],
               ['Adobe XD for Beginners [Free]','https://youtu.be/WEljsc2jorI'],
               ['Adobe XD in Simple Way','https://learnux.io/course/adobe-xd']]

hr_courses = [
    ['Human Resources Management: HR for People Managers', 'https://www.coursera.org/learn/hr-for-people-managers'],
    ['Human Resources Foundations', 'https://www.linkedin.com/learning/human-resources-foundations-2'],
    ['SHRM-CP/SCP Certification Prep', 'https://www.shrm.org/certification/preparation'],
    ['HR Analytics', 'https://www.udemy.com/course/hr-analytics-using-excel'],
    ['Effective Communication in the Workplace', 'https://www.edx.org/course/effective-communication-in-the-workplace']
]


def resume_store(data):
            collection.insert_one(data)
    
def show_pdf(file_path):
    
    encoded_pdf = base64.b64encode(file_path.read()).decode('utf-8')
    
    embed_code = f'<embed src="data:application/pdf;base64,{encoded_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(embed_code, unsafe_allow_html=True)
    return encoded_pdf

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    for page in PDFPage.get_pages(file,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
    text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text
def course_recommender(course_list):
    st.subheader("*Courses & Certificates🎓 Recommendations*")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course
def run():
        st.title("Resume Analyser")

        # st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Upload your resume, and get smart recommendation based on it."</h4>''',
        #             unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            count_=0

            encoded_pdf=show_pdf(pdf_file)
            resume_data = ResumeParser(pdf_file).get_extracted_data()

            resume_data["pdf_to_base64"]=encoded_pdf
            
            #resume_store(resume_data)
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(pdf_file)

                st.header("*Resume Analysis*")
                st.success("Hello "+ resume_data['name'])
                st.subheader("*Your Basic info*")
                try:
                    st.text('Name: '+resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: '+str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >=3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
                

                st.subheader("**Skills Recommendation💡**")
                ## Skill shows
                keywords = st_tags(label='### Skills that you have',
                text='See our skills recommendation',
                    value=resume_data['skills'],key = '1')

                ##  recommendation
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']
                hr_keywords =['psychology', 'human resources', 'sourcing', 'employee', 'recruitment', 'hiring', 'onboarding', 'orientation', 'training', 'development', 'performance management', 'compensation', 'benefits', 'employee relations', 'hr policies', 'legal compliance', 'conflict resolution', 'communication', 'interpersonal skills', 'organizational skills', 'data analysis', 'reporting', 'hris', 'time management', 'problem-solving', 'decision-making', 'recruitment', 'onboarding', 'employee relations', 'performance management', 'compensation and benefits', 'hr policies and procedures', 'legal compliance', 'training and development', 'organizational development', 'conflict resolution', 'data analysis', 'reporting', 'communication', 'interpersonal skills', 'time management', 'problem-solving', 'decision-making']

                blockchain_keywords = ['blockchain', 'smart contracts', 'decentralized applications', 'ethereum', 'solidity', 'hyperledger', 'distributed ledger technology', 'cryptocurrency', 'consensus algorithms', 'web3.js', 'ipfs', 'tokenization', 'node.js', 'truffle suite', 'ganache', 'remix ide', 'api development', 'cybersecurity', 'encryption', 'hashing', 'digital identity', 'scalability', 'performance optimization', 'full stack development']

                recommended_skills = []
                reco_field = ''
                rec_course = ''
                ## Courses recommendation
                for i in resume_data['skills']:
                    ## Data science recommendation
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '2')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(ds_course)
                        break

                    ## Web development recommendation
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '3')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(web_course)
                        break

                    ## Android App Development
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android App Development Jobs **")
                        recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '4')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(android_course)
                        break

                    ## IOS App Development
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                        recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '5')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(ios_course)
                        break

                    ## Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['Human Resources', 'Employee', 'Recruitment', 'Hiring', 'Onboarding', 'Orientation', 'Training', 'Development', 'Performance Management', 'Compensation', 'Benefits', 'Employee Relations', 'HR Policies', 'Legal Compliance', 'Conflict Resolution', 'Communication', 'Interpersonal Skills', 'Organizational Skills', 'Data Analysis', 'Reporting', 'HRIS', 'Time Management', 'Problem-Solving', 'Decision-Making']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '6')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(uiux_course)
                        break

                    elif i.lower() in hr_keywords:
                        print(i.lower())
                        reco_field = 'HR'
                        st.success("** Our analysis says you are looking for HR Jobs **")
                        recommended_skills = ['Psychology','UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research','Recruitment', 'Onboarding', 'Employee Relations', 'Performance Management', 'Compensation and Benefits', 'HR Policies and Procedures', 'Legal Compliance', 'Training and Development', 'Organizational Development', 'Conflict Resolution', 'Data Analysis', 'Reporting', 'Communication', 'Interpersonal Skills', 'Time Management', 'Problem-Solving', 'Decision-Making']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '6')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(hr_courses)
                        break

                ## Insert into table
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)
                st.write(timestamp)
                st.dataframe(resume_data)
                save={timestamp:resume_data}
                if count_==0:
                    count_=1
                    resume_store(save)

                ### Resume writing recommendation
                st.subheader("**Resume Tips & Ideas💡**")
                resume_score = 0
                if 'Objective' in resume_text:
                    resume_score = resume_score+20
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

                if 'Declaration'  in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration✍/h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',unsafe_allow_html=True)

                if 'Hobbies' or 'Interests'in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies⚽</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

                if 'Achievements' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements🏅 </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

                if 'Projects' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects👨‍💻 </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

                st.subheader("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score)+'**')
                st.warning("** Note: This score is calculated based on the content that you have added in your Resume. **")
                st.balloons()

                

            else:
                st.error("Wrong ID & Password Provided")

            st.balloons()           

# Set sidebar config
st.sidebar.title("About us")
st.sidebar.subheader("By")
text_string_variable1="Rakshit Khajuria - 19bec109"
url_string_variable1="https://www.linkedin.com/in/rakshit-khajuria/"
link = f'[{text_string_variable1}]({url_string_variable1})'
st.sidebar.markdown(link, unsafe_allow_html=True)

text_string_variable2="Prikshit Sharma - 19bec062"
url_string_variable2="https://www.linkedin.com/in/prikshit7766/"
link = f'[{text_string_variable2}]({url_string_variable2})'
st.sidebar.markdown(link, unsafe_allow_html=True)


run()

# # Take input as a PDF file
# pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# if pdf_file is not None:
#     # Convert PDF to base64
#     encoded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
#     st.write(encoded_pdf)

#     # Embed base64 PDF and display it in Streamlit
#     embed_code = f'<embed src="data:application/pdf;base64,{encoded_pdf}" width="700" height="1000" type="application/pdf">'
#     st.markdown(embed_code, unsafe_allow_html=True)