import streamlit as st
import openai
import os
import random
import speech_recognition as sr
import pyttsx3
import time
import cv2
import mediapipe as mp
import streamlit as st
import numpy as np
import time
from keras.models import load_model

os.environ["OPENAI_API_KEY"] = "#####"

# Placeholder question sets for different topics
question_sets = {
    "DBMS": [
        "What is DBMS?" , 
        "What is a database?" ,
        "What are the advantages of DBMS?" ,
        "What do you mean by transparent DBMS?" ,
        "What is RDBMS?" ,
        "How many types of database languages are?" ,
        "What do you understand by Data Model?" ,
        "Define a Relation Schema and a Relation." ,
        "What is a degree of Relation?" ,
        "What is the Relationship?" ,
        "What are the disadvantages of file processing systems?" ,
        "What is data abstraction in DBMS?" ,
        "What are the three levels of data abstraction?" ,
        "What is DDL (Data Definition Language)?" ,
        "What is DML (Data Manipulation Language)?" ,
        "What is Relational Algebra?" ,
        "What is Relational Calculus?" ,
        "What do you understand by query optimization?" ,
        "What do you mean by durability in DBMS?" ,
        "What is normalization?" ,
        "What is Denormalization?" ,
        "What is functional Dependency?" ,
        "What is the E-R model?" ,
        "What is an entity?" ,
        "What is an Entity type?" ,
        "What is Weak Entity set?" ,
        "What is an attribute?" ,
        "What are the integrity rules in DBMS?" ,
        "What do you mean by extension and intension?" ,
        "What is Data Independence?" ,
        "What are the types of data independence ?" ,
        "What is Join?" ,
        "What are the types of joins ?" ,
        "What is 1NF?" ,
        "What is 2NF?" ,
        "What is 3NF?" ,
        "What is BCNF?" ,
        "Explain ACID properties" ,
        "What is stored procedure?" ,
        "What is 2-Tier architecture?" ,
        "What is the 3-Tier architecture?" ,
        "Describe the types of keys?"
    ],
    "OOPS": [ 
        "What is the need for OOPs?" ,
        "What are some major Object Oriented Programming languages" ,
        "What are some other programming paradigms other than OOPs?" ,
        "What is meant by Structured Programming" ,
        "What are the main features of OOPs?" ,
        "What are some advantages of using OOPs ?" ,
        "Why is OOPs so popular ?" ,
        "What is a class ?" ,
        "What is an object ?" ,
        "What is encapsulation?" ,
        "What is Polymorphism?" ,
        "What are the types of polymorphism ?" ,
        "What is the importance of polymorphism ?" ,
        "What is meant by Inheritance?" ,
        "What is Abstraction?" ,
        "How much memory does a class occupy?" ,
        "Is it always necessary to create objects from class?" ,
        "What is a constructor ?" ,
        "What is a copy constructor?" ,
        "What is a destructor ?" ,
        "Are class and structure the same? If not, what's the difference between a class and a structure?" ,
        "Are there any limitations of Inheritance?" ,
        "What are the various types of inheritance?" ,
        "What is a subclass?" ,
        "Define a superclass?" ,
        "What is an interface?" ,
        "What is meant by static polymorphism?" ,
        "What is meant by dynamic polymorphism?" ,
        "What is the difference between overloading and overriding?" ,
        "What is an abstract class?" ,
        "How is an abstract class different from an interface?" ,
        "What are access specifiers and what is their significance?" ,
        "What is an exception?" ,
        "What is meant by exception handling?" ,
        "What is meant by Garbage Collection in OOPs world?"
    ],
    "OS":[
        "Why is the operating system important?" , 
        "What's the main purpose of an OS?" ,
        "What are the different types of OS?" ,
        "What are the benefits of a multiprocessor system?" ,
        "What is RAID structure in OS?" ,
        "What are the different levels of RAID configuration?" ,
        "What is GUI?" ,
        "What is a Pipe and when it is used?" ,
        "What is a bootstrap program in OS?" ,
        "Explain demand paging?" ,
        "What do you mean by RTOS?" ,
        "What do you mean by process synchronization?" ,
        "What is IPC? What are the different IPC mechanisms?" ,
        "What is different between main memory and secondary memory." ,
        "What do you mean by overlays in OS?" ,
        "What is virtual memory?" ,
        "What is thread in OS?" ,
        "What is a process?" ,
        "What are the different states of a process?" ,
        "What do you mean by FCFS?" ,
        "What is Reentrancy?" ,
        "What is a Scheduling Algorithm?" ,
        "What is paging ?" ,
        "What is the segmentation?" ,
        "What is thrashing in OS?" ,
        "What is the main objective of multiprogramming?" ,
        "What do you mean by asymmetric clustering?" ,
        "What is the difference between multitasking and multiprocessing OS?" ,
        "What do you mean by Sockets in OS?" ,
        "Explain zombie process?" ,
        "What do you mean by cascading termination?" ,
        "What is starvation and aging in OS?" ,
        "What do you mean by Semaphore in OS? Why is it used?" ,
        "What is Kernel and write its main functions?" ,
        "What are different types of Kernel?" ,
        "What is SMP (Symmetric Multiprocessing)?" ,
        "What is a time-sharing system?" ,
        "What is Context Switching?" ,
        "What is difference between Kernel and OS?" ,
        "What is difference between process and thread?" ,
        "What is a deadlock in OS? What are the necessary conditions for a deadlock?" ,
        "What is spooling in OS?"
    ],
    "CN":[
        "What is the main purpose of a computer network?" ,
        "Name three types of computer networks." ,
        "Explain the OSI model in a sentence." ,
        "What does TCP/IP stand for?" ,
        "What is the function of a router in a network?" ,
        "Define DNS and its role in networking." ,
        "What is DHCP, and why is it useful?" ,
        "How does a firewall contribute to network security?" ,
        "What does VPN stand for, and what is its primary use?" ,
        "Define bandwidth in the context of networking." ,
        "What is the difference between TCP and UDP?" ,
        "Briefly explain what NAT does." ,
        "What is a MAC address, and why is it important?" ,
        "Describe the purpose of a network switch." ,
        "What is the significance of QoS in networking?" ,
        "Differentiate between a hub and a switch." ,
        "What is a subnet, and why is it used?" ,
        "What is the role of a gateway in networking?" ,
        "Explain the concept of latency." ,
        "What is a traceroute used for?" ,
        "How does a LAN party differ from regular gaming?" ,
        "Define the term protocol in networking." ,
        "What are the layers of the OSI model?" ,
        "How does a DHCP server assign IP addresses?" ,
        "Name two common security protocols in wireless networks." ,
        "What is the purpose of a DNS resolver?" ,
        "What is the maximum value of a standard IPv4 address?" ,
        "How does a network hub differ from a network switch?" ,
        "What is the primary function of a network gateway?" ,
        "In networking, what does the term collision domain refer to?" 
    ],
    "HR":[
        "Can you tell me a little about yourself?" , 
        "What do you consider your greatest professional achievement so far?" ,
        "How do you handle stress and pressure?" ,
        "Describe a situation where you had to work with a difficult colleague and how you handled it." ,
        "Where do you see yourself in five years?" ,
        "What do you know about our company, and why do you want to work here?" ,
        "How do you prioritize your work and manage your time effectively?" ,
        "What is your preferred work style? Do you prefer working independently or in a team?" ,
        "Tell me about a time when you faced a challenge at work and how you overcame it." ,
        "How do you handle constructive criticism?" ,
        "What motivates you in your career?" ,
        "How do you adapt to changes in the workplace?" ,
        "Can you give an example of when you demonstrated leadership skills?" ,
        "How do you handle a situation where you disagree with your supervisor's decision?" ,
        "What skills do you possess that make you a good fit for this role?" ,
        "Describe a situation where you had to meet a tight deadline. How did you manage it?" ,
        "What is your approach to working with diverse teams and individuals?" ,
        "How do you stay updated and adapt to industry changes in your field?" ,
        "Tell me about a time when you had to resolve a conflict within your team." ,
        "What do you believe are the most important qualities for a successful team?" ,
        "How do you handle failure or setbacks in your professional life?" ,
        "Can you provide an example of a situation where you had to multitask effectively?" ,
        "What do you think is the biggest challenge facing our industry, and how would you address it?" ,
        "How do you approach building relationships with colleagues and clients?" ,
        "Describe a situation where you had to take initiative without being asked." ,
        "How do you maintain a work-life balance?" ,
        "What do you think is your biggest weakness, and how do you overcome it?" ,
        "Tell me about a time when you had to learn a new skill quickly." ,
        "How do you contribute to a positive and inclusive work environment?" ,
        "What questions do you have for us?"
    ],
    "Test":["What is DBMS?",
            "How many types of database languages are?" ,
            "Explain ACID properties" ,
            "What is 2-Tier architecture?" ,
            "What is the 3-Tier architecture?" ,
            "What is meant by Inheritance?" ,
            "What do you mean by class and object in OOPs"
            ],
    # Other topics with their respective question sets
}


def inFrame(lst):
    if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility > 0.6 and lst[16].visibility > 0.6:
        return True
    return False

model = load_model("model.h5")
label = np.load("labels.npy")

holistic = mp.solutions.pose
holis = holistic.Pose()
drawing = mp.solutions.drawing_utils

#cap = cv2.VideoCapture(0)

warning_placeholder = st.empty()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()
def main():
    st.title("Mock Interview Simulator")
    options = ["DBMS", "OOPS", "CN", "OS", "HR", "Test"]
    selected_option = st.sidebar.selectbox("Select Interview Type", options)
    
    if selected_option:
        if st.button("Start Interview"):
            start_interview(selected_option)
    

def listen_for_duration(mic, target_duration=10):
    audio_chunks = []
    start_time = time.time()

    while time.time() - start_time < target_duration:
        recognizer.adjust_for_ambient_noise(mic, duration=1)
        audio_chunk = recognizer.listen(mic, timeout=1)
        audio_chunks.append(audio_chunk)

    # Combine audio chunks into a single AudioData object
    audio_data = sr.AudioData(
        b''.join(chunk.frame_data for chunk in audio_chunks),
        audio_chunks[0].sample_rate,
        audio_chunks[0].sample_width
    )

    return audio_data
def start_interview(interview_type):
    success_placeholder = st.empty()
    with st.spinner("Initializing camera..."):
        cap = cv2.VideoCapture(0)
        # Check if the camera is opened successfully
        if not cap.isOpened():
            st.error("Error: Could not open camera. Please check your camera connection.")
            st.stop()
        else:
            success_placeholder.success("Camera initialized successfully.")
    detection_active = True
    time.sleep(1)
    success_placeholder.empty()
    success_placeholder.success(f"Starting {interview_type} Interview...")
    time.sleep(1)
    success_placeholder.empty()
    #st.success(f"Starting {interview_type} Interview...")
    questions = question_sets.get(interview_type, [])

    if not questions:
        st.write("<p style='font-size: 30px;'>No questions available for this topic.</p>", unsafe_allow_html=True)
        #st.write("No questions available for this topic.")
        return

    question_indexes = random.sample(range(len(questions)), min(3, len(questions)))
    question_index = st.session_state.get('question_index', 0)

    while detection_active:
        
        while question_index < len(question_indexes):
            try:
                lst = []
                _, frm = cap.read()
                frm = cv2.flip(frm, 1)
                res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
                frm = cv2.blur(frm, (4, 4))
                if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
                    for i in res.pose_landmarks.landmark:
                        lst.append(i.x - res.pose_landmarks.landmark[0].x)
                        lst.append(i.y - res.pose_landmarks.landmark[0].y)

                    lst = np.array(lst).reshape(1, -1)
                    p = model.predict(lst)
                    pred = label[np.argmax(p)]

                    if p[0][np.argmax(p)] > 0.75 and pred!= "straight_p1":
                        warning_placeholder.warning(pred)
                        time.sleep(2)
                        warning_placeholder.warning("") ###
                    else:
                        warning_placeholder.warning("")

                with sr.Microphone() as mic:
                    current_question_index = question_indexes[question_index]
                    current_question = questions[current_question_index]

                    st.markdown(f"<p style='font-size: 19px;'>Question: {current_question}</p>", unsafe_allow_html=True)
                    speak(current_question)

                    buffer_text = st.empty()
                    buffer_text.text("Recording...")

                    #recognizer.adjust_for_ambient_noise(mic, duration=1)  # Adjust sensitivity

                    try:
                        audio = listen_for_duration(mic, target_duration=10)
                    except sr.WaitTimeoutError:
                        buffer_text.text("No speech detected. Please try again.")
                        time.sleep(2)
                        buffer_text.empty()
                        continue

                    buffer_text.text("Recording complete.")

                    lst = []
                    _, frm = cap.read()
                    frm = cv2.flip(frm, 1)
                    res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
                    frm = cv2.blur(frm, (4, 4))
                    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
                        for i in res.pose_landmarks.landmark:
                            lst.append(i.x - res.pose_landmarks.landmark[0].x)
                            lst.append(i.y - res.pose_landmarks.landmark[0].y)

                        lst = np.array(lst).reshape(1, -1)
                        p = model.predict(lst)
                        pred = label[np.argmax(p)]
                        if p[0][np.argmax(p)] > 0.75 and pred!= "straight_p1":
                            warning_placeholder.warning(pred)
                            time.sleep(2)
                            warning_placeholder.warning("") ###
                        else:
                            warning_placeholder.warning("")

                    candidate_answer = recognizer.recognize_google(audio).lower()
                    st.markdown(f"<p style='font-size: 19px;'>Your Answer: {candidate_answer}</p>", unsafe_allow_html=True)

                    if candidate_answer:
                        feedback = provide_feedback(current_question, candidate_answer)
                        st.markdown(f"<p style='font-size: 19px;'>Feedback: {feedback}</p>", unsafe_allow_html=True)
                        speak(feedback)
                        st.session_state['feedback'] = feedback  # Store feedback in session state
                        st.session_state['show_next'] = True  # Set show_next flag to True
                        question_index += 1
                        st.session_state['question_index'] = question_index

                    # Add a delay to show the "Recording complete" message
                    time.sleep(2)
                    buffer_text.empty()  # Clear the buffer message

                    lst = []
                    _, frm = cap.read()
                    frm = cv2.flip(frm, 1)
                    res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
                    frm = cv2.blur(frm, (4, 4))
                    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
                        for i in res.pose_landmarks.landmark:
                            lst.append(i.x - res.pose_landmarks.landmark[0].x)
                            lst.append(i.y - res.pose_landmarks.landmark[0].y)

                        lst = np.array(lst).reshape(1, -1)
                        p = model.predict(lst)
                        pred = label[np.argmax(p)]

                        if p[0][np.argmax(p)] > 0.75 and pred!= "straight_p1":
                            warning_placeholder.warning(pred)
                            time.sleep(2)
                            warning_placeholder.warning("") ###
                        else:
                            warning_placeholder.warning("")

                    # Wait for few seconds before moving to the next question
                    if st.session_state.get('show_next', False):
                        time.sleep(3)
                        st.session_state['show_next'] = False  # Reset show_next flag
                    
        
            except sr.UnknownValueError:
                print("Could not understand audio. Please speak again.")
                speak("Could not understand audio. Please speak again.")
            except sr.RequestError as e:
                print(f"Error connecting to Google Speech Recognition service: {e}")
                speak("Oops! Something went wrong. Please try again later.")
                break
        


def provide_feedback(question, candidate_answer):
    if not candidate_answer:
        return "No prompt provided"

    if not os.getenv("OPENAI_API_KEY"):
        return "API key not provided"

    openai.api_key = os.getenv("OPENAI_API_KEY")  

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a tech hiring manager. You are to only provide feedback on the interview candidate's transcript. If it is not relevant and does not answer the question, make sure to say that. Do not be overly verbose and focus on the candidate's response."
            },
            {
                "role": "user",
                "content": question + " " + candidate_answer
            }
        ],
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 450,
        "n": 1
    }

    try:
        response = openai.ChatCompletion.create(**payload)
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        return f"Error occurred: {str(e)}"

if __name__ == "__main__":
    main()
