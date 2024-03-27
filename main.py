import paramiko
import time


# Basically what this function does is opening a shell connection using the paramiko library and the sending the appropiate command
# and then it waits for a second for the command outputs
def send_comd(conn, command):
    conn.send(command + "\n")
    time.sleep(1.0)

if __name__ == '__main__':
    print_hi('PyCharm')

