import re
import jionlp as jio

def merge_newlines(text):
    return re.sub(r'\n+', '\n', text)

def clean_content(content):
    content = merge_newlines(content)
    content = content.strip()
    content = jio.remove_exception_char(content)
    content = jio.remove_redundant_char(content)
    return content

def percent_of_chinese(text):
    char_count = len(text)
    if char_count == 0:
        return 0.
      
    chinese_count = 0.
    for c in text:
        if jio.check_any_chinese_char(c):
            chinese_count += 1.
    return chinese_count / char_count



