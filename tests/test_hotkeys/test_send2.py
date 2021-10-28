import time
from hotkeys import send
time.sleep(1)
start = time.time()

text = send('This is a really cool BIt of % text that I am sending to somewhere{enter}')
text.send()
