from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP(name="server")


@mcp.tool()
def create_folder(folder_name: str) -> str:
    """
    Creates a folder under c:/test/

    Parameters
    ----------
    folder_name : str
        Name of the folder to create

    Returns
    -------
    str
        Creation result message
    """
    import os

    folder_path = os.path.join("c:/test", folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return f"Folder '{folder_name}' has been created."
    else:
        return f"Folder '{folder_name}' already exists."


@mcp.tool()
def delete_folder(folder_name: str) -> str:
    """
    Deletes a folder under c:/test/

    Parameters
    ----------
    folder_name : str
        Name of the folder to delete

    Returns
    -------
    str
        Deletion result message
    """
    import os

    folder_path = os.path.join("c:/test", folder_name)
    if os.path.exists(folder_path):
        os.rmdir(folder_path)
        return f"Folder '{folder_name}' has been deleted."
    else:
        return f"Folder '{folder_name}' does not exist."


@mcp.tool()
def list_folders() -> list:
    """
    Returns the list of folders under c:/test/

    Returns
    -------
    list
        List of folders
    """
    import os

    folder_path = "c:/test"
    folders = [
        f
        for f in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, f))
    ]
    return folders


@mcp.tool()
def write_file(file_name: str, content: str) -> str:
    """
    Creates a file under c:/test/ and writes content to it.

    Parameters
    ----------
    file_name : str
        Name of the file to create (including extension)
    content : str
        Content to write to the file

    Returns
    -------
    str
        File writing result message
    """
    import os

    file_path = os.path.join("c:/test", file_name)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Content has been successfully written to file '{file_name}'."
    except Exception as e:
        return f"An error occurred while writing to the file: {str(e)}"


@mcp.tool()
def read_file(file_name: str) -> str:
    """
    Reads the content of a file under c:/test/

    Parameters
    ----------
    file_name : str
        Name of the file to read (including extension)

    Returns
    -------
    str
        File content or error message
    """
    import os

    file_path = os.path.join("c:/test", file_name)
    if not os.path.exists(file_path):
        return f"File '{file_name}' does not exist."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"An error occurred while reading the file: {str(e)}"


@mcp.tool()
def append_to_file(file_name: str, content: str) -> str:
    """
    Appends content to a file under c:/test/

    Parameters
    ----------
    file_name : str
        Name of the file to append to (including extension)
    content : str
        Content to append

    Returns
    -------
    str
        File append result message
    """
    import os

    file_path = os.path.join("c:/test", file_name)
    if not os.path.exists(file_path):
        return f"File '{file_name}' does not exist."

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Content has been successfully appended to file '{file_name}'."
    except Exception as e:
        return f"An error occurred while appending content to the file: {str(e)}"


@mcp.tool()
def list_files() -> list:
    """
    Returns the list of files under c:/test/

    Returns
    -------
    list
        List of files
    """
    import os

    folder_path = "c:/test"
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    return files


# Run server
if __name__ == "__main__":
    mcp.run()
