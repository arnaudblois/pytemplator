"""Exceptions for Pytemplator."""


class UserCancellationError(Exception):
    """Exception returned when the user cancels the operation."""


class InvalidInputError(Exception):
    """Exception returned when user input is invalid."""


class BrokenTemplateError(Exception):
    """Exception returned when the template is invalid."""


class NoInputOptionNotHandledByTemplateError(Exception):
    """Exception returned when a template doesn't handle the no-input option."""
