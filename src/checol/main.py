import os
import fire
from checol.vcs import Git
from checol.gpt import Claude


def review(git_path: str = ".", diff_or_branch_name: str = "diff"):
    print("CTRL+C to exit.")
    git = Git(git_path)
    claude = Claude(
      api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    if diff_or_branch_name == "diff":
        diff = git.head_diff()
    else:
        diff = git.diff(diff_or_branch_name)
    print('Description > ', end='')
    description = input()
    if description:
        message = claude.send(f'{description}\n\n{diff}')
    else:
        message = claude.send(diff)
    while True:
        print('AI > ', end='')
        for line in message.content[0].text.split("\n"):
            print(line)
        print('You > ', end='')
        user_message = input()
        message = claude.send(user_message)


def main():
    if os.environ.get("ANTHROPIC_API_KEY") is None:
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return
    fire.Fire({'review': review})


if __name__ == "__main__":
    main()
