"""Bounded semantic routing for JSON FlowFiles sent through NiFi InvokeHTTP."""

import argparse
import json
import os
from wsgiref.simple_server import make_server

from jev import evaluate, normalize
from service import InputError, decide, make_app, open_state


def adapt(payload):
    if not isinstance(payload, dict):
        raise InputError("invalid_flowfile")
    event_id, text = payload.get("id"), payload.get("text")
    if not isinstance(event_id, str) or not isinstance(text, str):
        raise InputError("invalid_flowfile")
    return event_id, text, {"flowfile_id": event_id}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true")
    mode.add_argument("--serve", action="store_true")
    parser.add_argument("--state", default=".local/decisions.sqlite")
    args = parser.parse_args()
    with open("examples/policy.json", encoding="utf-8") as source:
        policy = json.load(source)
    if args.demo:
        with open("examples/flowfile.json", encoding="utf-8") as source:
            event = json.load(source)
        with open_state(":memory:") as db:
            print(
                json.dumps(
                    decide(
                        event,
                        adapt,
                        policy,
                        lambda _: normalize("incident", 0.97, policy),
                        db,
                    ),
                    indent=2,
                )
            )
        return
    key = os.environ["TYPESAFE_API_KEY"]
    app = make_app(
        adapt,
        policy,
        lambda text: evaluate(text, policy, key),
        args.state,
        os.environ["JEV_INGEST_TOKEN"],
    )
    with make_server("127.0.0.1", int(os.environ.get("PORT", "8096")), app) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
