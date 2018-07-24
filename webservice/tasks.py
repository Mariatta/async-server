import asyncio
import aiojobs
import subprocess
import os

async def setup_cpython_repo():
    print("Setting up CPython repository")
    if "cpython" not in os.listdir("."):
        print("cloning")
        subprocess.check_output(
            f"git clone https://{os.environ.get('GH_AUTH')}:x-oauth-basic@github.com/Mariatta/cpython.git".split()
        )
        print("done cloning")
        subprocess.check_output(
            "git config --global user.email 'mariatta.wijaya@gmail.com'".split()
        )
        subprocess.check_output(
            ["git", "config", "--global", "user.name", "'Mariatta'"]
        )
        os.chdir("./cpython")
        subprocess.check_output(
            f"git remote add upstream https://{os.environ.get('GH_AUTH')}:x-oauth-basic@github.com/python/cpython.git".split()
        )
        print("Finished setting up CPython Repo")
        print(os.listdir("./cpython"))
    else:
        print("cpython directory already exists")

async def main():
    scheduler = await aiojobs.create_scheduler(limit=1)
    await scheduler.spawn(setup_cpython_repo())

    # gracefully close spawned jobs
    await scheduler.close()

asyncio.get_event_loop().run_until_complete(main())