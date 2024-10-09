import json
import re
import pyperclip


def generate_toc_from_ipynb(file_path):
    """function to generate a table of contents up to level 5from a Jupyter Notebook file - generated with support of fittencode: chat.

    Args:
        file_path(string): filepath to the Jupyter Notebook file.

    Returns:
        string: prepared table of contents up to level 5 as a string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        notebook_content = json.load(file)

    toc_lines = []
    for cell in notebook_content["cells"]:
        if cell["cell_type"] == "markdown":
            for line in cell["source"]:
                chapter_match = re.match(r"^(#+)\s*(.+)", line)
                if chapter_match:
                    level = len(chapter_match.group(1))
                    title = chapter_match.group(2).strip()
                    formatted_title = title.lower().replace(
                        " ", "-"
                    )  # Replace spaces with hyphens

                    if level == 1:  # Chapter
                        toc_line = f"* [{title}](#{formatted_title})"
                        toc_lines.append(toc_line)
                    elif level == 2:  # Section
                        toc_line = f"    * [{title}](#{formatted_title})"
                        toc_lines.append(toc_line)
                    elif level == 3:  # Sub Section
                        toc_line = f"        * [{title}](#{formatted_title})"
                        toc_lines.append(toc_line)
                    elif level == 4:  # Sub Sub Section
                        toc_line = f"            * [{title}](#{formatted_title})"
                        toc_lines.append(toc_line)
                    elif level == 5:  # Sub Sub Sub Section
                        toc_line = f"                * [{title}](#{formatted_title})"
                        toc_lines.append(toc_line)

    return "\n".join(toc_lines)


# Specify the path to your Jupyter Notebook file
toc = generate_toc_from_ipynb(
    "c:\\Users\\carst\\Unibox Rostock\\repositories\\DADM_lecture_STMC\\exercises\\STMC_all.ipynb"
)

# Copy the TOC to the clipboard
pyperclip.copy(toc)
print("Table of Contents copied to clipboard:")
print(toc)  # This will print the generated TOC
