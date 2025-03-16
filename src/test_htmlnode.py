import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode("a", 
                        "There was a time where...", 
                        None, 
                        {"class":"greeting", "href":"https://www.google.com"})
        self.assertEqual(node.props_to_html(),
                         ' class="greeting" href="https://www.google.com"')
        
    def test_print_without_children(self):
        node = HTMLNode("a", 
                        "There was a time where...", 
                        None, 
                        {"class":"greeting", "href":"https://www.google.com"})
        self.assertEqual(node.__repr__(),
                         "HTMLNode(tag=a, value=There was a time where..., children=None, {\'class\': \'greeting\', \'href\': \'https://www.google.com\'})")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        #node3 = LeafNode("a", "Click me!")
        #self.assertEqual(node2.to_html(), "can't be tag <a> without props")

if __name__ == "__main__":
    unittest.main()