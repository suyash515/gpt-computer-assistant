from ..llm import *
from ..utils.db import load_model_settings

from langchain.agents import AgentExecutor, create_json_chat_agent
from langchain_experimental.utilities import PythonREPL

prompt_cache = {}
python_repl = PythonREPL()

repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)
tools = [repl_tool]

def get_prompt(name):
    global prompt_cache
    if name in prompt_cache:
        return prompt_cache[name]
    else:
        from langchain import hub
        prompt = hub.pull(name)
        prompt_cache[name] = prompt
        return prompt


def get_agent_executor():
    model = load_model_settings()
    if model == "gpt-4o":
        return chat_agent_executor.create_tool_calling_executor(get_model(), tools)
    elif model == "llava":
        prompt = get_prompt("hwchase17/react-chat-json")
        the_agent = create_json_chat_agent(get_model(), tools, prompt)
        return AgentExecutor(
            agent=the_agent, tools=tools, verbose=True, handle_parsing_errors=True
        )
    elif model == "bakllava":
        prompt = get_prompt("hwchase17/react-chat-json")
        the_agent = create_json_chat_agent(get_model(), tools, prompt)
        return AgentExecutor(
            agent=the_agent, tools=tools, verbose=True, handle_parsing_errors=True
        )