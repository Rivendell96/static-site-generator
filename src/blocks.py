from enum import Enum
import re 
from textnode import text_node_to_html_node, TextType, TextNode
from inline_split import  text_to_textnodes
from htmlnode import HTMLNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST ="unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            stripped = line.lstrip()
            if stripped == "":
                continue
            if not stripped.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            stripped = line.lstrip()
            if stripped == "":
                continue
            if not stripped.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_tpye_to_html_tag(block_type, block):
    if block_type == BlockType.HEADING:
        hashtags_count = 0
        for ch in block:
            if ch == "#":
                hashtags_count += 1
            else:
                break
        return f"h{hashtags_count}"
    
    if block_type == BlockType.PARAGRAPH:
        return "p"
    
    if block_type == BlockType.QUOTE:
        return f"blockquote"
    
    if block_type == BlockType.UNORDERED_LIST:
        return f"ul"
    
    if block_type == BlockType.ORDERED_LIST:
        return f"ol"
    
    if block_type == BlockType.CODE:
        return None

    raise ValueError(f"unknown block type: {block_type}")

def prapre_block_to_inline_text_node(block, block_type):
    if block_type == BlockType.HEADING:
        block = block.lstrip("#")
        block = block.strip()
        return block

    if block_type == BlockType.QUOTE:
        block = block.lstrip(">")
        block = block.strip()
        return block

    if block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        block = " ".join(lines)
        return block

def code_block_to_html_node(block):
    lines = block.split("\n")
    inner_lines = lines[1:-1]
    text = "\n".join(inner_lines) + "\n"
    text_node = TextNode(text, TextType.TEXT)
    code_child = text_node_to_html_node(text_node)
    code_node = ParentNode(tag="code", children=[code_child], props=None)
    return ParentNode(tag="pre", children=[code_node], props=None)

def prapre_block_to_list_text_node(block, block_type):
    items = block.split("\n")
    list_items_textnodes = []

    for item in items:
        if block_type == BlockType.UNORDERED_LIST:
            text = item[2:]   # "- "
        else:
            text = item[3:]   # "1. ", "2. ", etc.

        text_nodes = text_to_textnodes(text)
        list_items_textnodes.append(text_nodes)

    return list_items_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_block = []

    for block in blocks:
        block_type = block_to_block_type(block)
        block_tag = block_tpye_to_html_tag(block_type, block)

        if block_type == BlockType.CODE:
            html_node_parent = code_block_to_html_node(block)
            html_node_block.append(html_node_parent)
            continue

        if (block_type == BlockType.PARAGRAPH or 
            block_type == BlockType.QUOTE or 
            block_type == BlockType.HEADING):

            block = prapre_block_to_inline_text_node(block, block_type)
            text_nodes = text_to_textnodes(block)

            html_nodes_childs = []
            for node in text_nodes:
                result = text_node_to_html_node(node)
                html_nodes_childs.append(result)

            html_node_parent = ParentNode(
                tag=block_tag,
                children=html_nodes_childs,
                props=None,
            )
            html_node_block.append(html_node_parent)

        elif (block_type == BlockType.ORDERED_LIST or 
              block_type == BlockType.UNORDERED_LIST):

            list_items_textnodes = prapre_block_to_list_text_node(block, block_type)

            li_nodes = []
            for item_textnodes in list_items_textnodes:
                li_children = []
                for tn in item_textnodes:
                    li_children.append(text_node_to_html_node(tn))
                li_nodes.append(
                   ParentNode(tag="li", children=li_children, props=None)
                )

            html_node_parent = ParentNode(
                tag=block_tag,
                children=li_nodes,
                props=None,
            )
            html_node_block.append(html_node_parent)
            

    # after processing ALL blocks, wrap them in <div>
    return ParentNode(
        tag="div",
        children=html_node_block,
        props=None,
    )

if __name__ == "__main__":
    with open("markdown_example.md", "r") as content:
        makrdown = content.read()
    result = markdown_to_html_node(makrdown)
    print(result.to_html())