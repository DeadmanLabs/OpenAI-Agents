from typing import List, Optional, Literal, Dict, Any, Union, Set
from pydantic import BaseModel, Field
from enum import Enum
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool
from models import ConceptComponent, GeneralArchitectureDesign

class StepStatus(str, Enum):
    """Status of a step in the agent's plan"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class PlanStep(BaseModel):
    """A step in the agent's plan for designing architecture"""
    id: str
    status: StepStatus = StepStatus.PENDING
    dependencies: List[str] = Field(default_factory=list)
    output: Optional[Dict[str, Any]] = None
    notes: List[str] = Field(default_factory=list)

class ResearchItem(BaseModel):
    """Information about a topic that needs research"""
    topic: str
    query: str
    status: StepStatus = StepStatus.PENDING
    findings: List[str] = Field(default_factory=list)
    relevance: Optional[str] = None

class RequirementCategory(str, Enum):
    """Categories of software requirements"""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    TECHNICAL = "technical"
    BUSINESS = "business"
    CONSTRAINT = "constraint"

class Requirement(BaseModel):
    """A requirement for the software system"""
    id: str
    description: str
    category: RequirementCategory
    priority: int = 1  # 1-5 scale, 5 being highest
    notes: List[str] = Field(default_factory=list)

@dataclass
class ArchitectAgentState:
    """Dataclass to maintain state for the Software Architect AI Agent"""
    
    # Basic information
    project_id: str
    project_name: str
    project_description: str
    
    # Requirements gathering
    requirements: List[Requirement] = Field(default_factory=list)
    
    # Planning state
    plan: List[PlanStep] = Field(default_factory=list)
    current_step_id: Optional[str] = None
    
    # Research state
    research_items: List[ResearchItem] = Field(default_factory=list)
    research_keywords: Set[str] = Field(default_factory=set)
    
    # Architecture design state
    components_draft: List[ConceptComponent] = Field(default_factory=list)
    architecture_drafts: List[Dict[str, Any]] = Field(default_factory=list)
    final_architecture: Optional[GeneralArchitectureDesign] = None
    
    # Decision points and rationale
    decisions: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    
    # Conversation context
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    clarification_questions: List[str] = Field(default_factory=list)
    
    # Progress tracking
    progress: Dict[str, float] = Field(default_factory=lambda: {
        "requirements_gathering": 0.0,
        "planning": 0.0,
        "research": 0.0,
        "component_design": 0.0,
        "architecture_design": 0.0,
        "review": 0.0
    })
    
    # Metadata
    created_at: str = Field(default_factory=lambda: __import__('datetime').datetime.now().isoformat())
    last_updated_at: str = Field(default_factory=lambda: __import__('datetime').datetime.now().isoformat())
    agent_version: str = "1.0.0"
    
    def update_progress(self, stage: str, value: float) -> None:
        """Update progress for a particular stage"""
        if stage in self.progress:
            self.progress[stage] = max(0.0, min(1.0, value))  # Clamp between 0 and 1
            self.last_updated_at = __import__('datetime').datetime.now().isoformat()
    
    def add_plan_step(self, step: PlanStep) -> None:
        """Add a new step to the plan"""
        self.plan.append(step)
        self.last_updated_at = __import__('datetime').datetime.now().isoformat()
    
    def update_step_status(self, step_id: str, status: StepStatus) -> None:
        """Update the status of a plan step"""
        for step in self.plan:
            if step.id == step_id:
                step.status = status
                self.last_updated_at = __import__('datetime').datetime.now().isoformat()
                return
    
    def add_research_item(self, item: ResearchItem) -> None:
        """Add a new research item"""
        self.research_items.append(item)
        self.research_keywords.add(item.topic)
        self.last_updated_at = __import__('datetime').datetime.now().isoformat()
    
    def add_component(self, component: ConceptComponent) -> None:
        """Add a component to the draft list"""
        self.components_draft.append(component)
        self.last_updated_at = __import__('datetime').datetime.now().isoformat()
    
    def finalize_architecture(self, architecture: GeneralArchitectureDesign) -> None:
        """Set the final architecture design"""
        self.final_architecture = architecture
        self.progress["architecture_design"] = 1.0
        self.last_updated_at = __import__('datetime').datetime.now().isoformat()
    
    def get_overall_progress(self) -> float:
        """Calculate overall progress as weighted average"""
        weights = {
            "requirements_gathering": 0.15,
            "planning": 0.10,
            "research": 0.20,
            "component_design": 0.25,
            "architecture_design": 0.20,
            "review": 0.10
        }
        return sum(self.progress[stage] * weights[stage] for stage in weights)
    
    def add_decision(self, key: str, decision: Dict[str, Any]) -> None:
        """Record a decision with its rationale"""
        self.decisions[key] = decision
        self.last_updated_at = __import__('datetime').datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the state to a dictionary for serialization"""
        import dataclasses
        return dataclasses.asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArchitectAgentState':
        """Create a state object from a dictionary"""
        # Handle nested objects like PlanStep, ResearchItem, etc.
        if 'plan' in data:
            data['plan'] = [PlanStep(**step) for step in data['plan']]
        if 'research_items' in data:
            data['research_items'] = [ResearchItem(**item) for item in data['research_items']]
        if 'requirements' in data:
            data['requirements'] = [Requirement(**req) for req in data['requirements']]
        if 'components_draft' in data:
            data['components_draft'] = [ConceptComponent(**comp) for comp in data['components_draft']]
        if 'final_architecture' in data and data['final_architecture']:
            data['final_architecture'] = GeneralArchitectureDesign(**data['final_architecture'])
        
        return cls(**data)

@dataclass
class ArchitectureContext:
    state: ArchitectAgentState

def architect_instructions(
        context: RunContextWrapper[ArchitectureContext], agent: Agent[ArchitectureContext]
) -> str:
    return f"The user's name is {context.context.uid}"