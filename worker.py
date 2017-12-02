import web
import git
import MyWebApplication
import lizard
import sys
import os
import requests
import threading



class worker:
    #worker class
    def GET(self):
        #gets the file and calculate cyclomatic complexity of the file
        args_passed = web.input(id='',filename="")
        print(args_passed.id)
        repo = git.Repo("C:/Users/HP/Documents/GitHub/mlframework")
        file_content = repo.git.show("%s:%s" % (args_passed.id, args_passed.filename))
        print("args_passed.filename",args_passed.filename)
        temp_filename = str(args_passed.filename)+str(args_passed.id)
        with open(temp_filename,"w") as tf:
            tf.write(file_content)
        #temp_file.write(file_content)
        tf.close()
        i = lizard.analyze_file(temp_filename)
        os.remove(temp_filename)
        print("CC",i.average_cyclomatic_complexity)
        url = "http://localhost:8080/work_done?cc="+str(i.average_cyclomatic_complexity)
        workdone_response = requests.post(url)
        #return i.average_cyclomatic_complexity

    def POST(self):
        return

class MyWebAppRun(threading.Thread):
    def run (self):
        urls = (
            '/worker','worker'
        )
        app = MyWebApplication.MyWebApplication(urls, globals())
        app.run(port=port)


if __name__ == "__main__":
    #get the port
    host = sys.argv[1]
    port = int(sys.argv[2])
    print("main")
    MyWebAppRun().start()
    #register the worker with the master
    while True:
        register_response = requests.get("http://localhost:8080/register/")
        #if the worker is registered, then request for work from the master
        print(register_response.text)
        #print(register_response)
        if register_response.text == 'active':
            print("inside loop")
            url = "http://localhost:8080/master?hostid="+str(host)+"&port="+str(port)
            print(url)
            response = requests.post(url)
            if response.text == 'Nowork':
                break;

    print("returned from loop")
