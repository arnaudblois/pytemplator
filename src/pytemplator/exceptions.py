"""Exceptions for Pytemplator.BlockingIOError($0)"""


class UserCancellationError(Exception):
    """Exception returned when the user cancels the operation."""


class BrokenTemplateError(Exception):
    """Exception returned when the template is invalid."""
