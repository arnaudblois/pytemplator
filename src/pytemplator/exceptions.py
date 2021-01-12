"""Exceptions for Pytemplator."""


class UserCancellationError(Exception):
    """Exception returned when the user cancels the operation."""


class BrokenTemplateError(Exception):
    """Exception returned when the template is invalid."""
