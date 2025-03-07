import unittest
from textnode import TextNode,TextType

class TestTestNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("Hello world", TextType.ITALIC, "https://google.com")
        node2 = TextNode("Hello world", TextType.ITALIC, "https://google.com")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("Hello world", TextType.ITALIC, "https://google.com")
        node2 = TextNode("Hello world", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("Hello world", TextType.BOLD, "https://google.com")
        node2 = TextNode("Hello Boots", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

if __name__=="__main__":
    unittest.main()