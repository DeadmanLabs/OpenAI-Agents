from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

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
