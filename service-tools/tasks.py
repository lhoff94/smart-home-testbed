from invoke import task
import time
import sys

@task 
def init_gpio(c):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

@task
def defer_gpio(c):
    import RPi.GPIO as GPIO
    GPIO.cleanup()

@task(pre=[init_gpio]) 
def set_boot_mode(c, pin=23):
    import RPi.GPIO as GPIO
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@task(pre=[init_gpio]) 
def unset_boot_mode(c, pin=23):
    import RPi.GPIO as GPIO
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup(pin)

@task(pre=[init_gpio]) 
def reset_mc(c, pin=24):
    import RPi.GPIO as GPIO
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup(pin)

@task(pre=[init_gpio]) 
def push_styrbar(c, button):
    if button =="arrow_left":
        pin = 13
    elif button =="arrow_right":
        pin  = 6
    elif button =="on":
        pin = 26
    elif button =="off":
        pin = 5
    else:
        print("Unkown button", file = sys.stderr)
        exit(1)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.cleanup(pin)
    

@task(pre=[init_gpio])
def relay(c, num, state):
    import RPi.GPIO as GPIO
    if num == "one":
        pin = 15
    elif num == "two":
        pin = 14
    else:
        print("Unkown relay", file = sys.stderr)
        exit(1)
    GPIO.setup(pin, GPIO.OUT)
    if state == "on":
        GPIO.output(pin, GPIO.HIGH)
    elif state == "off":
        GPIO.output(pin, GPIO.LOW)
    else: 
        print("Unkown state", file = sys.stderr)
        exit(1)


@task
def set_sensor_name(c, name, path):
    import json 
    with open(path, 'r') as file:
        json_data = json.load(file)
        json_data["node_name"] = name
    with open(path, 'w') as file:
        json.dump(json_data, file, indent=1)


@task
def erase_flash(c, tty, pin=23):
    set_boot_mode(c, pin)
    c.run(f"esptool.py --port {tty} erase_flash")
    unset_boot_mode(c, pin)


@task
def flash_image(c, tty, path, pin=23):
    set_boot_mode(c, pin)
    c.run(f"esptool.py --chip esp32 --port {tty} -b 460800 write_flash -z 0x1000 {path}")
    unset_boot_mode(c, pin)

@task
def wipe_root(c, tty):
    c.run(f"mpremote connect {tty} exec --no-follow \"import os, machine; os.umount('/'); os.VfsLfs2.mkfs(bdev); os.mount(bdev, '/'); machine.reset()\"")

@task
def copy_program(c, tty, src_path, dest_path):
    c.run(f"cd {src_path} && mpremote connect {tty} soft-reset cp -r ./* {dest_path}")

