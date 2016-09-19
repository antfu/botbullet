# Botbullet
A human-bot interface powered by [Pushbullet](https://www.pushbullet.com)

## Requirements
- [randomchars/pushbullet.py](https://github.com/randomchars/pushbullet.py)

## Get started
```python
from botbullet import Botbullet

bullect = Botbullet(your_api_token)

def callback(push, event_obj):
  # You can deal with 'push' here as you want
  print('> {}: {}'.format(push.sender_name, push.body))

# Start listening pushes
bullect.listen_pushes_asynchronously(callback)
```
When pushes come up
```
> Anthony Fu: Hello
> Anthony Fu: World
```

## More
For more details about pushbullet, you may like to have a look for:
- [randomchars/pushbullet.py](https://github.com/randomchars/pushbullet.py)
- [Pushbullet API](https://docs.pushbullet.com/)

## License
MIT
