import streamlit as st
from langchain.llms import OpenAI

st.title("Market Entry Assistant")

class MarketEntryApp:
    def __init__(self):
        self.output_placeholder = st.empty()

    # def run_crew(self, topic, company_name):
    #     # Initialize the MarketEntryCrew
    #     crew_instance = MarketEntryCrew()
    #     crew = crew_instance.crew()

    #     # Define the inputs for the crew
    #     inputs = {
    #         'topic': topic,
    #         'company_name': company_name
    #     }

    #     # Kickoff the crew and capture the output
    #     result = crew.kickoff(inputs=inputs)
    #     return result
    
# with st.sidebar:
#     st.header("Enter your market entry details")
#     with st.form("market_entry_form"):
#     topic = st.text_input(
#         "What is the topic or industry you're interested in?",
#         placeholder="e.g., Autonomous Drone Systems"
#     )
#     company_name = st.text_input(
#         "Enter the company name:",
#         placeholder="e.g., Airbus"
#     )
#     submitted = st.form_submit_button("Submit")
#     st.devider()


with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    # elif submitted:
    #     generate_response(text)