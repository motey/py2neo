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


class ByteReader(object):

    def __init__(self, s):
        self.socket = s
        self.buffer = bytearray()

    def read(self, n):
        while len(self.buffer) < n:
            self.buffer.extend(self.socket.recv(n))
        data = self.buffer[:n]
        self.buffer[:n] = []
        return data


class ByteWriter(object):

    def __init__(self, s):
        self.socket = s
        self.buffer = bytearray()

    def write(self, b):
        self.buffer.extend(b)

    def send(self):
        self.socket.sendall(self.buffer)
        self.buffer[:] = []

    def close(self):
        self.socket.close()
