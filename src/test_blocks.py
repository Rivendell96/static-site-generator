import unittest
from blocks import block_to_block_type, BlockType

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
