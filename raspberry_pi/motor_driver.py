import os
import logging
import paho.mqtt.client as motor_server
motor_array = [[0 for row in range(3)]for column in range(3)]


file_name = os.path.basename(__file__)
motor_server_ip = '192.168.0.101'
motor_client = motor_server.Client(file_name)
value_segment = 3

# logging.basicConfig(format='%(asctime)s, %(levelname)s\t: %(message)s', filename=file_name+'.log', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s, %(levelname)s\t: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def send_data(string_data):
    logging.info('sending motor start command to the micro controller')
    logging.info('sending data matrix to the micro controller')
    # put your code

    logging.debug('data send to microcontroller is successfull')
    pass


def convert_data():
    logging.info('constructing data into string format')
    string_data = ''
    for row in range(3):
        for column in range(3):
            string_data = string_data+str(motor_array[row][column]) + ','
        string_data = string_data + ','
        pass
    logging.info('removing unwanted charector from the string')
    string_data = string_data.replace(",,", ",")
    logging.info('removing last charector from the string')
    string_data = string_data[:-1]
    print(string_data)
    print(string_data[:-1])
    logging.debug(
        'successfully converted string data : {}'.format(string_data))
    return string_data


def on_connect(motor_client, _, flags, rc):
    logging.info('connected with result code : {}'.format(rc))


def process_message(motor_client, _, msg):
    logging.info('stating data retrival algorithm')
    msg_topic = msg.topic.split('/')
    if(msg_topic[2] == 'enable'):
        logging.info('motor enable command found')
        send_data(convert_data())
        pass
    else:
        logging.debug('finding the z axis cordinate')
        logging.info('z axis cordant is : {}'.format(msg_topic[2]))
        logging.debug('finding the z axis value')
        motor_row = int(msg_topic[value_segment][0])
        motor_column = int(msg_topic[value_segment][1])
        motor_value = int(msg.payload.decode("utf-8"))
        motor_array[motor_row][motor_column] = motor_value
        logging.info('successfully found {}x{} axis value : {}'.format(
            motor_row+1, motor_column+1, motor_value))


def on_subscribe(motor_client, _, mid, granted_qos):
    logging.info('subscribed: {}, {}'.format(mid, granted_qos))


def run_main():
    motor_client.on_connect = on_connect
    motor_client.on_message = process_message
    motor_client.on_subscribe = on_subscribe
    motor_client.enable_logger(logger=None)

    motor_client.connect(motor_server_ip)

    motor_client.subscribe("thesis/motor/#", qos=0)
    motor_client.loop_forever()


pass


if __name__ == '__main__':
    logging.info('welcome to thesis {} script'.format(file_name))
    run_main()
    logging.info('leaving from thesis {} script'.format(file_name))
