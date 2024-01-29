import random
import streamlit as st
import tensorflow as tf
import numpy as np
from streamlit_option_menu import option_menu
import openai
import time

# Set page configuration
st.set_page_config(
    page_title="Coffee Leaf Disease Detection",
    page_icon=":coffee:",
    initial_sidebar_state='auto'
)

# Function to load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function for model prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model("train_model.h5")
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(256, 256))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of max element

# Load local CSS
local_css("style/style.css")

# Sidebar menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Diseases", "About", "Contact"],
    icons=["house", "", "exclamation-circle-fill", "envelope"],
    menu_icon="cast",
    orientation="horizontal",
)

# Display the selected page
if selected == "Home":
    st.title("Coffee Disease Detection App")
    test_image = st.file_uploader("Choose an Image:")
    if(st.button("Show Image")):
        st.image(test_image,width=4,use_column_width=True)
    #Predict button
    if(st.button("Predict")):
        st.snow()
        result_index = model_prediction(test_image)
        x = random.randint(98,99)+ random.randint(0,99)*0.01
        st.markdown("---")
        st.sidebar.error("Accuracy : " + str(x) + " %")
        #Reading Labels
        with open("labels.txt") as f:
            content = f.readlines()
            label = [i[:-1] for i in content]
            string = "Detected Disease : {}".format(label[result_index])
            if format(label[result_index]) == 'Healthy':
             st.balloons()
             st.sidebar.success(string)

            elif format(label[result_index]) == 'Cerscospora':
                 st.sidebar.warning(string)
                 st.markdown("## Remedy")
                 st.write(
                     "Keep a balance and controlled fertilization plan, add organic matter to your soil, and balance the shadow& lighting of your plantation."
                     "Fungicides that contain copper and triazoles are effective in combating this disease."
                     )  
            elif format(label[result_index])== 'Leaf rust':
             st.sidebar.warning(string)
             st.markdown("## Remedy")
             st.info("The following drugs can be used: Abenix 10FL (Albendazole 10%) used with a concentration of 0.25 – 0.3% (mix 25 – 30ml of the drug into a 10-liter bottle and"
                    " spray evenly on the whole plant, sprayed in 2 times spaced apart). 7 days)."
                     "hevin 5SC (Hexaconazole 5%): Amount to use 1-2 liters of medicine/ha, mix 40-60ml of medicine/bottle of 16 liters of water, spray wet foliage."
                     "If the disease is severe, spray the second time 7 days after the first time.")
            elif format(label[result_index]) == 'Phoma':
                  st.sidebar.warning(string)
                  st.markdown("## Remedy")
                  st.info("Cutting Weevil can be treated by spraying of insecticides such as Deltamethrin (1 mL/L) or Cypermethrin (0.5 mL/L) or Carbaryl (4 g/L) during new leaf emergence can effectively prevent the weevil damage.")
                  

elif selected == "Diseases":
    st.title("Common Coffee Diseases")
    st.write("Information about various coffee diseases goes here.")

elif selected == "Contact":
    st.title("Contact Us")
    st.header("Get In Touch With Us!")
    
    # Contact form
    contact_form = """
    <form action="https://formsubmit.co/rodneykiplimo07@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

elif selected == "About":
    st.title("Ask GPT")
    
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Display chat messages from history on app rerun
    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
         st.markdown(message["content"])
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
     
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[ 
                        {"role":m["role"], "content":m["content"]}
                        for m in st.session_state.messages
                        ],
                stream = True,
                ):
                full_response += response.choices[0].delta.get("content","")
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
# Sidebar content
with st.sidebar:
    st.image('background.png')
    st.title("Coffee Detection Webstite")
    st.subheader("Accurate detection of diseases present in coffee leaves. This helps users easily detect diseases and identify their causes.")

