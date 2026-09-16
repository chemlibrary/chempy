import os
from chempy import files
#from chempy.files import parent_path, file_name, file_extension, file_safe_write


def detect_indentation(path:str) -> int:
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
        whitespace_count = 0
        for line in lines:
            ## Identify the indentation by counting leading whitespace
            leading_whitespace = len(line) - len(line.lstrip(' '))
            if leading_whitespace > 0:
                if whitespace_count == 0:
                    whitespace_count = leading_whitespace
                elif whitespace_count != leading_whitespace:
                    print(f"Warning: Mixed indentation found - {leading_whitespace} whitespaces on a line with {whitespace_count} whitespaces.")
                    return
                ## Stop counting after finding the first indent
                break
        if whitespace_count > 0:
            return whitespace_count
        else:
            return None
    except FileNotFoundError:
        print("The specified file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def sort_methods(path:str) -> bool:
    try:
        indent_size = detect_indentation(path)
    except:
        return False

    try:
        with open(path, 'r') as file:
            lines = file.readlines()
        current_block = []
        blocks = []
        imports = []
        top_level = []
        commented = []
        open_comment = False
        for line in lines:
            indent = len(line) - len(line.lstrip())
            if indent == 0 and line != '':
                ## Handle multiline comments with zero indent
                if line[:3] == '"""' or (line[:3] == "'''" or line[:3] == '```'):
                    if open_comment:
                        current_block.append(line)
                        commented.append(''.join(current_block))
                        current_block = []
                        open_comment = not(open_comment)
                    elif len(current_block) > 0:
                        blocks.append(''.join(current_block))
                        current_block = [line]
                        open_comment = not(open_comment)
                ## Handle multiline comment contents
                elif open_comment:
                    current_block.append(line)
                else:
                    if line[0] == '#':
                        continue
                    ## Handle imports
                    elif (line[:4] == 'from' or line[:6] == 'import'):
                        blocks.append(''.join(current_block))
                        current_block = []
                        imports.append(line)
                    ## Handle classes and methods
                    elif line[:3] != 'def' or line[:4] != 'class':
                        current_block.append(line)
                        top_level.append(''.join(current_block))
                        current_block = []
                    else:
                        blocks.append(''.join(current_block))
                        current_block = [line]
            else:
                current_block.append(line)
        if len(current_block) > 0:
            blocks.append(''.join(current_block))

        sorted_lines = imports + top_level + sorted(blocks) + commented
        sorted_contents = ''.join(sorted_lines)

        path = f'{parent_path(path)}{os.sep}{file_name(path, include_extension = False)}-sorted{file_extension(path)}'
        if file_safe_write(path, sorted_contents):
            return True
        return False
    except FileNotFoundError:
        print("The specified file does not exist.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
