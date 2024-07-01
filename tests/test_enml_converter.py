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

def test_anchor_no_text():
    enml_converter = ENMLConverter()
    result = enml_converter.to_markdown(textwrap.dedent("""
        <en-note>
            <a href="http://helloworld.com"/>
        </en-note>
    """))
    assert result == "[http://helloworld.com](http://helloworld.com)"

def test_anchor_no_url():
    enml_converter = ENMLConverter()
    result = enml_converter.to_markdown(textwrap.dedent("""
        <en-note>
            <a>Hello World!</a>
        </en-note>
    """))
    assert result == ""

def test_div():
    enml_converter = ENMLConverter()
    result = enml_converter.to_markdown(textwrap.dedent("""
        <en-note>
            <div>Hello World!</div>
        </en-note>
    """))
    assert result == "\n\nHello World!\n\n"

def test_collapse_consecutive_blank_lines():
    enml_converter = ENMLConverter()
    result = enml_converter.to_markdown(textwrap.dedent("""
        <en-note>
            <div>
                <div>
                    



                    <div>Hello World!</div>
                    


                </div>
            </div>
        </en-note>
    """))
    assert result == "\n\nHello World!\n\n"
