#!/usr/bin/python

# from fabric import Connection
# conn = Connection('linux.csc.uvic.ca',
#                   user='shoya', connect_kwargs={'password': 'arag0rn'})
# result = conn.run('psql -U shoya -h studentdb1.csc.uvic.ca\nV00730770')
# msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
# print(msg.format(result), flush=True)


import wexpect
child = wexpect.spawn('cmd.exe')
child.expect('>')
child.sendline('ls')
child.expect('>')
print(child.before)
child.sendline('exit')

# from paramiko import SSHClient
# ssh = SSHClient()
# ssh.load_system_host_keys()
# ssh.connect('linux.csc.uvic.ca', username='shoya', password='arag0rn')
# # (stdin, stdout, stderr) = ssh.exec_command('ls\ncd csc110\nls')
# # print("\nstdout is:\n" + stdout.read().decode('ASCII') + "\nstderr is:\n" +
# # stderr.read().decode('ASCII'), flush=True)  # print the output of ls
# # command

# # (stdin, stdout, stderr) = ssh.exec_command('cd csc110')
# # print("\nstdout is:\n" + stdout.read().decode('ASCII') + "\nstderr is:\n" +
# #       stderr.read().decode('ASCII'), flush=True)
# # (stdin, stdout, stderr) = ssh.exec_command('ls')
# # print("\nstdout is:\n" + stdout.read().decode('ASCII') + "\nstderr is:\n" +
# #       stderr.read().decode('ASCII'), flush=True)


# # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
# #     "psql -U shoya -h studentdb1.csc.uvic.ca")
# # ssh_stdin.write('V00730770\n')
# # ssh_stdin.flush()
# # output = ssh_stdout.read().decode('ASCII')
# # print(output, flush=True)

# # ssh_stdin.write('V00730770\n')
# # ssh_stdin.flush('\d')
# # output = ssh_stdout.read().decode('ASCII')
# # print(output, flush=True)

# stdin, stdout, stderr = ssh.exec_command(
#     "ls")
# stdin.write('lol\n')
# stdin.flush()
# data = stdout.read().decode('ASCII')
# print(data)
