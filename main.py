import subprocess

diffResult = subprocess.run(['git', 'diff', '--name-only', 'master..develop'], stdout=subprocess.PIPE).stdout.decode('utf-8')
