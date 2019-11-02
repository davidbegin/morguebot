
import subprocess
process = subprocess.Popen("whoami", stdout=subprocess.PIPE)
output, error = process.communicate()
print(output.decode("utf-8"))
