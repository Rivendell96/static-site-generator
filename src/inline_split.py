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

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(text):
    new_blocks = text.split("\n\n")
    new_blocks_without_space = map(str.strip, new_blocks)
    return list(new_blocks_without_space )


if __name__ == "__main__":
    text = """ This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
            """
    results = markdown_to_blocks(text)
    for i in results:
        print(f"{i} \n")