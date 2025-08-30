from time import time,sleep
from rich.console import Console
console = Console()
start_time = int(time())
def send_Msg(msg):
    if isinstance(msg, BaseMsg):
        console.print(msg, style=msg.style)
    else:
        print(msg)


class BaseMsg:
    def __init__(self, data: str):
        self._data = data
    
    @property
    def style(self) -> str:
        return '' 
        
    @property
    def data(self):
        return self._data
    
    def __str__(self):
        return self._data 
    
    def __len__(self):
        return len(self._data)
    def __eq__(self, other):
        if(self._data == other._data):
            return True
        else:
            return False
    def __add__(self, other):
        newdata = self._data + other._data
        if(isinstance(self,'BaseMsg')):
            return BaseMsg(newdata)
        elif(isinstance(self,'LogMsg')):
            return LogMsg(newdata)
        else:
            return WarnMsg(newdata)


class LogMsg(BaseMsg):
    def __init__(self, data):
        super().__init__(data)
        global start_time
        self._timestamp: int = (int(time()) - start_time) 
    @property
    def style(self) -> str:
        return 'default on yellow' 
    def __str__(self):
        return f"[{self._timestamp}]" + self._data

class WarnMsg(LogMsg):
    def __init__(self, data):
        super().__init__(data)
        global start_time
        self._timestamp: int = (int(time()) - start_time)
    @property
    def style(self) -> str:
        return 'white on red'
    def __str__(self):
        return '[!WARN]' + f"[{self._timestamp}]" + self._data
if __name__ == '__main__':
    m1 = BaseMsg('Normal message')
    sleep(2) #added sleeps to highlight time functionality
    m2 = LogMsg('Log')
    sleep(3) #added sleeps to highlight time functionality
    m3 = WarnMsg('Warning')
    send_Msg(m1)
    send_Msg(m2)
    send_Msg(m3)