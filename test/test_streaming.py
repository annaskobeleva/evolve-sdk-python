"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""

import zepben.cimbend.streaming.streaming as streaming
import asyncio
import grpc 

class TestStreaming(object):

    def test_retrieve_network(self):
        """Test retrieve_network"""
        channel = grpc.insecure_channel('localhost:50051')
        network = asyncio.run(streaming.retrieve_network(channel))
        #print(network)