from textnode import TextNode, TextType
def main():
    text_node = TextNode("hello world", TextType.LINK, "www.devboot.com")
    print(text_node)

if __name__== "__main__":
    main()