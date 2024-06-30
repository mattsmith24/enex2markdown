import logging

from lxml import etree

logger = logging.getLogger("enex2markdown." + __name__)

class ENMLConverter:
    def __init__(self):
        pass

    def to_markdown(self, content: str) -> str:
        mdlines = []
        content = remove_xml_pi(content)
        root = etree.fromstring(content)
        assert root.tag == "en-note"
        mdlines += elem_to_markdown(root)
        return "\n".join(mdlines)

def remove_xml_pi(content):
    content_lines = content.splitlines()
    content_lines = [c.strip() for c in content_lines if "<?xml " not in c]
    return "\n".join(content_lines)

def elem_to_markdown(elem):
    mdlines = []
    if before_elem(elem, mdlines):
        if elem.text is not None and len(elem.text.strip()) > 0:
            mdlines.append(elem.text.strip())
        for child in elem:
            mdlines += elem_to_markdown(child)
    after_elem(elem, mdlines)
    if elem.tail is not None and len(elem.tail.strip()) > 0:
        mdlines.append(elem.tail.strip())
    return mdlines

def before_elem(elem, mdlines):
    if elem.tag == "a":
        text = elem.text.strip()
        url = elem.get('href')
        mdlines.append(f"[{text}]({url})")
        return False
    if elem.tag == "div":
        mdlines.append("")
        mdlines.append("")
    return True

def after_elem(elem, mdlines):
    if elem.tag == "div":
        mdlines.append("")
        mdlines.append("")
    elif elem.tag == "br":
        mdlines.append("")
        mdlines.append("")