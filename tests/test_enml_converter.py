import textwrap

from enml_converter import ENMLConverter

def test_text():
    enml_converter = ENMLConverter()
    result = enml_converter.to_markdown(textwrap.dedent("""
        <en-note>
            Hello World!
        </en-note>
    """))
    assert result == "Hello World!"

def test_anchor():
    enml_converter = ENMLConverter()
    result = enml_converter.to_markdown(textwrap.dedent("""
        <en-note>
            <a href="http://helloworld.com">Hello World!</a>
        </en-note>
    """))
    assert result == "[Hello World!](http://helloworld.com)"

def test_div():
    enml_converter = ENMLConverter()
    result = enml_converter.to_markdown(textwrap.dedent("""
        <en-note>
            <div>Hello World!</div>
        </en-note>
    """))
    assert result == "\n\nHello World!\n\n"
