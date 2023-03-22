from app.resolver import PropertyResolver

class EmptyPropertyResolver(PropertyResolver):
    def __init__(self):
        self.url = ''
        self.activities_url = ''
        self.streets_url = ''