from datetime import datetime

class Note:
    #the following comments are the class fields beign created on initialization
    # code : int
    # text : str
    # TODO: timestamp


    def __init__(self, code:int, text:str) -> None:
        self.code = code
        self.text = text
        self.time = datetime.now()

    def get_time(self):
        return self.time
    
    def update_time(self):
        self.time = datetime.now()

    def get_code(self) -> int:
        return self.code
    
    def get_text(self) ->str:
        return self.text
    
    def set_text(self, text):
        self.text = text
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Note):
            return self.get_code() == other.get_code() and self.get_text() == other.get_text()
        
    def __str__(self) -> str:
        return f"Note[code={self.code}, text='{self.text}']"
        