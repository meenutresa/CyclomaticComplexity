import web
import git
import MyWebApplication
import lizard
import sys
import os
import requests

urls = (
    '/worker','worker'
)

class worker:
    #worker class
    def GET(self):
        #gets the file and calculate cyclomatic complexity of the file
        args_passed = web.input(id='',filename="")
        print(args_passed.id)
        repo = git.Repo("C:/Users/HP/Documents/GitHub/mlframework")
        file_content = repo.git.show("%s:%s" % (args_passed.id, args_passed.filename))
        with open(args_passed.filename,"w") as tf:
            tf.write(file_content)
        #temp_file.write(file_content)
        tf.close()
        i = lizard.analyze_file(args_passed.filename)
        os.remove(args_passed.filename)
        print(i.average_cyclomatic_complexity)
        url = "http://localhost:8080/work_done?cc="+str(i.average_cyclomatic_complexity)
        workdone_response = requests.post(url)
        #return i.average_cyclomatic_complexity

    def POST(self):
        return


if __name__ == "__main__":
    #get the port
    host = sys.argv[1]
    port = int(sys.argv[2])
    app = MyWebApplication.MyWebApplication(urls, globals())
    app.run(port=port)
    #register the worker with the master
    register_response = requests.post("http://localhost:8080/register/")
    #if the worker is registered, then request for work from the master
    if register.response == 'active':
        url = "http://localhost:8080/master?hostid="+str(host)+"&port="+str(port)
        requests.post(url)
