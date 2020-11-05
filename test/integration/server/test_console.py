#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2020, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from io import BytesIO, StringIO

from pytest import fixture
from six import PY3

from py2neo.server.console import Neo4jConsole


@fixture
def captured():
    if PY3:
        return StringIO()
    else:
        return BytesIO()


@fixture
def console(neo4j_service, captured):
    con = Neo4jConsole(out=captured)
    con.verbosity = 1
    con.service = neo4j_service
    yield con


def test_console_env(console, caplog):
    console.env()
    assert "BOLT_SERVER_ADDR='localhost:7687'" in caplog.text
    assert "NEO4J_AUTH='neo4j:password'" in caplog.text


def test_console_ls(console, captured):
    console.ls()
    lines = captured.getvalue().splitlines(False)
    assert lines[0] == ("CONTAINER   NAME        BOLT PORT   "
                        "HTTP PORT   HTTPS PORT   MODE")
    assert "a.py2neo    7687        7474" in lines[1]


def test_console_help(console, captured):
    console.help()
    lines = captured.getvalue().splitlines(False)
    assert lines[0] == "Commands:"
    assert lines[1] == "  browser   Start the Neo4j browser."
    assert lines[2] == "  env       Show available environment variables."
    assert lines[3] == "  exit      Exit the console."
    assert lines[4] == "  help      Show general or command-specific help."
    assert lines[5] == "  logs      Display server logs."
    assert lines[6] == "  ls        Show server details."
