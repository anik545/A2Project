import os
import shutil
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

root_dir = '.'

out_dir = 'prints'
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.makedirs(out_dir)

py = get_lexer_by_name('python')
js = get_lexer_by_name('js')
html = get_lexer_by_name('html+jinja')
css = get_lexer_by_name('css')

endings = {'.py': py, '.js': js, '.html': html, '.css': css}

formatter = HtmlFormatter(noclasses=True)

full_file_content = ''
full_output_file = 'full_code.html'

exclude_dirs = ['.', '__', 'venv', 'board', 'img', 'image-picker', out_dir, 'tests']
exclude_files = [full_output_file, 'print_files', 'TODO', 'ttt.html', 'cttt.html', '.db', '.dll', 'open_idle', '.pdf', 'create_db']

for subdir, dirs, files in os.walk(root_dir, topdown=True):
    dirs[:] = [d for d in dirs if all([d.startswith(string) is False for string in exclude_dirs]) is True]

    files[:] = [f for f in files if f[0] != '.' and all((string in f) is False for string in exclude_files) is True]

    for f in files:
        full_path = os.path.join(subdir, f)
        print(full_path)
        name, filetype = os.path.splitext(f)
        lexer = endings.get(filetype, None)
        relative_path = os.path.relpath(full_path, '.')
        p = '>'.join(relative_path.split(os.sep))
        p = os.path.join(out_dir, p.split('.')[0])
        if lexer:
            with open(full_path, 'r') as read_file,  open(p + '.html', 'w') as write_file:
                heading = '<p style="font-size:14pt;font-family:sans-serif"><strong>'+full_path+'</strong></p>'
                code = heading+highlight(read_file.read(), lexer, formatter)
                full_file_content += code+'<br>'
                write_file.write(code)

with open('full_code.html', 'w') as final:
    final.write(full_file_content)

#https://cloudconvert.com/html-to-rtf
