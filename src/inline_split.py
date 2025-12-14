from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # for saprate link
        pattren = r"(\[.*?\]\(.*?\))"
        split_nodes = []
        sections = re.split(pattren, old_node.text)

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if len(re.findall(pattren, sections[i])) == 0:
                # checks if contain "[]()"
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            if len(re.findall(pattren, sections[i])) != 0:
                results = extract_markdown_links(sections[i])
                split_nodes.append(TextNode(f"{results[0][0]}", TextType.LINK, f"{results[0][1]}"))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # for saprate image
        pattren = r"(\!\[.*?\]\(.*?\))"
        split_nodes = []
        sections = re.split(pattren, old_node.text)

        for i in range(len(sections)):

            if sections[i] == "":
                continue

            if len(re.findall(pattren, sections[i])) == 0:
                # checks if contain "[]()"
                split_nodes.append(TextNode(f"{sections[i]}", TextType.TEXT))

            if len(re.findall(pattren, sections[i])) != 0:
                results = extract_markdown_images(sections[i])
                split_nodes.append(TextNode(f"{results[0][0]}", TextType.IMAGE, f"{results[0][1]}"))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

if __name__ == "__main__":
    node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev",
    TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    print(new_nodes)

    # node = TextNode("This is text with a `code block` word", TextType.TEXT)
    # new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    # print(new_nodes)
