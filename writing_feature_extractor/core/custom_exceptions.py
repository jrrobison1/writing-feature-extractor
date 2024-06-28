class FeatureExtractorError(Exception):
    """Base class for exceptions in the feature extractor."""

    pass


class FileOperationError(FeatureExtractorError):
    """Raised when file operations (read/write) fail."""

    pass


class ModelError(FeatureExtractorError):
    """Raised when there's an error related to the ML model."""

    pass


class GraphError(FeatureExtractorError):
    """Raised when there's a probllem graphing"""

    pass


class ConfigurationError(FeatureExtractorError):
    """Raised when there's an error in the configuration."""

    pass
