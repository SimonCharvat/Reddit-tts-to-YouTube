
import pandas

def wrap_long_text(text, max_line_len, line_count):
    """
    Description
    ---------
    Input is long text that will be separated to list by "\\n".

    Parameters
    ---------
    text : str
        String containing text to be split into lines
    
    max_line_len : int
        Integer setting the maximum number of characters per line
    
    line_count : int
        Number of lines per page/image
    
    Returns
    ---------
    Returns list of list of strings (nested list). Inner lists represent one page/image and include strings (lines).
    """


    lines = []
    for line in text.split("\n"):
        if len(line) <= max_line_len:
            lines.append(line)
            continue
        else:
            split_idx = line.rfind(" ", 0, max_line_len) # index where to split string (whitespace char)
            split_check = line.find(" ", max_line_len) # next occurence of whitespace after split index


            if split_check - split_idx > max_line_len or split_check == -1: # next word is larger than max_line_len (must be split)
                lines.append(line[0:max_line_len])
                lines.append(wrap_long_text(line[max_line_len:], max_line_len, line_count))
                continue
            else:
                lines.append(line[0:split_idx])
                lines.append(wrap_long_text(line[split_idx + 1 :], max_line_len, line_count))
    
    
    sep_lines_list = []


    while len(flatten(lines)):
        sep_lines_list.append(lines[0:line_count])
        del lines[0:line_count]


    return sep_lines_list




def flatten(items, seqtypes=(list, tuple)):
    """
    Credits:
    -----------
    https://stackoverflow.com/a/10824086/14640064
    """

    for i, x in enumerate(items):
        while i < len(items) and isinstance(items[i], seqtypes):
            items[i:i+1] = items[i]
    return items



""" 
string_tmp = pandas.read_csv("./texts/talesfromtechsupport.csv", sep=";")["text"][5]

print(string_tmp)

a = wrap_long_text(string_tmp, 63, 21)

print(a)


print("")
 """