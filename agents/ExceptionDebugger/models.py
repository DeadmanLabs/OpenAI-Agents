from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

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
