import socket
import time


class EmpaticaConnection:
    """ This class is responsible for the connection to the Empatica E4 device. """

    # if connecting to more empaticas, we need several sockets
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffer_size = 4096
    server_address = '127.0.0.1'
    port_number = 28000
    socket_connected = False

    def connect(self):
        """ Connect to the Empatica E4 device."""

        self.socket.settimeout(5)
        self._connect_empatica()
        self._subscribe_to_socket()
        self._stream()

    def _connect_empatica(self):
        """ Create the socket connection and connect the device to the socket """

        print("trying to connect")
        if not self.socket_connected:
            self.socket.connect((self.server_address, self.port_number))
            self.socket_connected = True

        self.socket.send("device_list\r\n".encode())
        response = self.socket.recv(self.buffer_size)

        print(response.decode('utf-8'))

        if ("Empatica_E4" not in response.decode('utf-8')):
            print ("found no empatica device, trying again after 10 seconds")
            time.sleep(10)
            return self.connect()

        # first possible device id, needs to be changed if there are multiple devices
        devicd_id = response.decode('utf-8').split(" ")[4]

        self.socket.send(f"device_connect {devicd_id}\r\n".encode())
        connected_response = self.socket.recv(self.buffer_size)
        print(connected_response.decode('utf-8'))

        if ("R device_connect OK" in connected_response.decode('utf-8')):
            # do we need to add the PAUSE ON command here?
            print("successfully connected to empatica")

    def _subscribe_to_socket(self):
            """ Subscribe to the data on the socket connection """

            print("subscribing to data")

            self.socket.send(("device_subscribe " + 'gsr' + " ON\r\n").encode())
            self.socket.recv(self.buffer_size)

            self.socket.send(("device_subscribe " + 'tmp' + " ON\r\n").encode())
            self.socket.recv(self.buffer_size)

            self.socket.send(("device_subscribe " + 'ibi' + " ON\r\n").encode())
            self.socket.recv(self.buffer_size)

            # if we did PAUSE ON, do PAUSE OFF here

    def _stream(self):
        """ Continuously receive data from the socket connection """

        print("streaming started")
        while True:
            try:
                response = self.socket.recv(self.buffer_size).decode("utf-8")
                if "connection lost to device" in response:
                    print("Lost connection to device, reconnecting in 10 sec...")
                    time.sleep(10)
                    return self.connect()
                if "turned off via button" in response:
                    print("The wristband was turned off, reconnecting in 10 sec...")
                    time.sleep(10)
                    return self.connect()

                samples = response.split("\n")
                for i in range(len(samples) - 1):
                    name = samples[i].split()[0]
                    data = float(samples[i].split()[2].replace(',', '.'))
                    # if name == "E4_Temperature":
                    #     self._send_data_to_subscriber("TEMP", data)
                    # elif name == "E4_Gsr":
                    #     self._send_data_to_subscriber("EDA", data)
                    # elif name == "E4_Hr":
                    #     self._send_data_to_subscriber("HR", data)
                    # elif name == "E4_Ibi":
                    #     self._send_data_to_subscriber("IBI", data)

            except socket.timeout:
                print("Socket timeout, reconnecting in 10 sec...")
                time.sleep(10)
                return self.connect()