import os, sys, logging
import re


MAGENTA = "\033[35m"
GRAY = "\033[90m"
RESET = "\x1b[0m"
BLUE = "\033[34m"

log = logging.basicConfig(
    format=f"{GRAY} %(asctime)s  {BLUE}%(levelname)s  {MAGENTA}%(name)s: {RESET}%(message)s",
    datefmt="%Y-%m-%d- %H:%M:%S",
    level=logging.DEBUG
)

def clean_file(file: str, remove_styles: bool) -> str:
    '''
    Function will provide a fully cleaned HTML file.

    :param file: File content
    :param remove_styles: Should "styles=..." be removed from <p>, <td> etc.
    '''



    return ""

def specific_file():
    file_name = input("Please provide the file name: ")
    logging.debug(f"File provided {file_name}")

    # Remove the file extention if there is one
    file_name = os.path.splitext(file_name)[0]

    # An exception is thrown if failed to open. file is valid
    parsed_file = clean_file(file_name, True)

    # Write to file
    file = open(file_name + ".html", "wt")
    file.write(parsed_file)


def files_in_directory():
    # Collect files to consider for cleaning. No subdirectories
    files = os.listdir('.')
    file_length = len(files)
    logging.debug(f"Files: {files}\tLength: {file_length}")


# User selection
selection = 0
loop = True

print("Hello, welcome to HTML cleaner. Please select an option.")
while (loop):
    # Menu
    print("1. Select a specific file.")
    print("2. Clean all HTML files in directory.")

    try:
        # Get user input
        selection = int(input())

        if (not(selection < 3 and selection > 0)):
            print("Number is out of range")
        else:
            loop = False
    except ValueError:
        print("Please enter a number.")
    except Exception as e:
        logging.warning(f"Unknown error: {e}")
        exit(1)

match selection:
    # Choose specific file
    case 1:
        specific_file()

    # Choose all HTML
    case 2:
        files_in_directory()

    case _:
        logging.warning("You should not be here...")
        exit(0)
