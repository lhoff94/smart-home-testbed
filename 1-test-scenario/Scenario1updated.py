from marvis import ArgumentParser, Network, DockerNode,SwitchNode, Scenario, InterfaceNode#, SimulationServer

import os

print(os.getcwd())

def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    switch = SwitchNode('br-1')


    # Note: Since Python connects to the docker daemon running on the host and not inside the marvis container
    # the volume mount path has to be absolute and the path on the host and not the one inside the container
    zigbee2mqtt = DockerNode(
        'zigbee2mqtt',
        docker_image='koenkk/zigbee2mqtt:1.18.1',
        volumes={
            '/home/lhoff/masterarbeit/smart-home-testbed/1-test-scenario/docker/zigbee2mqtt/data':{'bind':'/app/data','mode':'rw'},
            '/run/udev':{'bind':'/run/udev','mode':'ro'}
        },
        devices="/dev/ttyUSB1:/dev/ttyUSB1:rwm",
        exposed_ports={'8080':'8080'}
    )
    channel_server = net.create_channel(data_rate="1000Mbps")
    channel_server.connect(zigbee2mqtt)
    channel_server.connect(switch)
    
    
    

    mosquittoserver = DockerNode('mosquittoserver', docker_build_dir='./docker/mosquitto', exposed_ports={'1883':'1883'})
    channel_server = net.create_channel(data_rate="1000Mbps")
    channel_server.connect(mosquittoserver, "10.0.0.20")
    channel_server.connect(switch)

    #mpymqttclient = DockerNode('mpymqttclient', docker_build_dir='./docker/micropython/mpy-client')
    #channel_client = net.create_channel(delay="50ms", data_rate="100Mbps")
    #channel_client.connect(mpymqttclient)
    #channel_client.connect(switch)

    external = InterfaceNode('external','enp8s0')
    channel_external = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_external.connect(external)
    channel_external.connect(switch)

    # Note: Since Python connects to the docker daemon running on the host and not inside the marvis container
    # the volume mount path has to be absolute and the path on the host and not the one inside the container
    hass = DockerNode(
        'hass',
        docker_image='homeassistant/home-assistant:2021.4.0',
        volumes={'/home/lhoff/masterarbeit/smart-home-testbed/1-test-scenario/docker/hass/config2': {'bind': '/config', 'mode': 'rw'}},
        exposed_ports={'8123':'8123'}
    )
    channel_sub = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_sub.connect(hass)
    channel_sub.connect(switch)

    #bash = DockerNode('bash-attach', docker_build_dir='./docker/bash-attach')
    #channel_sub = net.create_channel(delay="50ms", data_rate="100Mbps")
    #channel_sub.connect(bash)
    #channel_sub.connect(bridge)

    #@scenario.workflow
    #def test(workflow):
    #    workflow.sleep(60)
    #      hass.restart_docker_container(scenario.simulation)


    scenario.add_network(net)
    #driver = SimulationServer(9000)
    #scenario.add_simulation_driver(driver)


    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
