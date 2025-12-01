import unittest

from htmlnode import  HTMLNode, LeafNode, ParentNode


class TestHTMLtNode(unittest.TestCase):
    def test_eq(self):
        htmlnode1 = HTMLNode("b", "Bootsdev is the best", None, None)
        htmlnode2 = HTMLNode("b", "Bootsdev is the best", None, None)
        self.assertEqual(htmlnode1, htmlnode2)

    def test_not_eq(self):
        htmlnode1 = HTMLNode("b", "Bootsdev is the best", None, None)
        htmlnode2 = HTMLNode("p", "Bootsdev is the best", None, None)
        self.assertNotEqual(htmlnode1, htmlnode2)

    def test_to_html(self):
        htmlnode1 = HTMLNode("p", "Bootsdev is the best", None, {"href": "https://www.google.com",
                                                                 "target": "_blank",})
        expected_result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expected_result, htmlnode1.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        expected_result = "<p>Hello, world!</p>"
        self.assertEqual(expected_result, node.to_html())

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_result = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_result)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )