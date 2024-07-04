# ENEX 2 Markdown

I developed this for myself after exporting a 4GB enex file from Evernote. My
notes are very simple so I haven't put a lot of effort into formatting the
markdown, the script just extracts the things I was interested in. Other devs
are welcome to adapt and expand this under the MIT license. I did try using
enex2md that I found on pypi but I could tell it was going to struggle with a
4GB file and it wasn't working for me on Windows.

If you want to run this:

```
cd enex2markdown
pipenv install
pipenv run pytest tests
pipenv run python enex2markdown.py INPUT_FILENAME
```

Help output:

```
usage: ENEX2Markdown [-h] [-o OUTPUT_DIR] [-l {debug,info,warning,error,critical}] input_filename

Converts an EXEX export file from Evernote to a directory of markdown files and attachments.

positional arguments:
  input_filename

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
  -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
```
