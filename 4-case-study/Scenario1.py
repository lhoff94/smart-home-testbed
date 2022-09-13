from asyncore import read
from marvis import ArgumentParser, Network, DockerNode,SwitchNode, Scenario, InterfaceNode, ServiceNode, SimulationServer

import logging
import time
logger = logging.getLogger(__name__)

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

    mpymqttclient1 = DockerNode(
        'mpymqttclient1',
        docker_image='lhoff94/micropython-runtime:latest',
        volumes={'/home/lhoff/masterarbeit/smart-home-testbed/4-case-study/MicroPython-smart-home-client': {'bind': '/root/', 'mode': 'ro'}},
        command="micropython main.py 1"
    )
    channel_client1 = net.create_channel(delay="50ms")
    channel_client1.connect(mpymqttclient1)
    channel_client1.connect(switch)

    mpymqttclient2 = DockerNode(
        'mpymqttclient2',
        docker_image='lhoff94/micropython-runtime:latest',
        volumes={'/home/lhoff/masterarbeit/smart-home-testbed/4-case-study/MicroPython-smart-home-client': {'bind': '/root/', 'mode': 'ro'}},
        command="micropython main.py 2"
    )
    channel_client1 = net.create_channel(delay="50ms")
    channel_client1.connect(mpymqttclient2)
    channel_client1.connect(switch)

    servicenode1 = ServiceNode(
        'servicenode1',
        ip='raspi',
        username='pi',
        password='pi-passwd',
        payload={
            "servicenode/tasks.py":"tasks.py",
            "servicenode/mock.py":"mock.py",
            "servicenode/config-esp1.json":"config-esp1.json",
            "servicenode/config-esp2.json":"config-esp2.json",
            "servicenode/esp32-20220618-v1.19.1.bin":"esp32-v1.19.1.bin"
        }
    )
    scenario.add_servicenode(servicenode1)

    @servicenode1.preparation
    def init_both_esps():
        servicenode1.execute_action("git clone https://github.com/lhoff94/MicroPython-smart-home-client.git")
        servicenode1.execute_action("invoke prepare-all --tty '/dev/ttyUSB1' --fw-path 'esp32-v1.19.1.bin' --src-path 'MicroPython-smart-home-client/' --dest-path ':' --boot-pin '23' --reset-pin '24'")
        servicenode1.execute_action("invoke copy-file --tty '/dev/ttyUSB1' --src-path 'config-esp1.json' --dest-path :config.json")
        servicenode1.execute_action("invoke prepare-all --tty '/dev/ttyUSB2' --fw-path 'esp32-v1.19.1.bin' --src-path 'MicroPython-smart-home-client/' --dest-path ':' --boot-pin '25' --reset-pin '8'")
        servicenode1.execute_action("invoke copy-file --tty '/dev/ttyUSB2' --src-path 'config-esp2.json' --dest-path :config.json")
        servicenode1.execute_action("python3 mock.py", type="asynchronous")

    @servicenode1.cleaning_up
    def defer_gpio():
        servicenode1.execute_action("invoke defer-gpio")
   
    driver = SimulationServer(9000)
    scenario.add_simulation_driver(driver)

    test_values = {
        "Luminance":119,
        "CO2":424,
        "Temperature": 28,
        "Pressure":1000009
    }

    @driver.app.get("/sensor-1/Luminance")
    async def read_luminance():
        return test_values["Luminance"]
        
    @driver.app.get("/sensor-1/CO2")
    async def read_luminance():
        return test_values["CO2"]

    @driver.app.get("/sensor-1/Temperature")
    async def read_luminance():
        return test_values["Temperature"]

    @driver.app.get("/sensor-1/Pressure")
    async def read_luminance():
        return test_values["Pressure"]   


    @scenario.workflow
    def change_values(workflow):
        for i in range(1,20):
            test_values["CO2"] = test_values.get("CO2") + 10
            test_values["Luminance"] = test_values.get("Luminance") + 5
            test_values["Temperature"] = test_values.get("Temperature") + 2
            test_values["Pressure"] = test_values.get("Pressure") + 300
            time.sleep(8)


    scenario.add_network(net)

    with scenario as sim:
        # The test runtime 6 minutes to cover in accordance to the workflow with additonal 30seconds for start-up
        sim.simulate(420)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
