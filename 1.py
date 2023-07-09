import subprocess

packages = ['python-dotenv', 'rich', 'emoji', 'requests', 'dnspython']

for package in packages:
    try:
        subprocess.check_call(['pip', 'install', package])
        print('Successfully installed {}'.format(package))
    except subprocess.CalledProcessError as e:
        print('Failed to install {}: {}'.format(package, e))
