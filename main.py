import paramiko
import time
from yaml import safe_load
import os


# Given an open connection using the paramiko library then sending the appropriate command
# it waits for a second for the command to be processed
def send_cmd(conn, command):
    # conn >> paramiko SSH client object
    conn.send(command + "\n")
    time.sleep(1.0)

# As the send_cmd function, given an open connection, read all the data from the buffer and decode the byte string as UTF-8
def get_output(conn):
    return conn.recv(65535).decode("utf-8")

if __name__ == '__main__':

    # host_root now is a dict that contains information about our hosts/devices
    with open("hosts.yaml", "r") as handle:
        host_root = safe_load(handle)

    for host in host_root["host_list"]:
        # Paramiko is used as a client here
        conn_params = paramiko.SSHClient()
        # Just so paramiko doesn't refuse connection due to missing SSH keys
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(
            hostname=host["ipaddr"],
            port=22,
            username=host["hostname"],
            password=host["pass"], # Of course you shouldn't store your credentials like this but again just for the sake of simplicity
            look_for_keys=False,
            allow_agent=False,
        )

        # Get an interactive shell and wait a bit for the prompt to appear
        conn = conn_params.invoke_shell()
        time.sleep(1.0)
        print(f"{get_output(conn).strip()}")

        commands = [
            "show version",
            host["cmd"],
        ]
        # An empty string to collect the commands output and put them in a file
        concat_output = ""

        for command in commands:
            send_cmd(conn, command)
            concat_output += get_output(conn)

        conn.close()

        # Open a new txt file per host and write the output
        print(f"Writing {host['name']} facts to file")
        with open(f"{host['name']}_facts.txt", "w") as handle:
            handle.write(concat_output)




