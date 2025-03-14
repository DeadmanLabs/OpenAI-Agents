from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

# Library Models
class LibraryRequirement(BaseModel):
    """Defines a specific requirement or feature needed from a library."""
    description: str = Field(..., description="Clear description of the required functionality")
    priority: Literal["essential", "important", "nice-to-have"] = Field(
        ..., description="The importance level of this requirement"
    )
    rationale: str = Field(..., description="Why this requirement matters for the project")

class LibraryCandidate(BaseModel):
    """Represents a potential library that's being evaluated."""
    name: str = Field(..., description="Name of the library")
    version: str = Field(..., description="Latest stable version at time of research")
    description: str = Field(..., description="Brief description of what the library does")
    url: str = Field(..., description="Official documentation or repository URL")
    license: str = Field(..., description="License type (e.g., MIT, Apache 2.0)")
    last_updated: str = Field(..., description="Date of last update/release")
    active_maintenance: bool = Field(..., description="Whether the library appears actively maintained")
    stars: Optional[int] = Field(None, description="GitHub stars or equivalent popularity metric if available")
    requires_api_key: bool = Field(..., description="Whether the library requires API keys for core functionality")
    requires_registration: bool = Field(..., description="Whether the library requires registration for core functionality")
    is_free: bool = Field(..., description="Whether the library is completely free to use")
    has_usage_limits: bool = Field(False, description="Whether there are usage limits on the free tier")
    installation_command: str = Field(..., description="Command to install this library (e.g., 'pip install libraryname')")
    
    pros: List[str] = Field(default_factory=list, description="Advantages of using this library")
    cons: List[str] = Field(default_factory=list, description="Limitations or drawbacks of this library")
    
    meets_requirements: Dict[str, bool] = Field(
        default_factory=dict, description="Mapping of requirement descriptions to whether this library meets them"
    )
    
    example_usage: Optional[str] = Field(..., description="Simple code example showing basic usage")

class LibraryEvaluation(BaseModel):
    """Evaluation results for a library candidate."""
    library: LibraryCandidate = Field(..., description="The library being evaluated")
    overall_score: float = Field(..., description="Score from 0-10 based on how well it meets requirements")
    requirement_satisfaction: Dict[str, float] = Field(
        ..., description="How well each requirement is satisfied (0-10)"
    )
    community_support: int = Field(..., description="Rating of community support and resources (0-10)")
    ease_of_integration: int = Field(..., description="How easy it is to integrate with existing code (0-10)")
    performance_notes: Optional[str] = Field(None, description="Notes on performance characteristics if available")
    security_notes: Optional[str] = Field(None, description="Notes on security considerations if available")
    additional_notes: List[str] = Field(default_factory=list, description="Any other relevant notes from evaluation")

class LibraryResearchState(BaseModel):
    """Complete state of the library research process."""
    query: str = Field(..., description="The original query or prompt about needed functionality")
    language: str = Field(..., description="Programming language the library needs to work with")
    target_environment: List[str] = Field(..., description="Target environments (e.g., ['Windows', 'Linux', 'MacOS'])")
    requirements: List[LibraryRequirement] = Field(..., description="List of specific requirements for the library")
    
    candidates: List[LibraryCandidate] = Field(
        default_factory=list, description="Libraries identified as potential candidates"
    )
    evaluations: List[LibraryEvaluation] = Field(
        default_factory=list, description="Detailed evaluations of candidate libraries"
    )
    filtered_candidates: List[str] = Field(
        default_factory=list, description="Libraries filtered out and reasons why"
    )
    
    recommended_library: Optional[LibraryCandidate] = Field(
        None, description="The final recommended library with implementation details"
    )
    
    research_status: Literal["initialized", "gathering_candidates", "evaluating", "complete"] = Field(
        ..., description="Current status of the research process"
    )
    
    research_notes: List[str] = Field(
        default_factory=list, description="Notes generated during the research process"
    )
