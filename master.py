import web
import os
import MyWebApplication
import git

urls = (
    '/master','master'
)

class master:
    #master class
    def GET(self):
        return

    def POST(self):
        return

if __name__ == "__main__":
    #get the repository and get the commit details. save in a dictionary object
    repo = git.Repo("C:/Users/HP/Documents/GitHub/mlframework")
    commits_list = list(repo.iter_commits('master'))
    filelist_per_commit = {}
    for commit in commits_list:
        filelist_per_commit[commit.hexsha] = list(commit.stats.files.keys())
    print(filelist_per_commit['638d8fc545dc86af94edf1ec57f0102404ef9efe'])

    app = MyWebApplication.MyWebApplication(urls, globals())
    app.run(port=8080)
