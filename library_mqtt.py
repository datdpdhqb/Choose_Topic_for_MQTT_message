import json
import collections
import paho.mqtt.client as mqtt
import tkinter


class MqttClient(object):
    """Helper class to make it easier to work with MQTT subscriptions and publications."""
    def __init__(self, delegate=None):
        """
        Constructs the MQTT client and optionally connects a delegate object for message Rx.
        Notice that the delegate is optional.
        """
        self.client = mqtt.Client()
        self.delegate = delegate
        self.subscription_topic_name = None
        self.publish_topic_name = None
    def connect(self, subscription_suffix, publish_suffix,mqtt_broker_ip_address="test.mosquitto.org"):
        """
        Connect this MQTT client to the broker, note that connect_to_ev3 and connect_to_pc call this method.
        This connect method is the most generic allowing callers to set the subscription and publish topics.
        The lego_robot number is added to both the subscription and publish topics (as shown in the code below).
        Notice that the mqtt_broker_ip_address and lego_robot_number are optional (usually not set).
        Type hints:
          :type subscription_suffix: str
          :type publish_suffix: str
          :type mqtt_broker_ip_address: str
          :type lego_robot_number: int
        """
        topic_name = "mqtt"
        self.subscription_topic_name = topic_name + "/" + subscription_suffix
        self.publish_topic_name = topic_name + "/" + publish_suffix
        # Callback for when the connection to the broker is complete.
        self.client.on_connect = self._on_connect
        self.client.message_callback_add(self.subscription_topic_name, self._on_message)
        self.client.connect(mqtt_broker_ip_address, 1883, 60)
        print("Connecting to mqtt broker {}".format(mqtt_broker_ip_address), end="")
        self.client.loop_start()
    def send_message(self, function_name, parameter_list=None):
        """
        Sends a message to the MQTT broker using the publish_topic_name that was set by the connect method.
        What comes in:
          function_name: the name of the method that you want to call (as a string) on the other end's delegate
          parameter_list: a List containing the arguments to that method call. Note: even single arguments should be
                          placed into a list.  Also objects in the list will be transferred using json, so objects in
                          the list must be serializable (int, float, string, etc all work fine but nothing fancy)
        Type hints:
          :type function_name:  str
          :type parameter_list: list of object | None
        """
        message_dict = {"type": function_name}
        if parameter_list:
            if isinstance(parameter_list, collections.Iterable):
                message_dict["payload"] = parameter_list
            else:
                # Attempt to bail out users that pass a single item that was a non-list.
                # CONSIDER: Make this a feature and print no message. Just make it work.
                print("The parameter_list {} is not a list. Converting it to a list for you.".format(parameter_list))
                message_dict["payload"] = [parameter_list]
        message = json.dumps(message_dict)
        self.client.publish(self.publish_topic_name, message)
    # noinspection PyUnusedLocal
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("\nConnected!")
        else:
            print("\nError!!!")
            exit()
        print("Publishing to topic:", self.publish_topic_name)
        self.client.on_subscribe = self._on_subscribe

        # Subscribe to topic(s)
        self.client.subscribe(self.subscription_topic_name)

    # noinspection PyUnusedLocal
    def _on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed to topic:", self.subscription_topic_name)

    # noinspection PyUnusedLocal
    def _on_message(self, client, userdata, message):
        message = str(message.payload.decode("utf-8"))
        #msg_list.insert(tkinter.END, message)
        # print("Received message:", message)
        # Attempt to parse the message and call the appropriate function.
        try:
            message_dict = json.loads(message)
        except ValueError:
            print("Unable to decode the received message as JSON")
            return

        if "type" not in message_dict:
            print("Received a messages without a 'type' parameter.")
            return
        message_type = message_dict["type"]
        if hasattr(self.delegate, message_type):
            method_to_call = getattr(self.delegate, message_type)
            # Assumes that the user has the parameters correct.
            if "payload" in message_dict:
                message_payload = message_dict["payload"]
                attempted_return = method_to_call(*message_payload)
            else:
                attempted_return = method_to_call()
            if attempted_return:
                print("The method {} returned a value. That's not really how this library works." +
                      "The value {} was not magically sent back over".format(message_type, attempted_return))
        else:
            print("Attempt to call method {} which was not found.".format(message_type))
    def close(self):
        """
        Close the MQTT client (recommended of course, but does not seem to be required).
        """
        self.delegate = None
        self.client.loop_stop()
        self.client.disconnect()