import requests

host = 'http://0.0.0.0:8080'


def g(action, *args):
    url = host+'/'+action
    for arg in args:
        url += '/'+str(arg)
    r = requests.get(url)
    return r.json()


def write_i2c_block(address, block):
    return g('write_i2c_block', address, block)['return_value']


def writeNumber(value):
    return g('writeNumber', value)['return_value']


def readByte():
    return g('readByte', )['return_value']


def motor1(direction, speed):
    return g('motor1', direction, speed)['return_value']


def motor2(direction, speed):
    return g('motor2', direction, speed)['return_value']


def fwd():
    return g('fwd', )['return_value']


def motor_fwd():
    return g('motor_fwd', )['return_value']


def bwd():
    return g('bwd', )['return_value']


def motor_bwd():
    return g('motor_bwd', )['return_value']


def left():
    return g('left', )['return_value']


def left_rot():
    return g('left_rot', )['return_value']


def right():
    return g('right', )['return_value']


def right_rot():
    return g('right_rot', )['return_value']


def stop():
    return g('stop', )['return_value']


def increase_speed():
    return g('increase_speed', )['return_value']


def decrease_speed():
    return g('decrease_speed', )['return_value']


def trim_test(value):
    return g('trim_test', value)['return_value']


def trim_read():
    return g('trim_read', )['return_value']


def trim_write(value):
    return g('trim_write', value)['return_value']


def digitalRead(pin):
    return g('digitalRead', pin)['return_value']


def digitalWrite(pin, value):
    return g('digitalWrite', pin, value)['return_value']


def pinMode(pin, mode):
    return g('pinMode', pin, mode)['return_value']


def analogRead(pin):
    return g('analogRead', pin)['return_value']


def analogWrite(pin, value):
    return g('analogWrite', pin, value)['return_value']


def volt():
    return g('volt', )['return_value']


def brd_rev():
    return g('brd_rev', )['return_value']


def us_dist(pin):
    return g('us_dist', pin)['return_value']


def read_motor_speed():
    return g('read_motor_speed', )['return_value']


def led_on(l_id):
    return g('led_on', l_id)['return_value']


def led_off(l_id):
    return g('led_off', l_id)['return_value']


def servo(position):
    return g('servo', position)['return_value']


def enc_tgt(m1, m2, target):
    return g('enc_tgt', m1, m2, target)['return_value']


def enc_read(motor):
    return g('enc_read', motor)['return_value']


def fw_ver():
    return g('fw_ver', )['return_value']


def enable_encoders():
    return g('enable_encoders', )['return_value']


def disable_encoders():
    return g('disable_encoders', )['return_value']


def enable_servo():
    return g('enable_servo', )['return_value']


def disable_servo():
    return g('disable_servo', )['return_value']


def set_left_speed(speed):
    return g('set_left_speed', speed)['return_value']


def set_right_speed(speed):
    return g('set_right_speed', speed)['return_value']


def set_speed(speed):
    return g('set_speed', speed)['return_value']


def enable_com_timeout(timeout):
    return g('enable_com_timeout', timeout)['return_value']


def disable_com_timeout():
    return g('disable_com_timeout', )['return_value']


def read_status():
    return g('read_status', )['return_value']


def read_enc_status():
    return g('read_enc_status', )['return_value']


def read_timeout_status():
    return g('read_timeout_status', )['return_value']


def ir_read_signal():
    return g('ir_read_signal', )['return_value']


def ir_recv_pin(pin):
    return g('ir_recv_pin', pin)['return_value']


if __name__ == '__main__':
    pass
