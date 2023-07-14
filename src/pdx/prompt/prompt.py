class Prompt:
    def __init__(self, content: str = None, template: str = None, template_path: str = None, role: str = None, pointer: str = None):
        self.content = content
        self.template = template
        self.template_path = template_path
        self.role = role
        self.pointer = pointer
