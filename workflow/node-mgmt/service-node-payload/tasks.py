from invoke import task


@task
def get_file_list(c, port, baudrate):
    pass

@task
def clean_all(c, port, baudrate):
    
    pass

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


@task
def erase_flash(c, tty):
    c.run(f"esptool.py --port {tty} erase_flash")

@task(pre=[set_boot_mode], post=[unset_boot_mode])
def flash_image(c, tty, path):
    c.run(f"esptool.py --chip esp32 --port {tty} write_flash -z 0x1000 {path}")

@task
def wipe_root(c, tty):
    c.run(f"mpremote connect {tty} exec --no-follow \"import os, machine; os.umount('/'); os.VfsLfs2.mkfs(bdev); os.mount(bdev, '/'); machine.reset()\"")

@task
def copy_programm(c, tty, path):
    c.run()