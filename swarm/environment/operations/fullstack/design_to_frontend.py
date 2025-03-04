from ..operation_registry import register_operation
from ..optimizable_operation import OptimizableOperation


@register_operation
class DesignToFrontend(OptimizableOperation):
    """Operation that transforms system design into frontend implementation tasks."""

    def __init__(self):
        super().__init__()
        self.name = "design_to_frontend"
        self.description = "Transforms architectural decisions into Angular frontend tasks"

    async def arun(self, inputs):
        """
        Convert system design into concrete frontend implementation tasks.
        
        Args:
            inputs (dict): Contains system design specifications
            
        Returns:
            dict: Frontend implementation tasks and requirements
        """
        design = inputs.get("design", {})
        
        # Transform architectural decisions into frontend tasks
        frontend_tasks = await self._extract_frontend_tasks(design)
        
        return {
            "frontend_tasks": frontend_tasks,
            "tech_stack": "Angular",
            "dependencies": design.get("frontend_dependencies", [])
        }

    async def _extract_frontend_tasks(self, design):
        """Extract frontend-specific tasks from the overall system design."""
        # This would contain the actual logic for task extraction
        tasks = []
        
        if "ui_components" in design:
            tasks.extend(self._create_component_tasks(design["ui_components"]))
            
        if "api_endpoints" in design:
            tasks.extend(self._create_service_tasks(design["api_endpoints"]))
            
        return tasks

    def _create_component_tasks(self, components):
        """Create tasks for UI component implementation."""
        return [
            {
                "type": "component",
                "name": comp.get("name"),
                "requirements": comp.get("requirements", []),
                "dependencies": comp.get("dependencies", [])
            }
            for comp in components
        ]

    def _create_service_tasks(self, endpoints):
        """Create tasks for service implementation."""
        return [
            {
                "type": "service",
                "endpoint": endpoint.get("path"),
                "method": endpoint.get("method"),
                "data_model": endpoint.get("data_model")
            }
            for endpoint in endpoints
        ]