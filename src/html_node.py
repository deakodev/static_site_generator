


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html to implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_pairs = self.props.items()
        props_list = list(map(lambda pair: f" {pair[0]}=\"{pair[1]}\"", props_pairs))
        return "".join(props_list)          

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})" 
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("all parent nodes must have a tag")
        if self.children is None:
            raise ValueError("all parent nodes must have a child")
        children = ""
        for child in self.children:
            children = children + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"