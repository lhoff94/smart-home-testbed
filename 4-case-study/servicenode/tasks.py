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
def set_boot_mode(c, pin="23"):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(int(pin), GPIO.OUT)
    GPIO.output(int(pin), GPIO.LOW)

@task(pre=[init_gpio]) 
def unset_boot_mode(c, pin="23"):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(int(pin), GPIO.OUT)
    GPIO.output(int(pin), GPIO.HIGH)
    GPIO.cleanup(int(pin))

@task(pre=[init_gpio]) 
def reset_mc(c, pin="24"):
    import RPi.GPIO as GPIO
    GPIO.setup(int(pin), GPIO.OUT)
    GPIO.output(int(pin), GPIO.LOW)
    time.sleep(1)
    GPIO.output(int(pin), GPIO.HIGH)
    GPIO.cleanup(int(pin))


@task(pre=[init_gpio]) 
def push_styrbar(c, button):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
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
    GPIO.setup(int(pin), GPIO.OUT)
    GPIO.output(int(pin), GPIO.LOW)
    time.sleep(0.1)
    GPIO.cleanup(int(pin))
    

@task(pre=[init_gpio])
def relay(c, num, state):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    if num == "one":
        pin = 15
    elif num == "two":
        pin = 14
    else:
        print("Unkown relay", file = sys.stderr)
        exit(1)
    GPIO.setup(int(pin), GPIO.OUT)
    if state == "on":
        GPIO.output(int(pin), GPIO.HIGH)
    elif state == "off":
        GPIO.output(int(pin), GPIO.LOW)
    else: 
        print("Unkown state", file = sys.stderr)
        exit(1)


@task(pre=[init_gpio])
def light_status(c,pin):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(int(pin), GPIO.IN)
    status = GPIO.input(int(pin))
    if status == 0:
        return True
    elif status == 1:
        return False


@task
def set_sensor_name(c, name, path):
    import json 
    with open(path, 'r') as file:
        json_data = json.load(file)
        json_data["node_name"] = name
    with open(path, 'w') as file:
        json.dump(json_data, file, indent=1)


@task
def erase_flash(c, tty, pin="23"):
    set_boot_mode(c, int(pin))
    c.run(f"esptool.py --port {tty} erase_flash")
    unset_boot_mode(c, pin)


@task
def flash_image(c, tty, path, pin="23"):
    set_boot_mode(c, int(pin))
    c.run(f"esptool.py --chip esp32 --port {tty} -b 460800 write_flash -z 0x1000 {path}")
    unset_boot_mode(c, int(pin))

@task
def wipe_root(c, tty):
    c.run(f"mpremote connect {tty} exec --no-follow \"import os, machine; os.umount('/'); os.VfsLfs2.mkfs(bdev); os.mount(bdev, '/'); machine.reset()\"")

@task
def copy_folder(c, tty, src_path, dest_path):
    c.run(f"cd {src_path} && mpremote connect {tty} cp -r ./* {dest_path}")

@task
def copy_file(c, tty, src_path, dest_path):
    c.run(f"mpremote connect {tty} cp {src_path} {dest_path}")

@task
def prepare_all(c, tty, fw_path, src_path, dest_path, boot_pin, reset_pin):
    erase_flash(c, tty, boot_pin)
    flash_image(c, tty, fw_path, boot_pin)
    reset_mc(c, reset_pin)
    copy_folder(c, tty, src_path, dest_path)
    reset_mc(c, reset_pin)


