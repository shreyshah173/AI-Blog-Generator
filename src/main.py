import os
import json
import streamlit as st
from groq import Groq
from groq import BadRequestError

# Streamlit page configuration
st.set_page_config(
    page_title="Groq Blog Generator",
    layout="centered"
)

# Define working directory and load config
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(os.path.join(working_dir, "config.json")))

# Set the Groq API key
groq_api_key = config_data["Groq_API_KEY"]
os.environ["GROQ_API_KEY"] = groq_api_key

# Initialize Groq client
client = Groq()

# Display the title
st.title("Groq Blog Generator")

# Input fields for blog generation
blog_topic = st.text_input("Enter the blog topic")
blog_length = st.selectbox("Select the blog length", ["Short", "Medium", "Long"])
blog_person = st.text_input("Enter the person from whose perspective the blog should be written")

# Input field for the user's prompt
if blog_topic and blog_length and blog_person:
    prompt = f"Write a {blog_length} blog on the topic '{blog_topic}' from the perspective of {blog_person}."
    
    # Send the user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt}
    ]

    model_id = "llama3-groq-70b-8192-tool-use-preview"

    try:
        # Try to get the response from the model
        response = client.chat.completions.create(
            model=model_id,
            messages=messages
        )

        assistant_response = response.choices[0].message.content

        # Display only the assistant's blog response
        st.markdown("### Generated Blog")
        st.markdown(assistant_response)

    except BadRequestError as e:
        st.write(f"{e}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}. Please try again later.")
