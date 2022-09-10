from marvis import ArgumentParser, Network, DockerNode,SwitchNode, Scenario, InterfaceNode
from marvis.command_executor import SSHCommandExecutor

import paramiko


def prepare_mc(tty, ip, username, password, firmware, node_name):
    firmware_path = "firmware/" + firmware
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(ip, username=username, password=password)
    service_node = SSHCommandExecutor("service_node",client)
    service_node.execute(f"invoke erase-flash --tty '{tty}'")
    service_node.execute(f"invoke flash-image --tty '{tty}' --path '{firmware_path}'")
    service_node.execute(f"invoke reset-mc")
    service_node.execute(f"invoke set-sensor-name --name '{node_name}' --path 'MicroPython-smart-home-client/config.json'")
    service_node.execute(f"invoke copy-program --tty '{tty}' --src-path 'MicroPython-smart-home-client/' --dest-path ':' ")
    service_node.execute(f"invoke reset-mc")


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    switch = SwitchNode('br-1')

    # Note: Since Python connects to the docker daemon running on the host and not inside the marvis container
    # the volume mount path has to be absolute and the path on the host and not the one inside the container
    hass = DockerNode(
        'hass',
        docker_image='homeassistant/home-assistant:stable',
        volumes={'/home/lhoff/masterarbeit/smart-home-testbed/2-case-study/docker/hass/config': {'bind': '/config', 'mode': 'rw'}},
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
        'mpymqttclient1',
        docker_image='lhoff94/micropython-runtime:v1.18',
        volumes={'/home/lhoff/masterarbeit/smart-home-testbed/2-case-study/mpy/MicroPython-smart-home-client': {'bind': '/root/', 'mode': 'ro'}},
        command="micropython main.py 1"
    )
    channel_client1 = net.create_channel(delay="50ms")
    channel_client1.connect(mpymqttclient)
    channel_client1.connect(switch)

    # Setup Microcontroller
    # Microcontroller are connected to Raspberry Pi
    prepare_mc("/dev/ttyUSB1","172.16.0.107","pi", "pi-passwd", "esp32-v1.18.bin", "ESP-1" )

    @scenario.workflow
    def cycle_version(workflow):
        workflow.sleep(330)
        mpymqttclient.docker_image = 'lhoff94/micropython-runtime:v1.19'
        prepare_mc("/dev/ttyUSB1","172.16.0.107","pi", "pi-passwd", "esp32-v1.19.bin", "ESP-1" )
        mpymqttclient.build_docker_image()
        workflow.sleep(330)
        mpymqttclient.docker_image = 'lhoff94/micropython-runtime:v1.19.1'
        prepare_mc("/dev/ttyUSB1","172.16.0.107","pi", "pi-passwd", "esp32-v1.19.1.bin", "ESP-1" )
        mpymqttclient.build_docker_image()

    scenario.add_network(net)


    with scenario as sim:
        # The test runtime is 
        sim.simulate(990)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
