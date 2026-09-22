from .submission_service import (
    detect_language,
    validate_submission,
    validate_python_syntax,
    validate_java_syntax,
    ACCEPTED_EXTENSIONS,
)

__all__ = [
    "detect_language",
    "validate_submission",
    "validate_python_syntax",
    "validate_java_syntax",
    "ACCEPTED_EXTENSIONS",
]
