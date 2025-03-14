from agents import Agent, Runner, ModelSettings, function_tool

from typing import List, Optional, Literal, Dict, Any, Union
from pydantic import BaseModel, Field

# Context
@dataclass
class ArchitectureDesignState:
    uid: str

def architect_instructions(
        context: RunContextWrapper[ArchitectureDesignState], agent: Agent[ArchitectureDesignState]
) -> str:
    return f"The user's name is {context.context.uid}"

architechture_designer = Agent[ArchitectureDesignState](
    name="Software Architecture Designer",
    instructions=architect_instructions,
    output_type=State,
    model="o3-mini",
    tools=[]
)

@dataclass
class StackBuilderState:
    uid: str

def stack_instructions(
        context: RunContextWrapper[StackBuilderState], agent: Agent[StackBuilderState]
) -> str:
    return "The user's name is {context.context.uid}"

stack_builder = Agent[StackBuilderState](
    name="",
    instructions=stack_instructions,
    output_type=State,
    model="o3-mini",
    tools=[]
)




@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    def fetch_purchases() -> list[Purchase]:
        return []

manager_agent = Agent(
    name="",
    instructions="",
    handoffs=[other, agents]
)

guided_agent = Agent(
    name="",
    instructions="",
    output_type=MyOutput
)

@function_tool
def get_weather(city: str) -> str:
    return f"Its sunny nigga"

weather_agent = Agent(
    name="",
    instructions="",
    model="o3-mini",
    tools=[get_weather]
)

smart_agent = Agent[UserContext](
    name="",
    instructions=""
)

result = Runner.run_sync(guided_agent, input_data)
output = result.final_output_as(MyOutput)

agent = Agent(name="Assistant", instructions="You are a helpful assistant")
result = Runner.run_sync(agent, "Write a poem about programming")
print(result.final_output)