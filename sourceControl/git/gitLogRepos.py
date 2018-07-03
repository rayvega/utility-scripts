#!/usr/bin/env python
"""
get logs from git repos

- generates files containing commit logs for a specified author and date from each repo under a specified directory 
"""

import os
import subprocess
import argparse
from datetime import date

# command line args
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--repos-directory", help="parent directory of all git repos. default is current directory", default=os.getcwd())
parser.add_argument("-o", "--output", help="directory to output log results. default is current directory", default=os.getcwd())
parser.add_argument("-a", "--author", help="author name of commits", required=True)
parser.add_argument("-s", "--startdate", help="start datetime of git logs. format --> YYYY-MM-DD HH:MM. default is today's date", default=date.today().strftime("%Y-%m-%d %H:%M"))
args = parser.parse_args()

repos_root_dir = args.repos_directory
results_root_dir = args.output
author_name = args.author
start_date = args.startdate

if not os.path.isdir(repos_root_dir):
    print("git repo root directory does not exist: {0}".format(repos_root_dir))
    quit()

repo_names = [
    name
    for name in os.listdir(repos_root_dir)
    if os.path.isdir(os.path.join(repos_root_dir, name))
]

if not repo_names:
    print("no repo directories found at {0}".format(repos_root_dir))
    quit()

if not author_name:
    print("\nno author name specified!\n")
    parser.print_help()
    quit()

os.makedirs(results_root_dir, exist_ok=True)

for repo_name in repo_names:
    print("-" * 80)
    print("")

    # run git log
    repo_file_path = os.path.join(repos_root_dir, repo_name)
    print("getting logs starting from {0} since {1}...".format(repo_file_path, start_date))

    # check if directory is a git repo
    git_rev_parse_command = ['git', 'rev-parse', '--is-inside-work-tree']
    git_repo_process = subprocess.Popen(git_rev_parse_command, stdout=subprocess.PIPE,
                                        cwd=repo_file_path, universal_newlines=True)
    git_repo_process_output = git_repo_process.communicate()[0]
    is_git_repo = str(git_repo_process_output.strip())

    if is_git_repo != "true":
        print("no git repo found under {0}. skipping".format(repo_file_path))
        continue

    # fetch latest commits
    git_fetch_command = ['git', 'fetch']
    git_fetch_process = subprocess.Popen(git_fetch_command, stdout=subprocess.PIPE, cwd=repo_file_path)
    git_fetch_process.wait()

    # get repo logs
    git_log_command = ['git', '--no-pager', 'shortlog', 'origin/master',
                       '--author={0}'.format(author_name), '--after="{0}"'.format(start_date)]
    print("running command: \n\t{0}".format(" ".join(git_log_command)))
    git_log_process = subprocess.Popen(git_log_command, stdout=subprocess.PIPE, cwd=repo_file_path)
    (git_log_process_output, git_log_process_error) = git_log_process.communicate()

    if not git_log_process_output:
        print("no git logs for {0}".format(repo_file_path))
        continue
        
    # output log to file
    simplified_repo_name = repo_name.replace('.', '').strip()
    results_file_name = "git_log_{0}_{1}.txt".format(str(date.today()), simplified_repo_name)
    results_repo_file_path = os.path.join(results_root_dir, results_file_name)

    print("creating log file {0}...".format(results_repo_file_path))
    file_ = open(results_repo_file_path, "wb")
    file_.write(git_log_process_output)
    file_.close()

print("-" * 80)
print("")
print("done!")

