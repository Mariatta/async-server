import os
import aiohttp
import subprocess
from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

router = routing.Router()

@router.register("issues", action="opened")
@router.register("issues", action="reopened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    author = event.data["issue"]["user"]["login"]
    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    issue_comment_url = event.data["issue"]["comments_url"]
    await gh.post(issue_comment_url,
            data={
                "body": message
            })

async def main(request):
    body = await request.read()

    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    event = sansio.Event.from_http(request.headers, body, secret=secret)
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "mariatta",
                                  oauth_token=oauth_token)
        await router.dispatch(event, gh)
    return web.Response(status=200)

async def setup_cpython_repo(app):
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
    else:
        print("cpython directory already exists")

if __name__ == "__main__":
    app = web.Application()
    app.router.add_post("/", main)
    app.on_startup.append(setup_cpython_repo)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
    print("running")