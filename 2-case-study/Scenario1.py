from marvis import ArgumentParser, Network, DockerNode,SwitchNode, Scenario, InterfaceNode
from marvis.command_executor import SSHCommandExecutor

import paramiko

from marvis.marvis.channel.wifi import WiFiChannel


def prepare_mc(tty, ip, username, password, firmware):
    firmware_path = "firmware/" + firmware
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(ip, username=username, password=password)
    service_node = SSHCommandExecutor("service_node",client)
    service_node.execute(f"invoke erase-flash --tty '{tty}'")
    service_node.execute(f"invoke flash-image --tty '{tty}' --path '{firmware_path}'")
    service_node.execute(f"invoke reset-mc")
    service_node.execute(f"invoke set-sensor-name --name 'sensor-node-1', --path 'MicroPython-smart-home-client(config.json'")
    service_node.execute(f"invoke copy-program --tty '{tty}' --src-path 'MicroPython-smart-home-client/' --dest-path ':' ")


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    switch = SwitchNode('br-1')

    hass = DockerNode(
        'hass',
        docker_image='homeassistant/home-assistant:stable',
        volumes={'/home/lhoff/masterarbeit/smart-home-testbed/1-test-scenario/docker/hass/config': {'bind': '/config', 'mode': 'rw'}},
        exposed_ports={'8123':'8123'}
    )
    channel_sub = net.create_channel(delay="10ms", data_rate="1000Mbps")
    channel_sub.connect(hass)
    channel_sub.connect(switch)

    mosquittoserver = DockerNode('mosquittoserver', docker_build_dir='./docker/mosquitto', exposed_ports={'1883':'1883'})
    channel_server = net.create_channel(delay="10ms", data_rate="1000Mbps")
    channel_server.connect(mosquittoserver, "10.0.0.20")
    channel_server.connect(switch)

    external = InterfaceNode('external','enp8s0')
    channel_external = net.create_channel(delay="10ms", data_rate="100Mbps")
    channel_external.connect(external)
    channel_external.connect(switch)

    mpymqttclient = DockerNode(
        'mpymqttclient 2',
        docker_image='lhoff94/micropython-runtime:latest',
        volumes={'/home/lhoff/masterarbeit/smart-home-testbed/2-test-scenario/mpy/MicroPython-smart-home-client': {'bind': '/root/', 'mode': 'ro'}},
        command="micropython main.py 1"
    )
    channel_client1 = net.create_channel(delay="50ms", channel_type=WiFiChannel)
    channel_client1.connect(mpymqttclient)
    channel_client1.connect(switch)


    # Note: Since Python connects to the docker daemon running on the host and not inside the marvis container
    # the volume mount path has to be absolute and the path on the host and not the one inside the container


    # Setup Microcontroller
    # Microcontroller are connected to Raspberry Pi
    prepare_mc("/dev/ttyUSB0","172.16.0.107","pi", "pi-passwd", "esp32-v1.19.bin" )



    scenario.add_network(net)


    with scenario as sim:
        # The test runtime is 5 minutes with 30 seconds added as startup buffer
        sim.simulate(330)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
