import web
import os
import MyWebApplication
import git
import requests
import threading

urls = (
    '/master',"master",
    '/register/',"register",
    '/work_done',"work_done"
)

class master:
    #master class
    def GET(self):
        return

    def POST(self):
        #Give the work to the worker who has approached
        print("inside post")
        worker_address = web.input(hostid='',port='')
        if web.config.work_assigned_key <= len(web.config.filelist_per_commit):
            web.config.lock.acquire()
            work_details = web.config.filelist_per_commit[web.config.work_assigned_key]
            web.config.work_assigned_key = web.config.work_assigned_key+1
            web.config.lock.release()
            url = "http://" + str(worker_address.hostid) + ":"+ str(worker_address.port)+"/worker?id="+str(work_details[0])+"&filename="+str(work_details[1])
            print(url)
            requests.get(url)
            return "work assigned"
        else:
            return "Nowork"
class register:
    #register class for the workers to register
    def GET(self):
        #regiser the worker
        web.config.no_of_workers = web.config.no_of_workers+1
        print("inside register")
        return "active"

    def POST(self):
        return
class work_done:
    #register class for the workers to register
    def GET(self):
        return

    def POST(self):
        #get the result from the worker and add to cc_total to get the total
        #if all the works are done, then the average is taken
        cyclomatic_complexity = web.input(cc='')
        web.config.lock.acquire()
        web.config.work_done_count = web.config.work_done_count+1
        web.config.cc_total = web.config.cc_total + float(cyclomatic_complexity.cc)
        web.config.lock.release()
        print("Recieved CC",cyclomatic_complexity.cc)
        print("web.config.work_done_count",web.config.work_done_count)
        print("len(web.config.filelist_per_commit)",len(web.config.filelist_per_commit))
        if web.config.work_done_count >= len(web.config.filelist_per_commit):
            cc_average = web.config.cc_total/web.config.work_done_count
            print("Average :",cc_average)
        return "received result successfully"

if __name__ == '__main__':
    no_of_workers = 0 #to count the number of workers
    filelist_per_commit = {} #to store commit and file in commit
    work_assigned_key=1 #to track how much work is assigned to workers
    work_done_count = 0 #to track hwo much work is completed by the workers
    cc_total = 0 #to summing cyclomatc complexity of each file
    #get the repository and get the commit details. save in a dictionary object

    app = MyWebApplication.MyWebApplication(urls, globals())
    web.config.update({"no_of_workers":0, "filelist_per_commit" : {},"work_assigned_key":1,"work_done_count" : 0,"cc_total" : 0,"lock": threading.Lock()})

    repo = git.Repo("C:/Users/HP/Documents/GitHub/mlframework")
    commits_list = list(repo.iter_commits('master'))
    i=1
    for commit in commits_list:
        for file_key in commit.stats.files.keys():
            if os.path.splitext(file_key)[1] not in [".txt",".md",".pdf",".csv",".pyc",""]:
                web.config.filelist_per_commit[i] = [commit.hexsha,file_key]
                i=i+1
    print(len(web.config.filelist_per_commit))

    app.run(port=8080)
