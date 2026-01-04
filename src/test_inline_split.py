import unittest 
from textnode import TextNode, TextType, text_node_to_html_node
from inline_split import (split_nodes_delimiter, 
                          split_nodes_link, 
                          split_nodes_image,
                          extract_markdown_images,
                          extract_markdown_links,
                          text_to_textnodes)


class TestTextNodeSplitNodesDelimiter(unittest.TestCase):
    def test_spint_nodes_1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        excepted_nodes = [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("code block", TextType.CODE),
                          TextNode(" word", TextType.TEXT)
                          ]
        
        self.assertEqual(new_nodes, excepted_nodes)

    def test_spint_nodes_2(self):
        node = TextNode("**This is text** with a `code block` word", TextType.TEXT)
        bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_bold = [
                        TextNode("This is text", TextType.BOLD),
                        TextNode(" with a `code block` word", TextType.TEXT),
                        ]
        self.assertEqual(bold_nodes, expected_bold)

        code_nodes = split_nodes_delimiter(bold_nodes, "`", TextType.CODE)
        expected_full = [
            TextNode("This is text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(code_nodes, expected_full)

class TestExtractMarkdowntext(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        results = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(results, matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )
        results = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(results, matches)

class TestExtractMarkdownLinksAndImagesWithtext(unittest.TestCase):
    def test_split_nodes_link(self):
        #with missing closing Bracket 
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev",
            TextType.TEXT
        )
        results = split_nodes_link([node])
        excepted_results = [TextNode("This is text with a link ", TextType.TEXT, None), 
                   TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
                   TextNode(" and [to youtube](https://www.youtube.com/@bootdotdev", TextType.TEXT, None)]
        self.assertListEqual(results, excepted_results)

    def test_split_no_images(self):
        """
        Tests a node with only text and NO images.
        The function should return a list containing the original node.
        """
        node = TextNode("This is just plain text with no image links.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        # The result should be a list containing the single original node
        self.assertListEqual(
            [
                TextNode("This is just plain text with no image links.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        """
        Tests a node where the image link occurs at the very beginning of the text.
        The first element in the resulting list should be the image node.
        """
        node = TextNode(
            "![First image](https://i.imgur.com/start.png) followed by text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("First image", TextType.IMAGE, "https://i.imgur.com/start.png"),
                TextNode(" followed by text.", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTestToTextNode(unittest.TestCase):
    def test_text_to_textnode1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        results = text_to_textnodes(text)
        expected_results = [TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev")]
        
        self.assertListEqual(results, expected_results)




if __name__ == "__main__":
    unittest.main()