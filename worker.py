import web
import git
import MyWebApplication
import lizard
import sys
import os

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
        return i.average_cyclomatic_complexity

    def POST(self):
        return

if __name__ == "__main__":
    #get the port
    port = int(sys.argv[1])
    app = MyWebApplication.MyWebApplication(urls, globals())
    app.run(port=port)
