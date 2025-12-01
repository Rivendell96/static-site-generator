from textnode import TextNode, TextType

def main():
    text = TextNode("hello world", TextType.LINK, "https://www.google.com")
    print(text)

if __name__ == "__main__":
    main()