import socket
import argparse
import subprocess
import os

class App:
    def __init__(self, c, h, p):
        self.controller_mode = c
        self.host = h
        self.port = p
        self.state = ""
        self.test_threads = os.cpu_count() 
        self.test_log = []
        self.test_results = []
        if self.controller_mode:
            self.state = "LISTENING"
            self.controller_state_machine()
        else:
            self.state = "CONNECT"
            self.node_state_machine()
    #
    # Contorller Logic
    #
    def controller_state_machine(self):
        match self.state:
            case "LISTENING":
                self.listen_for_nodes()
            case "PROMPT":
                self.prompt_for_test()
            case "DISPATCH":
                self.dispatch_workload()
            case "WAIT":
                self.wait_for_result()
            case "RESULTS":
                self.save_run()

    def listen_for_nodes(self):
        pass

    def prompt_for_test(self):
        pass

    def dispatch_workload(self):
        pass

    def wait_for_result(self):
        pass

    def save_run(self):
        pass

    def print_run(self):
        pass

    #
    # Node Logic
    #
    def node_state_machine(self):
        match self.state:
            case "CONNECT":
                self.connect_to_controller()
            case "WAIT":
                self.wait_for_dispatch()
            case "EXECUTE":
                self.execute_dispatch()
            case "RESULTS":
                self.send_results()
 
    def connect_to_controller(self):
        pass

    def wait_for_dispatch(self):
        pass

    def execute_dispatch(self):
        # Download and Compile stream.c
        # Make a function for this and check if already downloaded
        commands = [
            "mkdir ./tmp",
            "wget https://www.cs.virginia.edu/stream/FTP/Code/stream.c -O ./tmp/stream.c",
            "gcc -fopenmp -D_OPENMP ./tmp/stream.c -o ./tmp/stream",
        ]
        results = []
        for c in commands:
            sp = subprocess.run(c, capture_output=True, text=True, shell=True)
            results.append(sp)
        self.test_log.append(results)
        # Test Run for Each Thread Count
        # Move this logic to controller to sync tests
        for t in range(1, self.test_threads + 1):
            commands = [
                "export OMP_NUM_THREADS=%s" % str(t),
                "./tmp/stream"
            ]
            results = []
            for c in commands:
                sp = subprocess.run(c, capture_output=True, text=True, shell=True)
                results.append(sp)
            self.test_log.append(results)
            self.test_results.append(results[1].stdout)
        print(len(self.test_results))

    def send_results(self):
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("-c", help="Controller Mode", action="store_true")
    parser.add_argument("--host", help="IPv4 Address, default: \"0.0.0.0\"", type=str, default="0.0.0.0", required=False)
    parser.add_argument("--port", help="TCP Port 0-65535, default: 8787", type=int, default=8787, required=False)
    args = parser.parse_args()
    a = App(args.c, args.host, args.port)
    a.execute_dispatch()


