from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

# Software Planner Models
class FunctionSignature(BaseModel):
    """Defines a function signature with parameters and return type."""
    name: str = Field(..., description="Name of the function")
    description: str = Field(..., description="Description of what the function does")
    parameters: List[Dict[str, str]] = Field(
        default_factory=list, 
        description="List of parameters with name, type, and description"
    )
    return_type: str = Field(..., description="Return type of the function")
    return_description: str = Field(..., description="Description of what the function returns")
    exceptions: List[Dict[str, str]] = Field(
        default_factory=list, 
        description="Potential exceptions this function may raise"
    )
    is_async: bool = Field(False, description="Whether this function is asynchronous")
    example_usage: Optional[str] = Field(None, description="Example of how to use this function")

class ClassDefinition(BaseModel):
    """Defines a class with its properties and methods."""
    name: str = Field(..., description="Name of the class")
    description: str = Field(..., description="Description of the class's purpose")
    attributes: List[Dict[str, str]] = Field(
        default_factory=list, 
        description="List of class attributes with name, type, and description"
    )
    methods: List[FunctionSignature] = Field(default_factory=list, description="Methods of the class")
    parent_class: Optional[str] = Field(None, description="Parent class if this inherits from another class")
    interfaces: List[str] = Field(default_factory=list, description="Interfaces this class implements")
    is_abstract: bool = Field(False, description="Whether this is an abstract class")
    security_considerations: List[str] = Field(default_factory=list, description="Security aspects to consider")
    dependencies: List[str] = Field(default_factory=list, description="External dependencies needed by this class")

class ComponentDefinition(BaseModel):
    """Defines a software component (module, package, etc.)."""
    name: str = Field(..., description="Name of the component")
    description: str = Field(..., description="Description of the component's purpose")
    type: Literal["module", "package", "service", "library", "utility"] = Field(
        ..., description="Type of component"
    )
    functions: List[FunctionSignature] = Field(default_factory=list, description="Top-level functions in this component")
    classes: List[ClassDefinition] = Field(default_factory=list, description="Classes defined in this component")
    dependencies: List[str] = Field(default_factory=list, description="External dependencies needed by this component")
    internal_dependencies: List[str] = Field(
        default_factory=list, description="Other components in the project this depends on"
    )
    libraries: List[Dict[str, Any]] = Field(
        default_factory=list, description="Libraries required by this component (from Library Researcher)"
    )
    security_considerations: List[str] = Field(default_factory=list, description="Security aspects to consider")
    efficiency_considerations: List[str] = Field(default_factory=list, description="Performance considerations")

class ComponentRelationship(BaseModel):
    """Defines a relationship between two components."""
    source: str = Field(..., description="Source component name")
    target: str = Field(..., description="Target component name")
    relationship_type: Literal["depends_on", "extends", "uses", "implements", "communicates_with"] = Field(
        ..., description="Type of relationship between components"
    )
    description: str = Field(..., description="Description of how these components interact")
    data_flow: Optional[str] = Field(None, description="Description of data flowing between components")
    is_bidirectional: bool = Field(False, description="Whether the relationship is bidirectional")

class SecurityConsideration(BaseModel):
    """Defines a security consideration for the software."""
    category: str = Field(..., description="Category of security concern (e.g., 'Authentication', 'Data Validation')")
    description: str = Field(..., description="Description of the security consideration")
    mitigation_strategy: str = Field(..., description="How this security concern will be addressed")
    components_affected: List[str] = Field(..., description="Components affected by this security consideration")
    priority: Literal["critical", "high", "medium", "low"] = Field(..., description="Priority of this consideration")
    potential_vulnerabilities: List[str] = Field(
        default_factory=list, description="Potential vulnerabilities if not addressed"
    )

class EfficiencyConsideration(BaseModel):
    """Defines an efficiency/performance consideration."""
    category: str = Field(..., description="Category of efficiency concern (e.g., 'Memory Usage', 'CPU Performance')")
    description: str = Field(..., description="Description of the efficiency consideration")
    optimization_strategy: str = Field(..., description="How this efficiency concern will be addressed")
    components_affected: List[str] = Field(..., description="Components affected by this efficiency consideration")
    priority: Literal["critical", "high", "medium", "low"] = Field(..., description="Priority of this consideration")
    metrics: Optional[Dict[str, str]] = Field(
        None, description="Metrics to track for this efficiency consideration"
    )

class ProgrammingTask(BaseModel):
    """Defines a task to be sent to the Software Programmer agent."""
    component_name: str = Field(..., description="Name of the component to be implemented")
    component_type: str = Field(..., description="Type of component (class, function, module, etc.)")
    specifications: Union[ClassDefinition, FunctionSignature, ComponentDefinition] = Field(
        ..., description="Detailed specifications of what needs to be implemented"
    )
    dependencies: List[str] = Field(default_factory=list, description="Dependencies this implementation needs")
    libraries: List[Dict[str, Any]] = Field(
        default_factory=list, description="Libraries to use (from Library Researcher)"
    )
    task_description: str = Field(..., description="Detailed description of the programming task")
    security_requirements: List[str] = Field(
        default_factory=list, description="Security requirements for this implementation"
    )
    efficiency_requirements: List[str] = Field(
        default_factory=list, description="Efficiency requirements for this implementation"
    )
    expected_interfaces: List[str] = Field(
        default_factory=list, description="Interfaces this component should expose or implement"
    )
    examples: Optional[str] = Field(None, description="Example code or pseudocode to guide implementation")
    testing_criteria: List[str] = Field(
        default_factory=list, description="Criteria for testing this implementation"
    )
    status: Literal["pending", "in_progress", "completed", "failed"] = Field(
        default="pending", description="Status of this programming task"
    )

class SoftwarePlanState(BaseModel):
    """Complete state of the software planning process."""
    project_name: str = Field(..., description="Name of the software project")
    description: str = Field(..., description="Description of what the software project does")
    components: List[ComponentDefinition] = Field(..., description="Components that make up the software")
    relationships: List[ComponentRelationship] = Field(
        default_factory=list, description="Relationships between components"
    )
    security_considerations: List[SecurityConsideration] = Field(
        default_factory=list, description="Security considerations for the project"
    )
    efficiency_considerations: List[EfficiencyConsideration] = Field(
        default_factory=list, description="Efficiency considerations for the project"
    )
    library_research_requests: List[Dict[str, Any]] = Field(
        default_factory=list, description="Library research requests sent to Library Researcher agent"
    )
    library_selections: List[Dict[str, Any]] = Field(
        default_factory=list, description="Libraries selected based on Library Researcher recommendations"
    )
    programming_tasks: List[ProgrammingTask] = Field(
        default_factory=list, description="Tasks sent to the Software Programmer agent"
    )
    implementation_status: Dict[str, str] = Field(
        default_factory=dict, description="Implementation status for each component"
    )
    planning_notes: List[str] = Field(default_factory=list, description="Notes from the planning process")
    planning_status: Literal["initializing", "designing", "library_research", "task_definition", "implementation", "complete"] = Field(
        default="initializing", description="Current status of the planning process"
    )
    dependency_graph: Optional[Dict[str, List[str]]] = Field(
        None, description="Graph representing component dependencies"
    )
    implementation_order: List[str] = Field(
        default_factory=list, description="Planned order for implementing components"
    )
