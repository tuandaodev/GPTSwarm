from ..operation_registry import register_operation
from ..optimizable_operation import OptimizableOperation

@register_operation
class DesignToBackend(OptimizableOperation):
    """Operation that transforms system design into backend implementation tasks."""

    def __init__(self):
        super().__init__()
        self.name = "design_to_backend"
        self.description = "Transforms architectural decisions into .NET backend tasks"

    async def arun(self, inputs):
        """
        Convert system design into concrete backend implementation tasks.
        
        Args:
            inputs (dict): Contains system design specifications
            
        Returns:
            dict: Backend implementation tasks and requirements
        """
        design = inputs.get("design", {})
        
        # Transform architectural decisions into backend tasks
        backend_tasks = await self._extract_backend_tasks(design)
        
        return {
            "backend_tasks": backend_tasks,
            "tech_stack": ".NET Core",
            "dependencies": design.get("backend_dependencies", [])
        }

    async def _extract_backend_tasks(self, design):
        """Extract backend-specific tasks from the overall system design."""
        tasks = []
        
        if "api_endpoints" in design:
            tasks.extend(self._create_api_tasks(design["api_endpoints"]))
            
        if "data_models" in design:
            tasks.extend(self._create_model_tasks(design["data_models"]))
            
        if "services" in design:
            tasks.extend(self._create_service_tasks(design["services"]))
            
        return tasks

    def _create_api_tasks(self, endpoints):
        """Create tasks for API endpoint implementation."""
        return [
            {
                "type": "controller",
                "endpoint": endpoint.get("path"),
                "method": endpoint.get("method"),
                "request_model": endpoint.get("request_model"),
                "response_model": endpoint.get("response_model"),
                "security": endpoint.get("security", [])
            }
            for endpoint in endpoints
        ]

    def _create_model_tasks(self, models):
        """Create tasks for data model implementation."""
        return [
            {
                "type": "model",
                "name": model.get("name"),
                "properties": model.get("properties", []),
                "validations": model.get("validations", []),
                "relationships": model.get("relationships", [])
            }
            for model in models
        ]

    def _create_service_tasks(self, services):
        """Create tasks for service layer implementation."""
        return [
            {
                "type": "service",
                "name": service.get("name"),
                "operations": service.get("operations", []),
                "dependencies": service.get("dependencies", []),
                "data_access": service.get("data_access", {})
            }
            for service in services
        ]