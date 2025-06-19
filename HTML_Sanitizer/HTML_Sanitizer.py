import os, sys, logging
# Menu, allow for the following:
# 1. Specifiy a specific file to clean
# 2. Clean all HTML files in directory (w/o subdirectories?)

# Color. There is a better way to do this...
MAGENTA = "\033[35m"
GRAY = "\033[90m"
RESET = "\x1b[0m"
BLUE = "\033[34m"

log = logging.basicConfig(
    format=f"{GRAY} %(asctime)s  {BLUE}%(levelname)s  {MAGENTA}%(name)s: {RESET}%(message)s",
    datefmt="%Y-%m-%d- %H:%M:%S",
    level=logging.DEBUG
)

def specific_file(files:list):
    pass

def files_in_directory(files:list):
    pass

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
        print(f"Unknown error: {e}")
        exit(1)

# Collect files to consider for cleaning. No subdirectories
files = os.listdir('.')
file_length = len(files)
logging.debug(f"Files: {files}Length: {file_length}")

match selection:
    # Choose specific file
    case 1:
        specific_file(files)
        files = input("Please provide the file name: ")

        pass

    # Choose all HTML
    case 2:
        pass
    
    case _:
        print("You should not be here...")
        exit(0)
