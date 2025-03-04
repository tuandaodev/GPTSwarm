from ..operation_registry import register_operation
from ..optimizable_operation import OptimizableOperation

@register_operation
class FrontendBackendSync(OptimizableOperation):
    """Operation that ensures synchronization between frontend and backend implementations."""

    def __init__(self):
        super().__init__()
        self.name = "frontend_backend_sync"
        self.description = "Synchronizes Angular frontend with .NET backend implementation"

    async def arun(self, inputs):
        """
        Synchronize frontend and backend implementations.
        
        Args:
            inputs (dict): Contains frontend and backend implementation details
            
        Returns:
            dict: Synchronization results and required adjustments
        """
        frontend_impl = inputs.get("frontend_implementation", {})
        backend_impl = inputs.get("backend_implementation", {})
        
        # Analyze and synchronize implementations
        sync_results = await self._analyze_sync_points(frontend_impl, backend_impl)
        
        return {
            "sync_results": sync_results,
            "adjustments_needed": self._generate_adjustments(sync_results)
        }

    async def _analyze_sync_points(self, frontend, backend):
        """Analyze synchronization points between frontend and backend."""
        sync_points = []
        
        # API Contract Validation
        api_sync = self._validate_api_contracts(
            frontend.get("api_services", []),
            backend.get("api_endpoints", [])
        )
        sync_points.extend(api_sync)
        
        # Data Model Validation
        model_sync = self._validate_data_models(
            frontend.get("models", []),
            backend.get("data_models", [])
        )
        sync_points.extend(model_sync)
        
        # Authentication/Authorization Sync
        auth_sync = self._validate_auth_implementation(
            frontend.get("auth_config", {}),
            backend.get("security_config", {})
        )
        sync_points.extend(auth_sync)
        
        return sync_points

    def _validate_api_contracts(self, frontend_services, backend_endpoints):
        """Validate API contracts between frontend and backend."""
        validations = []
        
        for service in frontend_services:
            matching_endpoint = self._find_matching_endpoint(
                service, backend_endpoints)
            
            if matching_endpoint:
                validations.append({
                    "type": "api_contract",
                    "status": "matched",
                    "frontend_service": service.get("name"),
                    "backend_endpoint": matching_endpoint.get("path"),
                    "methods": self._compare_methods(
                        service.get("methods", []),
                        matching_endpoint.get("methods", [])
                    )
                })
            else:
                validations.append({
                    "type": "api_contract",
                    "status": "missing_endpoint",
                    "frontend_service": service.get("name")
                })
        
        return validations

    def _validate_data_models(self, frontend_models, backend_models):
        """Validate data model consistency between frontend and backend."""
        validations = []
        
        for f_model in frontend_models:
            b_model = self._find_matching_model(f_model, backend_models)
            
            if b_model:
                validations.append({
                    "type": "data_model",
                    "status": "matched",
                    "model_name": f_model.get("name"),
                    "property_diffs": self._compare_properties(
                        f_model.get("properties", []),
                        b_model.get("properties", [])
                    )
                })
            else:
                validations.append({
                    "type": "data_model",
                    "status": "missing_model",
                    "model_name": f_model.get("name")
                })
        
        return validations

    def _validate_auth_implementation(self, frontend_auth, backend_auth):
        """Validate authentication/authorization implementation."""
        validations = []
        
        # Compare auth mechanisms
        if frontend_auth.get("mechanism") != backend_auth.get("mechanism"):
            validations.append({
                "type": "auth",
                "status": "mismatch",
                "component": "mechanism",
                "frontend": frontend_auth.get("mechanism"),
                "backend": backend_auth.get("mechanism")
            })
        
        # Compare roles and permissions
        role_diffs = self._compare_roles(
            frontend_auth.get("roles", []),
            backend_auth.get("roles", [])
        )
        if role_diffs:
            validations.append({
                "type": "auth",
                "status": "role_mismatch",
                "differences": role_diffs
            })
        
        return validations

    def _generate_adjustments(self, sync_results):
        """Generate required adjustments based on sync analysis."""
        adjustments = {
            "frontend": [],
            "backend": [],
            "critical": []
        }
        
        for result in sync_results:
            if result["status"] != "matched":
                if result["type"] == "api_contract":
                    self._handle_api_mismatch(result, adjustments)
                elif result["type"] == "data_model":
                    self._handle_model_mismatch(result, adjustments)
                elif result["type"] == "auth":
                    self._handle_auth_mismatch(result, adjustments)
        
        return adjustments

    def _handle_api_mismatch(self, result, adjustments):
        """Handle API contract mismatches."""
        if result["status"] == "missing_endpoint":
            adjustments["backend"].append({
                "type": "create_endpoint",
                "service": result["frontend_service"]
            })
        elif result["status"] == "method_mismatch":
            adjustments["critical"].append({
                "type": "api_method_mismatch",
                "service": result["frontend_service"],
                "details": result["methods"]
            })

    def _handle_model_mismatch(self, result, adjustments):
        """Handle data model mismatches."""
        if result["status"] == "missing_model":
            adjustments["backend"].append({
                "type": "create_model",
                "model": result["model_name"]
            })
        elif result["status"] == "property_mismatch":
            adjustments["critical"].append({
                "type": "model_property_mismatch",
                "model": result["model_name"],
                "details": result["property_diffs"]
            })

    def _handle_auth_mismatch(self, result, adjustments):
        """Handle authentication/authorization mismatches."""
        if result["type"] == "auth":
            adjustments["critical"].append({
                "type": "auth_mechanism_mismatch",
                "details": {
                    "frontend": result["frontend"],
                    "backend": result["backend"]
                }
            })