"""Initialize the context for the templating."""


def generate_context():
    """Generate context."""

    return {
        "main_file_name": "test2",
        "main_folder_name": "Directory",
        "second_file": "file2",
        "user": "John Doe",
        "nested_folder": "My_Nested_Folder",
        "remove_test1_file": True,
    }
