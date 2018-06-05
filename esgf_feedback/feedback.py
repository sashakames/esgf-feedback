from flask import Flask, request, abort
from time import sleep
#from json import loads
import os


app = Flask(__name__)

TASK_PID = os.getpid()

global counter
counter = 0



@app.route('/', methods=['POST'])
def feedback_srv():
    
    global counter
    path = request.path

#  TODO:  once we have a means to distribute tokens we can enable this
#    token = request.args.get('token')

#    if token != 'secret':
#        abort(401)

    data  = request.data
  
    fn = str(TASK_PID) + '.' +  str(counter) + '.json'

    written = False

    for i in range(5):


        try:
 
            with open('/tmp/' + fn, 'w') as outf: 
    
                outf.write(data)
                written = True
        except:
            sleep(.5)
        
        if written:
            break

    if not written:
        #Log an error
        abort(500)
    
        
    counter = counter + 1
    return ("OK")


if __name__ == '__main__':
    app.run()

