import unittest
from htmlnode import HTMLNode

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
        
if __name__ == "__main__":
    unittest.main()