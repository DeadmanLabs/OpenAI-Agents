from agents import Agent, Runner, ModelSettings, function_tool

from context import architect_instructions, ArchitectureContext
from models import GeneralArchitectureDesign, ConceptComponent

class ArchitectAgent:
    def __init__(self):
        self._research_agent = Agent[ArchitectureContext](
            name="",
            instructions="",
            output_type=ConceptComponent,
            model="o3-mini",
            tools=[]
        )

        # Handoff Agents
        self._architect_backend = Agent[ArchitectureContext](
            name="",
            instructions="",
            output_type=ConceptComponent,
            handoffs=[_research_agent],
            model="o3-mini",
            tools=[]
        )

        self._architect_frontend = Agent[ArchitectureContext](
            name="",
            instructions="",
            output_type=ConceptComponent,
            handoffs=[_research_agent],
            model="o3-mini",
            tools=[]
        )

        self._architect_database = Agent[ArchitectureContext](
            name="",
            instructions="",
            output_type=ConceptComponent,
            handoffs=[_research_agent],
            model="o3-mini",
            tools=[]
        )

        self._architect_messaging = Agent[ArchitectureContext](
            name="",
            instructions="",
            output_type=ConceptComponent,
            handoffs=[_research_agent],
            model="o3-mini",
            tools=[]
        )

        self._architect_deployment = Agent[ArchitectureContext](
            name="",
            instructions="",
            output_type=ConceptComponent,
            handoffs=[_research_agent],
            model="o3-mini",
            tools=[]
        )

        self._architect_components = Agent[ArchitectureContext](
            name="",
            instructions="",
            output_type=ConceptComponent,
            handoffs=[_research_agent],
            model="o3-mini",
            tools=[]
        )

        self.architect = Agent[ArchitectureContext](
            name="Software Architecture Designer",
            instructions=architect_instructions,
            output_type=GeneralArchitectureDesign,
            handoffs=[_architect_backend, _architect_frontend, _architect_database, _architect_messaging, _architect_deployment, _architect_components],
            model="o3-mini",
            tools=[]
        )

    def run(self, prompt: str) -> GeneralArchitectureDesign:
        result = Runner.run_sync(self.architect, prompt)
        return result.final_output_as(GeneralArchitectureDesign)