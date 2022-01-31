"""Initialize the context for the templating."""

from pytemplator.utils import Context
from pytemplator.utils import Question as Q


def generate_context(no_input: bool) -> dict:
    """Generate context."""

    context = Context()
    context.questions = [
        Q("main_file_name"),
        Q("main_folder_name", default=lambda: "Directory"),
        Q("second_file", default="DEFAULT", no_input_default="file2"),
        Q("user", no_input_default="John Doe"),
        Q("nested_folder", ask=False, default="My_Nested_Folder"),
    ]
    context.resolve(no_input)
    return context.as_dict()
