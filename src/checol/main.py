import os
from typing import Optional

import fire
from halo import Halo

from checol.vcs import Git
from checol.gpt import Claude

spinner = Halo(text="Loading", spinner="dots")


def generate_response_from_claude(git_diff: str):
    print("Description > ", end="")
    model = "claude-3-haiku-20240307"
    if os.environ.get("ANTHROPIC_API_MODEL") is not None:
        model = os.environ.get("ANTHROPIC_API_MODEL")

    claude = Claude(api_key=os.environ.get("ANTHROPIC_API_KEY"), model=model)
    description = input()
    spinner.start()
    if description:
        message = claude.send(f"{description}\n\n{git_diff}")
    else:
        message = claude.send(git_diff)
    spinner.stop()
    while True:
        print("AI > ", end="")
        for line in message.content[0].text.split("\n"):
            print(line)
        print("You > ", end="")
        user_message = input()
        spinner.start()
        message = claude.send(user_message)
        spinner.end()


def uncommitted(staged: bool = False):
    git_path = os.getcwd()
    git = Git(git_path)
    uncommitted_diff = git.head_diff(staged=staged)
    generate_response_from_claude(uncommitted_diff)


def diff(branch: Optional[str] = None):
    git_path = os.getcwd()
    git = Git(git_path)
    diff = git.diff(branch)
    generate_response_from_claude(diff)


def main():
    if os.environ.get("ANTHROPIC_API_KEY") is None:
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return
    print("CTRL+C to exit.")
    fire.Fire({"uncommitted": uncommitted, "diff": diff})


if __name__ == "__main__":
    main()
