import argparse
import subprocess
import textwrap

# example https://github.com/jtolds/git-treesame-commit/blob/master/git-treesame-commit

def run(cmd, input=""):
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  out, _ = proc.communicate(input)
  rv = proc.poll()
  if rv:
    raise subprocess.CalledProcessError(rv, cmd, out)
  return out


def parse_commit(commit):
  d = {}
  for line in commit.rstrip().split("\n"):
    line = line.rstrip()
    if not line:
      return d
    header, value = line.split(" ", 1)
    if header in ("tree", "author", "committer"):
      d[header] = value
  return d


def main():
  parser = argparse.ArgumentParser(description="Cherry Pick commits to multiple branch")
  parser.add_argument("branch", help="branch on with to cherry-pick on", action='append')
  parser.add_argument("-c", "--commit", help="the commit to cherry-pick", action='append')
  parser.add_argument("--remote", help="remote name, default:origin", action='store_const', const='remote')
  args = parser.parse_args()
  print(args)
  print("Fetching remote origin")
  result = run(["git", "fetch", "origin"])

  newparent = run(["git", "log", "--format=%H", "-1", "HEAD"]).strip()


if __name__ == "__main__":
  main()