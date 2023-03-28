import datetime
import subprocess
import string
import random
import json

def terminalCall(commandCall, returnData=None):
    try:
        prCall = subprocess.check_output(
            args=commandCall,
            universal_newlines=True,
            shell=True
        )

        output = prCall

        if returnData == 1:
            return json.loads(output)
        elif returnData ==2:
            return str(output)

    except Exception as e:
        print(e)

        raise Exception("Cannot complete command line call: \n" + commandCall)
