from marvis import ArgumentParser, Network, DockerNode, Scenario, ServiceNode #, SimulationServer


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0", base="0.0.0.2")
    net.block_ip_address("10.0.0.1")

    node1 = DockerNode('ping', docker_build_dir='./docker/ping')
    node2 = DockerNode('pong', docker_build_dir='./docker/ping')
    node3 = ServiceNode(
        'service',
        ip='172.16.0.104',
        username='pi',
        password='pi-passwd',
        payload={})
    channel = net.create_channel(delay="200ms")
    channel.connect(node1, "10.0.0.17")
    channel.connect(node2)

    scenario.add_network(net)
    #driver = SimulationServer(8080)
    #scenario.add_simulation_driver(driver)
    node3.execute_command(command = 'mock-mhz19.py')
    node3.execute_command(command = 'python3 -c "import sys; print(\'python test stdout\', file = sys.stdout)"')


    @scenario.workflow
    def turn_led_on(workflow):
        node3.execute_command(command = 'LED-on.py')
        workflow.wait_until(triggered)
        node3.execute_command(command = 'LED-off.py')

    @scenario.workflow
    def change_config(workflow):
        

    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate(simulation_time=30)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
