from agents import Agent, Runner, ModelSettings, function_tool

from typing import List, Optional, Literal, Dict, Any, Union
from pydantic import BaseModel, Field

# Architecture Models
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

class GeneralArchitechtureDesign(BaseModel):
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

# Stack Models
class SelectedComponent(BaseModel):
    """Represents the selected technology for a conceptual component."""
    conceptual_name: str = Field(..., description="The name of the conceptual component (e.g., 'Backend')")
    category: Literal["backend", "frontend", "database", "messaging", "deployment", "other"] = Field(
        ..., description="The category of the conceptual component."
    )
    selected_technology: str = Field(..., description="The specific technology or framework chosen (e.g., 'Express.js', 'React.js')")
    rationale: str = Field(..., description="Brief explanation of why this technology was selected")
    pros: List[str] = Field(default_factory=list, description="Advantages of the selected technology")
    cons: List[str] = Field(default_factory=list, description="Limitations of the selected technology")
    installation_instructions: Optional[str] = Field(
        None, description="Instructions for installing or deploying this technology (e.g., shell commands, package installation)"
    )
    docker_snippet: Optional[str] = Field(
        None, description="Any Dockerfile modifications needed to integrate this component"
    )

class StackBuildState(BaseModel):
    """Complete stack build state."""
    project_name: str = Field(..., description="The final project name")
    output_directory: str = Field(..., description="Directory path where the project is created")
    architecture_design: Dict[str, Any] = Field(..., description="The conceptual architecture design (as dict)")
    selections: List[SelectedComponent] = Field(..., description="Technology selections for each conceptual component")
    installation_status: Literal["pending", "in_progress", "complete", "failed"] = Field(
        ..., description="Status of the installation process"
    )
    notes: List[str] = Field(default_factory=list, description="Additional notes from the stack building process")

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

# Software Programmer Models
class CodeFile(BaseModel):
    """Represents a single code file to be created or modified."""
    file_path: str = Field(..., description="Path where the file should be saved")
    content: str = Field(..., description="The complete content of the file")
    language: str = Field(..., description="Programming language of the file")
    overwrite_existing: bool = Field(False, description="Whether to overwrite if file exists")

class DocComment(BaseModel):
    """Represents a documentation comment for code elements."""
    element_type: Literal["function", "class", "method", "module", "parameter", "attribute", "property"] = Field(
        ..., description="Type of code element being documented"
    )
    element_name: str = Field(..., description="Name of the element being documented")
    description: str = Field(..., description="Main description of the element")
    params: List[Dict[str, str]] = Field(
        default_factory=list, description="Parameter documentation (name, type, description)"
    )
    returns: Optional[Dict[str, str]] = Field(
        None, description="Return value documentation (type, description)"
    )
    raises: List[Dict[str, str]] = Field(
        default_factory=list, description="Exceptions that may be raised (type, condition)"
    )
    examples: List[str] = Field(default_factory=list, description="Usage examples")
    notes: List[str] = Field(default_factory=list, description="Additional notes or considerations")
    see_also: List[str] = Field(default_factory=list, description="Related elements to reference")

class LoggingStatement(BaseModel):
    """Defines a logging statement to be included in the code."""
    level: Literal["debug", "info", "warning", "error", "critical"] = Field(
        ..., description="Logging level"
    )
    message: str = Field(..., description="Log message content")
    context_data: List[str] = Field(default_factory=list, description="Variables/data to include in log")
    location: str = Field(..., description="Where in the code this log should be placed")
    purpose: str = Field(..., description="Purpose of this logging statement")

class UnitTest(BaseModel):
    """Defines a unit test for implemented code."""
    test_name: str = Field(..., description="Name of the test function")
    element_tested: str = Field(..., description="Name of element being tested")
    test_description: str = Field(..., description="Description of what the test verifies")
    test_inputs: List[Any] = Field(default_factory=list, description="Inputs to test with")
    expected_outputs: List[Any] = Field(default_factory=list, description="Expected outputs or behaviors")
    edge_cases: List[str] = Field(default_factory=list, description="Edge cases being tested")
    mocks_required: List[str] = Field(default_factory=list, description="Any dependencies that need to be mocked")
    code: str = Field(..., description="Complete test function code")

class CodeImplementation(BaseModel):
    """Represents the implementation of a component or function."""
    component_name: str = Field(..., description="Name of the component being implemented")
    component_type: str = Field(..., description="Type of component (class, function, module, etc.)")
    implementation_code: str = Field(..., description="The actual implementation code")
    documentation: List[DocComment] = Field(..., description="Documentation for this implementation")
    logging_statements: List[LoggingStatement] = Field(
        default_factory=list, description="Logging statements included in the implementation"
    )
    unit_tests: List[UnitTest] = Field(default_factory=list, description="Unit tests for this implementation")
    files_created: List[CodeFile] = Field(default_factory=list, description="Files created for this implementation")
    files_modified: List[Dict[str, Any]] = Field(
        default_factory=list, description="Files modified for this implementation"
    )
    dependencies_used: List[str] = Field(default_factory=list, description="Dependencies used in the implementation")
    best_practices_applied: List[str] = Field(
        default_factory=list, description="Best practices applied in this implementation"
    )
    performance_considerations: List[str] = Field(
        default_factory=list, description="Performance considerations addressed"
    )
    security_considerations: List[str] = Field(
        default_factory=list, description="Security considerations addressed"
    )
    integration_notes: List[str] = Field(
        default_factory=list, description="Notes on how this integrates with existing code"
    )

class CodeReview(BaseModel):
    """Self-review of implemented code."""
    component_name: str = Field(..., description="Name of component reviewed")
    clarity_score: int = Field(..., description="Score from 1-10 of code clarity")
    documentation_score: int = Field(..., description="Score from 1-10 of documentation quality")
    robustness_score: int = Field(..., description="Score from 1-10 of code robustness")
    maintainability_score: int = Field(..., description="Score from 1-10 of code maintainability")
    issues_identified: List[str] = Field(default_factory=list, description="Issues identified during review")
    improvement_suggestions: List[str] = Field(
        default_factory=list, description="Suggestions for future improvements"
    )
    best_practices_followed: List[str] = Field(default_factory=list, description="Best practices followed")
    best_practices_missed: List[str] = Field(default_factory=list, description="Best practices that could be applied")
    review_notes: str = Field(..., description="Overall notes from the review")

class ExistingCodeAnalysis(BaseModel):
    """Analysis of existing code for integration purposes."""
    file_path: str = Field(..., description="Path to the analyzed file")
    file_content: str = Field(..., description="Content of the analyzed file")
    language: str = Field(..., description="Programming language of the file")
    defined_elements: List[Dict[str, Any]] = Field(
        default_factory=list, description="Elements defined in this file (functions, classes, etc.)"
    )
    dependencies: List[str] = Field(default_factory=list, description="Dependencies used in this file")
    integration_points: List[Dict[str, str]] = Field(
        default_factory=list, description="Potential points for integration"
    )
    code_style: Dict[str, Any] = Field(default_factory=dict, description="Code style observations")
    documentation_style: Dict[str, Any] = Field(default_factory=dict, description="Documentation style observations")
    logging_approach: Optional[str] = Field(None, description="Approach to logging in this file")
    naming_conventions: Dict[str, str] = Field(default_factory=dict, description="Naming conventions observed")
    analysis_notes: List[str] = Field(default_factory=list, description="General notes from analysis")

class ProgrammerTask(BaseModel):
    """Task assigned to the Software Programmer agent."""
    task_id: str = Field(..., description="Unique identifier for this task")
    component_specification: Dict[str, Any] = Field(
        ..., description="Specification from the Software Planner"
    )
    task_description: str = Field(..., description="Description of the programming task")
    required_libraries: List[Dict[str, Any]] = Field(
        default_factory=list, description="Libraries to use in implementation"
    )
    security_requirements: List[str] = Field(
        default_factory=list, description="Security requirements to fulfill"
    )
    efficiency_requirements: List[str] = Field(
        default_factory=list, description="Efficiency requirements to fulfill"
    )
    existing_code_to_analyze: List[str] = Field(
        default_factory=list, description="Paths to existing code files to analyze"
    )
    status: Literal["received", "analyzing", "implementing", "testing", "reviewing", "completed", "failed"] = Field(
        default="received", description="Status of this task"
    )
    priority: int = Field(1, description="Priority of this task (higher number = higher priority)")
    assigned_at: str = Field(..., description="When this task was assigned")
    completed_at: Optional[str] = Field(None, description="When this task was completed")

class SoftwareProgrammerState(BaseModel):
    """Complete state of the Software Programmer agent."""
    project_name: str = Field(..., description="Name of the software project")
    current_task: Optional[ProgrammerTask] = Field(None, description="Current task being worked on")
    completed_tasks: List[ProgrammerTask] = Field(default_factory=list, description="Tasks that have been completed")
    pending_tasks: List[ProgrammerTask] = Field(default_factory=list, description="Tasks waiting to be worked on")
    implementations: Dict[str, CodeImplementation] = Field(
        default_factory=dict, description="Implemented components"
    )
    code_reviews: List[CodeReview] = Field(default_factory=list, description="Self-reviews of implemented code")
    existing_code_analyses: List[ExistingCodeAnalysis] = Field(
        default_factory=list, description="Analyses of existing code"
    )
    project_files: List[str] = Field(default_factory=list, description="All files in the project")
    documentation_files: List[str] = Field(default_factory=list, description="Documentation files created")
    programming_notes: List[str] = Field(default_factory=list, description="Notes from the programming process")
    best_practices_used: Dict[str, List[str]] = Field(
        default_factory=dict, description="Best practices used by component"
    )
    issues_encountered: List[Dict[str, Any]] = Field(
        default_factory=list, description="Issues encountered during implementation"
    )
    integration_decisions: List[Dict[str, Any]] = Field(
        default_factory=list, description="Decisions made for code integration"
    )
    overall_status: Literal["idle", "analyzing", "implementing", "integrating", "testing"] = Field(
        default="idle", description="Current overall status of the programmer agent"
    )

# Exception Debugger Models
class ExceptionDetails(BaseModel):
    """Details about an exception encountered during build or run."""
    exception_type: str = Field(..., description="Type of the exception (e.g. 'ImportError', 'TypeError')")
    message: str = Field(..., description="The error message from the exception")
    traceback: str = Field(..., description="Full exception traceback")
    file_path: Optional[str] = Field(None, description="Path to file where exception occurred")
    line_number: Optional[int] = Field(None, description="Line number where exception occurred")
    code_snippet: Optional[str] = Field(None, description="Code snippet where exception occurred")
    timestamp: str = Field(..., description="When the exception occurred")
    environment: Dict[str, str] = Field(
        default_factory=dict, description="Environment details (OS, Python version, etc.)"
    )
    variables_state: Optional[Dict[str, Any]] = Field(
        None, description="State of relevant variables at the time of exception"
    )
    severity: Literal["critical", "high", "medium", "low"] = Field(
        ..., description="Assessed severity of the exception"
    )

class ResearchFinding(BaseModel):
    """Research information about an exception and potential solutions."""
    exception_type: str = Field(..., description="Type of exception researched")
    source: str = Field(..., description="Source of the information (e.g. 'Stack Overflow', 'Documentation')")
    url: Optional[str] = Field(None, description="URL of the information source if applicable")
    solution_summary: str = Field(..., description="Summary of the proposed solution")
    solution_code: Optional[str] = Field(None, description="Code snippet for the solution")
    applicability_score: int = Field(..., description="How applicable this solution is (1-10)")
    implementation_complexity: Literal["simple", "moderate", "complex"] = Field(
        ..., description="Complexity of implementing this solution"
    )
    side_effects: List[str] = Field(default_factory=list, description="Potential side effects of this solution")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites for this solution")
    notes: List[str] = Field(default_factory=list, description="Additional notes about this solution")

class SolutionAttempt(BaseModel):
    """An attempt to resolve an exception."""
    attempt_id: str = Field(..., description="Unique identifier for this attempt")
    exception_id: str = Field(..., description="ID of the exception being addressed")
    approach_description: str = Field(..., description="Description of the approach taken")
    changed_files: List[Dict[str, str]] = Field(
        default_factory=list, description="Files modified in this attempt (path and changes)"
    )
    new_files: List[Dict[str, str]] = Field(
        default_factory=list, description="Files created in this attempt (path and content)"
    )
    commands_executed: List[str] = Field(default_factory=list, description="Commands executed in this attempt")
    libraries_installed: List[str] = Field(default_factory=list, description="Libraries installed in this attempt")
    config_changes: List[Dict[str, Any]] = Field(
        default_factory=list, description="Configuration changes made in this attempt"
    )
    timestamp: str = Field(..., description="When this attempt was made")
    result: Literal["success", "partial_success", "failure", "pending"] = Field(
        default="pending", description="Result of this attempt"
    )
    new_exceptions: List[str] = Field(
        default_factory=list, description="IDs of any new exceptions introduced by this attempt"
    )
    root_cause_identified: bool = Field(False, description="Whether the root cause was identified in this attempt")
    root_cause_description: Optional[str] = Field(None, description="Description of the identified root cause")

class BuildRunSession(BaseModel):
    """A session of building and running the solution."""
    session_id: str = Field(..., description="Unique identifier for this session")
    start_time: str = Field(..., description="When this session started")
    end_time: Optional[str] = Field(None, description="When this session ended")
    build_command: str = Field(..., description="Command used to build the solution")
    run_command: str = Field(..., description="Command used to run the solution")
    build_output: str = Field(..., description="Output from the build process")
    run_output: Optional[str] = Field(None, description="Output from running the solution")
    build_success: bool = Field(..., description="Whether the build succeeded")
    run_success: bool = Field(..., description="Whether running succeeded")
    exceptions_encountered: List[str] = Field(
        default_factory=list, description="IDs of exceptions encountered in this session"
    )
    environment: Dict[str, str] = Field(
        default_factory=dict, description="Environment details for this session"
    )
    solution_version: str = Field(..., description="Version of the solution in this session")
    session_notes: List[str] = Field(default_factory=list, description="Notes from this session")

class UserInteraction(BaseModel):
    """An interaction with the human user."""
    interaction_id: str = Field(..., description="Unique identifier for this interaction")
    timestamp: str = Field(..., description="When this interaction occurred")
    context: str = Field(..., description="Context for this interaction")
    exception_id: Optional[str] = Field(None, description="ID of exception related to this interaction")
    question: str = Field(..., description="Question asked to the user")
    response: Optional[str] = Field(None, description="Response from the user")
    resolution_action: Optional[str] = Field(None, description="Action taken based on user response")
    notes: List[str] = Field(default_factory=list, description="Notes about this interaction")

class SolutionStatus(BaseModel):
    """Current status of the solution."""
    build_status: Literal["succeeded", "failed", "not_attempted"] = Field(
        ..., description="Current build status"
    )
    run_status: Literal["succeeded", "failed", "not_attempted"] = Field(
        ..., description="Current run status"
    )
    outstanding_exceptions: List[str] = Field(
        default_factory=list, description="IDs of exceptions still to be resolved"
    )
    resolved_exceptions: List[str] = Field(
        default_factory=list, description="IDs of exceptions that have been resolved"
    )
    last_successful_build: Optional[str] = Field(None, description="Timestamp of last successful build")
    last_successful_run: Optional[str] = Field(None, description="Timestamp of last successful run")
    current_version: str = Field(..., description="Current version of the solution")
    health_assessment: str = Field(..., description="Overall assessment of solution health")

class ExceptionResolution(BaseModel):
    """Resolution of an exception."""
    exception_id: str = Field(..., description="ID of the resolved exception")
    resolution_description: str = Field(..., description="Description of how the exception was resolved")
    solution_attempts: List[str] = Field(
        default_factory=list, description="IDs of solution attempts for this exception"
    )
    successful_attempt: str = Field(..., description="ID of the successful solution attempt")
    resolution_time: str = Field(..., description="When the exception was resolved")
    research_findings_used: List[str] = Field(
        default_factory=list, description="IDs of research findings used in the resolution"
    )
    files_modified: List[str] = Field(default_factory=list, description="Files modified to resolve the exception")
    root_cause: str = Field(..., description="Description of the root cause of the exception")
    lessons_learned: List[str] = Field(
        default_factory=list, description="Lessons learned from resolving this exception"
    )

class ExceptionDebuggerState(BaseModel):
    """Complete state of the Exception Debugger agent."""
    project_name: str = Field(..., description="Name of the project being debugged")
    project_path: str = Field(..., description="Path to the project files")
    current_exceptions: Dict[str, ExceptionDetails] = Field(
        default_factory=dict, description="Currently active exceptions by ID"
    )
    resolved_exceptions: Dict[str, ExceptionResolution] = Field(
        default_factory=dict, description="Resolved exceptions by ID"
    )
    build_run_sessions: List[BuildRunSession] = Field(
        default_factory=list, description="History of build and run sessions"
    )
    solution_attempts: Dict[str, SolutionAttempt] = Field(
        default_factory=dict, description="Solution attempts by ID"
    )
    research_findings: Dict[str, List[ResearchFinding]] = Field(
        default_factory=dict, description="Research findings by exception type"
    )
    user_interactions: List[UserInteraction] = Field(
        default_factory=list, description="History of interactions with the user"
    )
    current_solution_status: SolutionStatus = Field(
        ..., description="Current status of the solution"
    )
    debugging_history: List[Dict[str, Any]] = Field(
        default_factory=list, description="Chronological history of debugging activities"
    )
    environment_state: Dict[str, Any] = Field(
        default_factory=dict, description="Current state of the environment"
    )
    modified_files: Dict[str, str] = Field(
        default_factory=dict, description="Files modified during debugging"
    )
    debugging_status: Literal["initializing", "building", "running", "analyzing_exception", "researching", "implementing_solution", "verifying", "completed"] = Field(
        default="initializing", description="Current status of the debugging process"
    )
    debug_logs: List[str] = Field(default_factory=list, description="Logs from the debugging process")
    total_exceptions_encountered: int = Field(0, description="Total number of exceptions encountered")
    total_exceptions_resolved: int = Field(0, description="Total number of exceptions resolved")
    continuous_operation: bool = Field(True, description="Whether the agent is operating continuously")

# Dependency Analyzer Models
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

class DependencyAnalyzerState(BaseModel):
    """Complete state of the Dependency Analyzer agent."""
    project_name: str = Field(..., description="Name of the project being analyzed")
    project_path: str = Field(..., description="Path to the project files")
    analysis_results: Optional[CodebaseAnalysisResult] = Field(
        None, description="Results of codebase analysis"
    )
    dependency_issues: Dict[str, List[DependencyIssue]] = Field(
        default_factory=dict, description="Issues by dependency"
    )
    research_tasks: Dict[str, DependencyResearchTask] = Field(
        default_factory=dict, description="Research tasks by ID"
    )
    alternatives_found: Dict[str, List[DependencyAlternative]] = Field(
        default_factory=dict, description="Alternatives by dependency"
    )
    planner_communications: List[PlannerCommunication] = Field(
        default_factory=list, description="Communications with the Software Planner"
    )
    modification_plans: Dict[str, DependencyModificationPlan] = Field(
        default_factory=dict, description="Modification plans by ID"
    )
    current_status: Literal["initializing", "analyzing_codebase", "identifying_issues", "researching_alternatives", "communicating_with_planner", "developing_plans", "idle"] = Field(
        default="initializing", description="Current status of the analyzer"
    )
    last_updated: str = Field(..., description="When this state was last updated")
    analyzed_file_count: int = Field(0, description="Number of files analyzed")
    identified_issue_count: int = Field(0, description="Number of issues identified")
    research_task_count: int = Field(0, description="Number of research tasks")
    completed_research_task_count: int = Field(0, description="Number of completed research tasks")
    dependency_count: Dict[str, int] = Field(
        default_factory=dict, description="Count of dependencies by type"
    )
    analyzer_notes: List[str] = Field(default_factory=list, description="Notes from the analysis process")

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