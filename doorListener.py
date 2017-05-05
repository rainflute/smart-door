from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import os
import json
import door


class ShadowCallbackContainer:
    def __init__(self, client):
        self.client = client

    def call_back_delta(self, payload, responseStatus, token):
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict["state"])
        deltaMessage = self.handle(deltaMessage)
        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        self.client.shadowUpdate(newPayload, None, 5)

    def handle(self, deltaMessage):
        try:
            if deltaMessage == 'open':
                door.open()
            elif deltaMessage == 'lock':
                door.lock()
            return deltaMessage
        except RuntimeError:
            if deltaMessage == 'open':
                return 'lock'
            elif deltaMessage == 'lock':
                return 'open'

    def initializeDoor(self, payload):
        payloadDict = json.loads(payload)
        status = json.dumps(payloadDict["state"]['reported']['status'])
        status = self.handle(status)
        newPayload = '{"state":{"reported":' + status + '}}'
        self.client.shadowUpdate(newPayload, None, 5)

host = "a108by5cx6oj8b.iot.us-west-2.amazonaws.com"
keyPath = os.path.dirname(os.path.abspath(__file__)) + '/../keys'
rootCAPath = keyPath + '/root-CA.crt'
privateKeyPath = keyPath + '/door.private.key'
certificatePath = keyPath + '/door.crt.pem'

myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("door")
myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("door", True)

callbackContainer = ShadowCallbackContainer(Bot)
# Initialize door
Bot.shadowGet(callbackContainer.initializeDoor)
# Listen on deltas
Bot.shadowRegisterDeltaCallback(callbackContainer.call_back_delta)

# Loop forever
while True:
    pass
