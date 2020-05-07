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

from enum import Enum

__all__ = ["DiagramStyle"]


class DiagramStyle(Enum):
    """
    The diagram style refer to a style used by the originating system for a diagram.  A diagram style describes
    information such as schematic, geographic, bus-branch etc.
    """

    # The diagram should be styled as a schematic view.
    SCHEMATIC = 0

    # The diagram should be styled as a geographic view.
    GEOGRAPHIC = 1

    @property
    def short_name(self):
        return str(self)[16:]