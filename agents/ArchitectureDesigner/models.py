from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

class ConceptComponent(BaseModel):
    """A high-level conceptual component of the architecture."""
    name: str = Field(..., description="A descriptive name for the component (e.g., 'User Management', 'Data Storage').")
    category: Literal["backend", "frontend", "database", "messaging", "deployment", "other"] = Field(
        ..., description="The general category of the component."
    )
    role: str = Field(..., description="A high-level description of the component's role in the system.")
    rationale: str = Field(..., description="General reasons for including this component (e.g., scalability, ease of use, open source).")
    pros: List[str] = Field(default_factory=list, description="General advantages of this component.")
    cons: List[str] = Field(default_factory=list, description="General limitations or considerations for this component.")

class GeneralArchitectureDesign(BaseModel):
    """General high-level architecture design focused on concepts rather than specific technologies."""
    summary: str = Field(..., description="A brief summary of the overall architecture concept.")
    backend: ConceptComponent = Field(..., description="Conceptual design for the backend layer.")
    frontend: ConceptComponent = Field(..., description="Conceptual design for the frontend layer.")
    database: ConceptComponent = Field(..., description="Conceptual design for the data storage solution.")
    messaging: Optional[ConceptComponent] = Field(
        None, description="Conceptual design for messaging or event distribution (if applicable)."
    )
    deployment: str = Field(..., description="A general deployment strategy (e.g., container-based, self-hosted).")
    components: List[ConceptComponent] = Field(
        ..., description="A list of other key conceptual components in the architecture."
    )
    rationale: str = Field(..., description="General rationale behind the overall architecture design.")
    requirements: str = Field(..., description="The high-level requirements used to drive the architecture concept.")