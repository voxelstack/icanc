import click
import json
import requests
import time
import tomli_w
from ..common.exception import NetworkException, NotFoundException
from ..common.rc import config
from ..tools.auth import get_auth

udebug_url = "https://www.udebug.com"

def fetch_testcases(judge, problem):
    auth = get_auth("icanc.udebug")

    user = auth["user"]
    password = auth["password"]
    if user is None or password is None:
        raise NotFoundException("config", "udebug auth", "Did you authenticate with icanc udebug auth?")
    
    auth = requests.auth.HTTPBasicAuth(user, password)

    src = {}
    click.echo("Downloading udebug testcases...")
    with click.progressbar(list_testcases(judge, problem, auth)) as testcases:
        time.sleep(0.2)
        for testcase in testcases:
            id = testcase["id"]
            user = testcase["user"]

            i = get_input(id, auth)
            time.sleep(0.2)
            o = get_output(id, auth)
            time.sleep(0.2)

            src[f"{id} by {user}"] = {"in": i, "out": o}

    return tomli_w.dumps(src)

def list_testcases(judge, problem, auth):
    udebug_config = config.get("udebug", {})
    min_votes = udebug_config.get("min_votes", 5)
    judge_aliases = udebug_config.get("judge_alias", {})
    judge_alias = judge_aliases.get(judge, judge)

    res = make_request(
        "input_api/input_list/retrieve.json",
        {"judge_alias":  judge_alias, "problem_id": problem},
        auth
    )

    return [r for r in res if int(r["Votes"]) >= min_votes]

def get_input(id, auth):
    res = make_request(
        "input_api/input/retrieve.json",
        {"input_id":  id},
        auth
    )
    
    return res[0]

def get_output(id, auth):
    res = make_request(
        "output_api/output/retrieve.json",
        {"input_id":  id},
        auth
    )

    return res[0]

def make_request(path, params, auth):
    res = requests.get(
        f"{udebug_url}/{path}",
        headers={"accept": "application/json"},
        params=params,
        auth=auth
    )
    if not res.ok:
        raise NetworkException(res.status_code, f"failed to fetch {path}", "Are your credentials correct, and do you have API access to udebug?" if res.status_code == 401 else None)
    
    return json.loads(res.content)
