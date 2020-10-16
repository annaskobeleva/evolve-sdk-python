#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List

from zepben.cimbend.cim.iec61968.common.document import Document
from zepben.cimbend.util import get_by_mrid, nlen, ngen, safe_remove

__all__ = ["OperationalRestriction"]


class OperationalRestriction(Document):
    """
    A document that can be associated with equipment to describe any sort of restrictions compared with the
    original manufacturer's specification or with the usual operational practice e.g.
    temporary maximum loadings, maximum switching current, do not operate if bus couplers are open, etc.

    In the UK, for example, if a breaker or switch ever mal-operates, this is reported centrally and utilities
    use their asset systems to identify all the installed devices of the same manufacturer's type.
    They then apply operational restrictions in the operational systems to warn operators of potential problems.
    After appropriate inspection and maintenance, the operational restrictions may be removed.
    """
    _equipment: Optional[List[Equipment]] = None

    def __init__(self, equipment: List[Equipment] = None):
        if equipment:
            for eq in equipment:
                self.add_equipment(eq)

    @property
    def num_equipment(self):
        """
        Returns the number of `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` associated with this `OperationalRestriction`
        """
        return nlen(self._equipment)

    @property
    def equipment(self) -> Generator[Equipment, None, None]:
        """
        The `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` to which this `OperationalRestriction` applies.
        """
        return ngen(self._equipment)

    def get_equipment(self, mrid: str) -> Equipment:
        """
        Get the `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` for this `OperationalRestriction` identified by `mrid`

        `mrid` The mRID of the required `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment`
        Returns The `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._equipment, mrid)

    def add_equipment(self, equipment: Equipment) -> OperationalRestriction:
        """
        Associate an `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` with this `OperationalRestriction`

        `equipment` The `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` to associate with this `OperationalRestriction`.
        Returns A reference to this `OperationalRestriction` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `OperationalRestriction`.
        """
        if self._validate_reference(equipment, self.get_equipment, "An Equipment"):
            return self
        self._equipment = list() if self._equipment is None else self._equipment
        self._equipment.append(equipment)
        return self

    def remove_equipment(self, equipment: Equipment) -> OperationalRestriction:
        """
        Disassociate `equipment` from this `OperationalRestriction`.

        `equipment` The `zepben.cimbend.cim.iec61970.base.core.equipment.Equipment` to disassociate from this `OperationalRestriction`.
        Returns A reference to this `OperationalRestriction` to allow fluent use.
        Raises `ValueError` if `equipment` was not associated with this `OperationalRestriction`.
        """
        self._equipment = safe_remove(self._equipment, equipment)
        return self

    def clear_equipment(self) -> OperationalRestriction:
        """
        Clear all equipment.
        Returns A reference to this `OperationalRestriction` to allow fluent use.
        """
        self._equipment = None
        return self
