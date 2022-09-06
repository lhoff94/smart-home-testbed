from invoke import task
import time

@task 
def set_boot_mode(c, pin=23):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
@task
def unset_boot_mode(c, pin=23):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup()

@task
def reset_mc(c, pin=24):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.cleanup()

@task
def set_sensor_name(c, name, path):
    import json 
    with open(path, 'r') as file:
        json_data = json.load(file)
        json_data["sensor_name"] = name
    with open(path, 'w') as file:
        json.dump(json_data, file, indent=1)


@task(pre=[set_boot_mode], post=[unset_boot_mode])
def erase_flash(c, tty):
    c.run(f"esptool.py --port {tty} erase_flash")

@task(pre=[set_boot_mode], post=[unset_boot_mode])
def flash_image(c, tty, path):
    c.run(f"esptool.py --chip esp32 --port {tty} -b 460800 write_flash -z 0x1000 {path}")

@task
def wipe_root(c, tty):
    c.run(f"mpremote connect {tty} exec --no-follow \"import os, machine; os.umount('/'); os.VfsLfs2.mkfs(bdev); os.mount(bdev, '/'); machine.reset()\"")

@task
def copy_program(c, tty, src_path, dest_path):
    c.run(f"cd {src_path} && mpremote connect {tty} soft-reset cp -r ./* {dest_path}")

