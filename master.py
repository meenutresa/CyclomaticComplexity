import web
import os
import MyWebApplication
import git
import requests

urls = (
    '/master','master'
    '/register','register'
    '/work_done','work_done'
)

class master:
    #master class
    def GET(self):
        return

    def POST(self):
        #Give the work to the worker who has approached
        worker_address = web.input(hostid='',port='')
        work_details = filelist_per_commit[work_assigned_key]
        work_assigned_key = work_assigned_key+1
        url = "http://" + str(worker_address.hostid) + ":"+ str(worker_address.port)+":/worker?id="+str(work_details[0])+"&filename="+str(work_details[1])
        requests.get(url)
        return "work assigned"
class register:
    #register class for the workers to register
    def GET(self):
        return

    def POST(self):
        #regiser the worker
        no_of_workers = no_of_workers+1
        return "active"
class work_done:
    #register class for the workers to register
    def GET(self):
        return

    def POST(self):
        #get the result from the worker and add to cc_total to get the total
        #if all the works are done, then the average is taken
        cyclomatic_complexity = web.input(cc='')
        work_done_count = work_done_count+1
        cc_total = cc_total + int(cyclomatic_complexity.cc)
        if work_done_count == len(filelist_per_commit):
            cc_average = cc_total/work_done_count
        return "received result successfully"

no_of_workers = 0
filelist_per_commit = {}
work_assigned_key=1
work_done_count = 0
cc_total = 0
if __name__ == "__main__":
    #get the repository and get the commit details. save in a dictionary object
    repo = git.Repo("C:/Users/HP/Documents/GitHub/mlframework")
    commits_list = list(repo.iter_commits('master'))
    i=1
    for commit in commits_list:
        for file_key in commit.stats.files.keys():
            filelist_per_commit[i] = [commit.hexsha,file_key]
            i=i+1
    print(len(filelist_per_commit))

    app = MyWebApplication.MyWebApplication(urls, globals())
    app.run(port=8080)
