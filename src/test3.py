from pystray import Icon, Menu, MenuItem
from PIL import Image
image = Image.open('E.ico')
icon = Icon(name='test', icon=image, title='pystray App')
icon.run()
