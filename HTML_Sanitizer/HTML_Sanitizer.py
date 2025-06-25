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

def clean_quotation(content: str) -> str:
    logging.debug(f"\nBefore clean_quotation:\n{content}")

    # Replace double quotations
    temp = re.sub(r'&[lr]d.*?;', '"', content)

    # Replace single quotations
    return re.sub(r'&[lr]s.*?;', "'", temp)


def clean_file(file_name: str, remove_styles: bool) -> str:
    '''
    Function will provide a fully cleaned HTML file.

    :param file_name: File content
    :param remove_styles: Should "styles=..." be removed from <p>, <td> etc.
    '''

    file = open(file_name, "rt")

    content = file.read()
    content = clean_quotation(content)

    logging.debug(f"\nCleaned Return: {content}\n")

    return content

def specific_file():
    loop = True

    while (loop):
        try:
            file_name = input("Please provide the file name and extension: ")
            logging.debug(f"File provided \"{file_name}\"")

            if not (file_name.endswith('.html') or file_name.endswith('.txt')):
                raise ValueError(f"Only .html and .txt files are accepted, file recieved: \"{file_name}\"")

            # Remove the file extention if there is one
            # file_name = os.path.splitext(file_name)[0]

            # An exception is thrown if failed to open.
            parsed_file = clean_file(file_name, True)

            # Write to file
            file = open(file_name, "wt")
            file.write(parsed_file)

            loop = False
        except FileNotFoundError as e:
            print(f"{e}\n")
        
        except ValueError as e:
            print(f"{e}\n")


def files_in_directory():
    # Collect files to consider for cleaning. No subdirectories
    files = os.listdir('.')
    file_length = len(files)
    logging.debug(f"Files: {files}\tLength: {file_length}")


# User selection
selection = -1
loop = True

print("Hello, welcome to HTML cleaner. Please select an option.")
while (loop):
    # Menu
    print("0. Exit")
    print("1. Select a specific file.")
    print("2. Clean all HTML files in directory.")

    try:
        # Get user input
        selection = int(input())

        if (not(selection < 3 and selection > -1)):
            print("Number is out of range")
        else:
            loop = False
    except ValueError:
        print("Please enter a number.")
    except Exception as e:
        logging.warning(f"Unknown error: {e}")
        exit(1)

# Clear screen. Should work with other OS
os.system('cls' if os.name == 'nt' else "printf '\033c'")

match selection:
    case 0:
        print("Goodbye!")

    # Choose specific file
    case 1:
        specific_file()

    # Choose all HTML
    case 2:
        files_in_directory()

    case _ as e:
        logging.warning(f"You should not be here...\n{e}")
