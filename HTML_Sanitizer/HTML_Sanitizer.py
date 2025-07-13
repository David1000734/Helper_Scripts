import os
import logging
import re


MAGENTA = "\033[35m"
GRAY = "\033[90m"
RESET = "\x1b[0m"
BLUE = "\033[34m"

log = logging.basicConfig(
    format=f"{GRAY} %(asctime)s  {BLUE}%(levelname)s  {MAGENTA}%(name)s: {RESET}%(message)s",   # noqa E501
    datefmt="%Y-%m-%d- %H:%M:%S",
    level=logging.INFO
)


def clean_quotation(content: str) -> str:
    logging.debug(f"Before clean_quotation:\n{content}")

    # Replace double quotations
    temp = re.sub(r'&[lr]d.*?;', '"', content)

    # Replace single quotations
    return re.sub(r'&[lr]s.*?;', "'", temp)


def clean_span(content: str) -> str:
    logging.debug(f"Before clean_span:\n{content}")

    # Remove all span but not it's content
    return re.sub(r'<span.*?>(.+?)<\/span>', r'\1', content)


def clean_style_1(content: str) -> str:
    logging.debug(f"Before clean_style_1:\n{content}")

    # Remove all styles from 1 character HTML element
    # For now, only <p>

    return re.sub(r'(<[p]) .*?>.*?', r'\1>', content)


def clean_style_2(content: str) -> str:
    logging.debug(f"Before clean_style_2:\n{content}")

    # Remove all styles from 2 character HTML elements
    # Only for those whos ending tag is on the SAME line
    temp = re.sub(r'(<[l][li]).*?>(.*?)(<\/.*>)', r'\1>\2\3', content)

    # Remove all styles from HTML elements with it's ending tag
    # on a new line
    #
    # NOTE: If specific HTML elements should be excluded from
    # cleaning, modify the character selectors.
    # Ex: Exclude ALL table elements -> Remove 't'
    # Ex: Exclude only table rows and data -> Remove 't' and 'd'
    temp = re.sub(r'(<[tou][lhrd]).*?>(.*?)', r'\1>', temp)

    return temp


def clean_p_space(content: str) -> str:
    logging.debug(f"Before clean_p_space:\n{content}")

    # Remove the paragraph with only a space there
    return re.sub(r'<p>?&nbsp;</p>', '', content, flags=re.M)


def clean_file(file_name: str) -> str:
    '''
    Function will provide a fully cleaned HTML file.

    :param file_name: File content
    '''
    print(f'Opening File "{file_name}" and starting clean.')

    file = open(file_name, "rt")

    content = file.read()
    content = clean_quotation(content)
    content = clean_span(content)
    content = clean_style_1(content)
    content = clean_style_2(content)
    content = clean_p_space(content)

    logging.debug(f"\nCleaned Return: {content}\n")

    print(f'"{file_name}" finished successfully.\n')
    file.close()

    return content


def specific_file():
    loop = True

    while (loop):
        try:
            file_name = input("Please provide the file name and extension: ")
            logging.debug(f"File provided \"{file_name}\"")

            if not (file_name.endswith('.html') or file_name.endswith('.txt')):
                raise ValueError("Only .html and .txt files are accepted, " +
                                 f"file recieved: \"{file_name}\"")

            # Remove the file extention if there is one
            # file_name = os.path.splitext(file_name)[0]

            # An exception is thrown if failed to open.
            parsed_file = clean_file(file_name)

            print(f'Successful clean, writting to {file_name}\n')

            # Write to file
            file = open(file_name, "wt")
            file.write(parsed_file)
            file.close()

            loop = False
        except FileNotFoundError as e:
            # Clear screen. Should work with other OS
            os.system('cls' if os.name == 'nt' else "printf '\033c'")

            print(f"{e}\n")

        except ValueError as e:
            # Clear screen. Should work with other OS
            os.system('cls' if os.name == 'nt' else "printf '\033c'")

            print(f"{e}\n")


def files_in_directory():
    loop = True

    # Collect files to consider for cleaning. No subdirectories
    files = os.listdir('.')
    # Only consider files that are html or txt
    files = [x for x in files if x.endswith('.html') or x.endswith('.txt')]

    while (loop):
        print(f"All {len(files)} file(s) will be modified: {files}.")
        confirm = input("Please verify the list as backups " +
                        "are NOT possible. Y/N\n").upper()

        match confirm:
            case "Y":
                for (idx, file_name) in enumerate(files):
                    parsed_file = clean_file(file_name)

                    # write to file
                    file = open(file_name, "wt")
                    file.write(parsed_file)
                    file.close()
                loop = False

            case "N":
                print("Goodbye!")
                loop = False

            case _:
                # Clear screen. Should work with other OS
                os.system('cls' if os.name == 'nt' else "printf '\033c'")

                print("Invalid selection, please enter Y or N.\n")


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

        if (not (selection < 3 and selection > -1)):
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
