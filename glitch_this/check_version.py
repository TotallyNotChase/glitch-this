from urllib import request
import json

def is_uptodate(version):
    # Check pypi for the latest version number\
    try:
        contents = request.urlopen('https://pypi.org/pypi/glitch-this/json').read()
    except:
        # Connection issue
        # Silenty return True, update check failed
        return True
    data = json.loads(contents)
    latest_version = data['info']['version']

    return version == latest_version
    
