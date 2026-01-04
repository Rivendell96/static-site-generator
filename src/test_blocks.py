import unittest
from blocks import block_to_block_type, BlockType, markdown_to_blocks, markdown_to_html_node

class TestBlockTypes(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        markdown = "# This is a heading"
        result = block_to_block_type(markdown)
        expected_result = BlockType.HEADING
        self.assertEqual(result, expected_result)

    def test_block_to_block_type_unordered_list(self):
        markdown = ("""- This is the first list item in a list block
                       - This is a list item
                       - This is another list item
                    """)
        result = block_to_block_type(markdown)
        print(result)
        expected_result = BlockType.UNORDERED_LIST
        self.assertEqual(result, expected_result)

    def test_block_to_block_type_ordered_list(self):
        markdown = ("""1. This is the first list item in a list block
                       2. This is a list item
                       4. This is another list item
                    """)
        result = block_to_block_type(markdown)
        expected_result = BlockType.PARAGRAPH
        # the list is not in order
        self.assertEqual(result, expected_result)

    def test_block_to_block_type_ordered_list2(self):
        markdown = ("""1. This is the first list item in a list block
                       2. This is a list item
                       3. This is another list item
                    """)
        result = block_to_block_type(markdown)
        expected_result = BlockType.ORDERED_LIST
        self.assertEqual(result, expected_result)

class TestMarkdownToText(unittest.TestCase):
    def test_markdown_to_blocks1(self):
        md = """
            This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):

        md = """
        # This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
        """
        blocks = markdown_to_blocks(md)
        expected_results = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        self.assertEqual(blocks, expected_results)
    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

