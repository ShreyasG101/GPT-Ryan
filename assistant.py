# Bring in deps
import os 
from apikey import openaikey, zapierkey, gkey, cse_id, serper_key

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 
from langchain.chat_models import ChatOpenAI



from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.agents import AgentType, Tool
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.utilities import OpenWeatherMapAPIWrapper, GoogleSerperAPIWrapper, GoogleSearchAPIWrapper
from langchain.agents.agent_toolkits import NLAToolkit



os.environ['OPENAI_API_KEY'] = openaikey
os.environ["ZAPIER_NLA_API_KEY"] =zapierkey
#os.environ["OPENWEATHERMAP_API_KEY"] =
os.environ["GOOGLE_CSE_ID"] = cse_id
os.environ["GOOGLE_API_KEY"] = gkey
os.environ["SERPER_API_KEY"] = serper_key



wikipedia = WikipediaAPIWrapper()

chatopenai = OpenAI(temperature=0)
llm = chatopenai
zapier = ZapierNLAWrapper()
z_toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
speak_toolkit = NLAToolkit.from_llm_and_url(llm, "https://api.speak.com/openapi.yaml")
search = GoogleSearchAPIWrapper(k=10)
serp_search = GoogleSerperAPIWrapper()




# Slightly tweak the instructions from the default agent
openapi_format_instructions = """
You are an AI assistant that will be helping a user named Shreyas with their questions and tasks utilizing the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: what to instruct the AI Action representative.
Observation: The Agent's response
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer. User can't see any of my observations, API responses, links, or tools.
Final Answer: the final answer to the original input question with the right amount of detail

When responding with your Final Answer, remember that the person you are responding to CANNOT see any of your Thought/Action/Action Input/Observations, so if there is any relevant information there you need to include it explicitly in your response. Pretend to be a friendly assistant / motivational coach to someone that you know really well.
Your response shouldn't be too long - summarize where needed. Maybe slip in a joke if possible. Try to be observant of all the details in the data and try to come across as observant and emotionally intelligent as you can. Don't ask for a followup or if they need any other help."""
tools = [Tool(
        name = "Wikipedia",
        func=wikipedia.run,
        description="This gives you access to wikipedia for when you need to answer questsions about specific people, events, or subjects."
    ),    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
        Tool(
        name="Intermediate Answer",
        func=serp_search.run,
        description="useful for when you need to ask with search"
    )

]+ z_toolkit.get_tools() + speak_toolkit.get_tools()
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs={"format_instructions":openapi_format_instructions})

def run(prompt):
    return agent.run(prompt)


