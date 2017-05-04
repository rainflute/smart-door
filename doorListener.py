from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import shadowCallBackContainer
import os

host = "a108by5cx6oj8b.iot.us-west-2.amazonaws.com"
keyPath = os.path.dirname(os.path.abspath(__file__)) + '/../keys'
rootCAPath = keyPath + '/root-CA.crt'
privateKeyPath = keyPath + '/door.private.key'
certificatePath = keyPath + '/door.cert.pem'

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

callbackContainer = shadowCallBackContainer.ShadowCallbackContainer(Bot)
# Initialize door
Bot.shadowGet(callbackContainer.initializeDoor)
# Listen on deltas
Bot.shadowRegisterDeltaCallback(callbackContainer.call_back_delta)

# Loop forever
while True:
    pass
