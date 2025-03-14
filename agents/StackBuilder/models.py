from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

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

class ComponentAction(BaseModel):
    """Represents the actions required to install and setup the structure"""
    container: bool = Field(..., description="Wether or not the solution is inside of a container")
    action: Literal["command", "download", "edit"] = Field(
        ..., description="The action needed to be taken for the infrastructure or solution to be installed"
    )
    command: Optional[List[List[str]]] = Field(..., description="The command(s) that needs to be run to install the solution (if action is command) split into arguments.")
    url: Optional[List[str]] = Field(..., description="The url to the binary we need to download and execute (if action is download).")
    file_path: Optional[str] = Field(None, description="The path to the file we need to apply the edit to (if action is edit)")
    diff: Optional[str] = Field(None, description="The git diff we need to apply to a file (if action is edit)")

class ComponentActions(BaseModel):
    selected_technology: str = Field(..., description="")
    actions: List[ComponentAction] = Field(default_factory=list, description="")

class ComponentActionResult(BaseModel):
    """Represents the result of an action to install a component"""
    success: bool = Field(..., description="Wether the installation action was a success")
    error: Optional[str] = Field(None, description="The error that occured (if it occured)")
    next_steps: Optional[List[str]] = Field(..., description="The next steps the user should take if the install failed.")

class ComponentActionReport(BaseModel):
    """Represents the report on what actions were taken and their status"""
    results: Dict[ComponentAction, ComponentActionResult] = Field(..., description="The actions and the results while attempting to perform them.")