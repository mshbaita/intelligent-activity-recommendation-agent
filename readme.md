#Activity Recommendation Agent

####Run locally

- Create a virtual venv directory for python python-m venv venv.
- Activate venv  source venv/bin/activate.
- Install requirements file pip install -r requirements.txt.
- Under utils add your openai api key and serp api key.
- Run main.py.

####Notes
- Serp api key is not verified(mobile sending code issue), so the output never tested, its commented out LINE 27 agent.py
- Python version used 3.10.9

####Design
    actions 
        - Ask question ( ask questions about the required and option parameters)
        - Google search (Using langchain tool) getting extra information from google to enrich recommend_activity prompt
        - Slot extraction (Map the generated/output from 
        - Recommend activities
    llm engine
        - Openai chat models i.e. Turbo
        - Openai generative models i.e. Text-davinci-003
    google_engine
        - Langchain serp tool 
    state
        - Required parameters
        - Optional parameters
        - List of messages
        - Search result
    agent
        - decision making method
        - execute actions method 
        - execute method


#### Summary of experience 
In the proposed design, I have incorporated an actions concept to this agent, employing a custom development approach with some assistance from the LangChain search engine tool. However, it should be noted that complete reliance on tools or frameworks like LangChain or autonomous agents was avoided due to their immaturity for development purposes. Instead, I utilized specific portions of LangChain's code as a search tool to enhance the functionality of the system.







#### Enhancements/Recommended Solution
The project can benefit from various enhancements across different areas. Starting with Slot_Extraction, there are several improvements that can be implemented:

Introducing few-shot learning within the prompt can effectively reduce the hallucination of the language model (LLM).
Performing fine-tuning after generating a dataset specifically designed for prompt completion can minimize hallucination.
While the flow currently works most of the time, incorporating either fine-tuning or few-shot learning techniques would significantly enhance its accuracy.
To address the issue of missing parameters, the following modifications can be made:

Instead of using a ping-pong approach, asking for all the missing required parameters in a single message can streamline the process.
Alternatively, the missing parameters can be requested one by one, reducing unnecessary back-and-forth communication.
Another valuable addition would be the inclusion of a new action called "summary_after_google_search":

Upon retrieving results from a Google search, trimming the obtained information and passing it as input to another prompt for generating a summary would provide more concise and relevant content.
The generated summary can then be utilized in conjunction with other parameters for recommendation activities.
To enhance the overall performance, the following features can be incorporated:

Implementing asynchronous methods can improve efficiency and responsiveness.
Introducing a streaming response, such as displaying "agent is typing..." messages, would create a more realistic and interactive experience for the user.




