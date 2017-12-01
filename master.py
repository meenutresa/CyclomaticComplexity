import web
import os
import MyApplication
import git

urls = (
    '/','master'
)

class master:
    #master class
    def GET(self):
        return

    def POST(self):
        return



if __name__ == "__main__":
    #get the repository and get the commit details. save that to a file
    repo = git.Repo("C:/Users/HP/Documents/GitHub/mlframework")
    commits_list = list(repo.iter_commits('master'))
    database = shelve.open('commit_details.dat')
    for commit in commits_list:
        database[commit.hexsha] = list(commit.stats.files.keys())
    #print(database['638d8fc545dc86af94edf1ec57f0102404ef9efe'])

    app = MyApplication.MyApplication(urls, globals())
    app.run(port=8080)
