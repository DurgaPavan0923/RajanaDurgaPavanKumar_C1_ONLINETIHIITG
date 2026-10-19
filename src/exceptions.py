"""Custom domain and system exceptions."""


class WaterMonitorError(Exception):
    """Base exception for water monitor package."""

    pass


class DataIntegrityError(WaterMonitorError):
    """Raised when data fails cryptographic checksum or schema verification."""

    pass


class InvalidTrackError(WaterMonitorError):
    """Raised when track assignment or auto-detection violates track assumptions."""

    pass


class DataLeakageError(WaterMonitorError):
    """Raised when data leakage or illicit split overlap is detected."""

    pass


class ModelPipelineError(WaterMonitorError):
    """Raised when model training, fitting, or inference encounters fatal error."""

    pass


class ConfigurationError(WaterMonitorError):
    """Raised when YAML configuration is invalid or missing required keys."""

    pass
