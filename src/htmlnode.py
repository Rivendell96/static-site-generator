from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        
        result = ""
        for i in self.props.items():
            result += f' {i[0]}="{i[1]}"'
        return result
    

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self,tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("A Parent node must have a tag.")
        
        if self.children is None:
            raise ValueError("A Parent node must have a children node.")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
def text_node_to_html_node(text_node):
        simple_type_to_tag = {
        TextType.TEXT: None,
        TextType.BOLD: "b",
        TextType.ITALIC: "i",
        TextType.CODE: "code"
        }
    
        if text_node.text_type in simple_type_to_tag:
            tag = simple_type_to_tag[text_node.text_type]
            return LeafNode(tag, text_node.text) 
        
        elif text_node.text_type == TextType.LINK:
            tag = "a"
            props = {"href":text_node.url}
            return LeafNode(tag, text_node.text, None, props)
        
        elif text_node.text_type == TextType.IMAGE:
            tag = "img"
            props = {
                "src": text_node.url,
                "alt": text_node.text
            }
            return LeafNode(tag=tag, props=props)
        else:
            raise Exception(f"Invalid text type: {text_node.text_type}")
        