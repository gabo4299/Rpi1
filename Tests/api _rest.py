
import paho.mqtt.publish as publish

s="{mesage:si}"

publish.single("test/node", s, hostname="localhost",port=1883)
# msgs = [{'topic':"test", 'payload222':"multiple 2"},("test", "multiple 2", 0, False)]

# publish.multiple(msgs, hostname="localhost")

