from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

class DependencyInfo(BaseModel):
    """Information about a single dependency."""
    name: str = Field(..., description="Name of the dependency")
    version: Optional[str] = Field(None, description="Current version in use")
    source: Literal["external", "internal"] = Field(..., description="Whether this is an external package or internal module")
    import_statements: List[str] = Field(default_factory=list, description="Import statements used in the codebase")
    usage_count: int = Field(0, description="Number of files/modules that use this dependency")
    usage_locations: List[str] = Field(default_factory=list, description="File paths where this dependency is used")
    critical_level: Literal["critical", "high", "medium", "low"] = Field(
        "medium", description="How critical this dependency is to the project"
    )
    is_direct: bool = Field(True, description="Whether this is a direct dependency or transitive")
    license: Optional[str] = Field(None, description="License of the dependency if external")
    documentation_url: Optional[str] = Field(None, description="URL to the dependency's documentation")
    repository_url: Optional[str] = Field(None, description="URL to the dependency's source repository")
    last_updated: Optional[str] = Field(None, description="When the dependency was last updated")

class DependencyIssue(BaseModel):
    """An issue identified with a dependency."""
    dependency_name: str = Field(..., description="Name of the dependency with the issue")
    issue_type: Literal["version_conflict", "security_vulnerability", "license_issue", "deprecated", "unmaintained", "performance", "compatibility", "other"] = Field(
        ..., description="Type of issue"
    )
    severity: Literal["critical", "high", "medium", "low"] = Field(..., description="Severity of the issue")
    description: str = Field(..., description="Description of the issue")
    affected_components: List[str] = Field(default_factory=list, description="Components affected by this issue")
    discovered_at: str = Field(..., description="When this issue was discovered")
    is_resolved: bool = Field(False, description="Whether this issue has been resolved")
    resolution_steps: Optional[str] = Field(None, description="Steps taken to resolve the issue")
    resolved_at: Optional[str] = Field(None, description="When this issue was resolved")
    references: List[str] = Field(default_factory=list, description="References related to this issue")

class DependencyAlternative(BaseModel):
    """An alternative for an existing dependency."""
    original_dependency: str = Field(..., description="Name of the original dependency")
    alternative_name: str = Field(..., description="Name of the alternative dependency")
    version: str = Field(..., description="Latest stable version of the alternative")
    compatibility_score: int = Field(..., description="Compatibility score from 1-10")
    migration_difficulty: Literal["trivial", "easy", "moderate", "difficult", "very_difficult"] = Field(
        ..., description="Difficulty of migrating to this alternative"
    )
    advantages: List[str] = Field(default_factory=list, description="Advantages of this alternative")
    disadvantages: List[str] = Field(default_factory=list, description="Disadvantages of this alternative")
    community_support: int = Field(..., description="Level of community support from 1-10")
    license: str = Field(..., description="License of the alternative")
    active_maintenance: bool = Field(..., description="Whether the alternative is actively maintained")
    migration_guide: Optional[str] = Field(None, description="Guide for migrating to this alternative")
    popularity_metrics: Optional[Dict[str, Any]] = Field(None, description="Metrics showing popularity")
    recommended: bool = Field(False, description="Whether this alternative is recommended")

class DependencyGraph(BaseModel):
    """A graph representation of project dependencies."""
    nodes: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Nodes in the graph (dependencies)"
    )
    edges: List[Dict[str, Any]] = Field(
        default_factory=list, description="Edges in the graph (dependency relationships)"
    )
    subgraphs: Dict[str, List[str]] = Field(
        default_factory=dict, description="Subgraphs for related dependencies"
    )
    critical_paths: List[List[str]] = Field(
        default_factory=list, description="Critical dependency paths"
    )
    cycles: List[List[str]] = Field(
        default_factory=list, description="Cycles in the dependency graph"
    )
    root_dependencies: List[str] = Field(
        default_factory=list, description="Root dependencies (not dependent on anything else)"
    )
    leaf_dependencies: List[str] = Field(
        default_factory=list, description="Leaf dependencies (nothing depends on them)"
    )
    visualization_data: Optional[Dict[str, Any]] = Field(
        None, description="Data for visualizing the dependency graph"
    )

class CodebaseAnalysisResult(BaseModel):
    """Results from analyzing the codebase for dependencies."""
    total_files_analyzed: int = Field(..., description="Total number of files analyzed")
    total_imports_found: int = Field(..., description="Total number of import statements found")
    external_dependencies: Dict[str, DependencyInfo] = Field(
        default_factory=dict, description="External dependencies found"
    )
    internal_dependencies: Dict[str, DependencyInfo] = Field(
        default_factory=dict, description="Internal dependencies found"
    )
    dependency_graph: DependencyGraph = Field(..., description="Graph of dependencies")
    issues_found: List[DependencyIssue] = Field(default_factory=list, description="Issues found with dependencies")
    unused_dependencies: List[str] = Field(default_factory=list, description="Dependencies that appear unused")
    analysis_timestamp: str = Field(..., description="When this analysis was performed")
    analysis_duration: float = Field(..., description="Duration of the analysis in seconds")
    analysis_coverage: float = Field(..., description="Percentage of codebase covered by the analysis")

class DependencyResearchTask(BaseModel):
    """A task to research dependency alternatives."""
    task_id: str = Field(..., description="Unique identifier for this task")
    dependency_name: str = Field(..., description="Name of the dependency to research")
    reason_for_research: str = Field(..., description="Reason for researching alternatives")
    current_version: Optional[str] = Field(None, description="Current version in use")
    required_features: List[str] = Field(default_factory=list, description="Features required in alternatives")
    compatibility_requirements: List[str] = Field(
        default_factory=list, description="Compatibility requirements for alternatives"
    )
    status: Literal["pending", "in_progress", "completed"] = Field(
        default="pending", description="Status of this research task"
    )
    results: List[DependencyAlternative] = Field(
        default_factory=list, description="Results of the research"
    )
    timestamp: str = Field(..., description="When this task was created")
    completed_at: Optional[str] = Field(None, description="When this task was completed")

class PlannerCommunication(BaseModel):
    """Communication with the Software Planner agent."""
    communication_id: str = Field(..., description="Unique identifier for this communication")
    timestamp: str = Field(..., description="When this communication occurred")
    direction: Literal["to_planner", "from_planner"] = Field(
        ..., description="Direction of communication"
    )
    content: Dict[str, Any] = Field(..., description="Content of the communication")
    related_dependencies: List[str] = Field(
        default_factory=list, description="Dependencies related to this communication"
    )
    purpose: str = Field(..., description="Purpose of this communication")
    response_required: bool = Field(False, description="Whether a response is required")
    response_received: bool = Field(False, description="Whether a response was received")
    response_id: Optional[str] = Field(None, description="ID of the response communication")

class DependencyModificationPlan(BaseModel):
    """Plan for modifying dependencies based on analysis and research."""
    plan_id: str = Field(..., description="Unique identifier for this plan")
    created_at: str = Field(..., description="When this plan was created")
    dependencies_to_add: List[Dict[str, Any]] = Field(
        default_factory=list, description="Dependencies to add to the project"
    )
    dependencies_to_remove: List[str] = Field(
        default_factory=list, description="Dependencies to remove from the project"
    )
    dependencies_to_update: List[Dict[str, Any]] = Field(
        default_factory=list, description="Dependencies to update in the project"
    )
    dependencies_to_replace: List[Dict[str, Any]] = Field(
        default_factory=list, description="Dependencies to replace with alternatives"
    )
    implementation_steps: List[str] = Field(
        default_factory=list, description="Steps to implement the modifications"
    )
    affected_files: List[str] = Field(
        default_factory=list, description="Files affected by these modifications"
    )
    estimated_effort: str = Field(..., description="Estimated effort to implement these modifications")
    risks: List[str] = Field(default_factory=list, description="Risks associated with these modifications")
    benefits: List[str] = Field(default_factory=list, description="Benefits of these modifications")
    approved: bool = Field(False, description="Whether this plan has been approved")
    approved_by: Optional[str] = Field(None, description="Who approved this plan")
    approved_at: Optional[str] = Field(None, description="When this plan was approved")