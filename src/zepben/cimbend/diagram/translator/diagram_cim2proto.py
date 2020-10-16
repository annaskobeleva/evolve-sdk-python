#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram
from zepben.protobuf.cim.iec61970.base.diagramlayout.OrientationKind_pb2 import OrientationKind as PBOrientationKind
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramStyle_pb2 import DiagramStyle as PBDiagramStyle
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2 import DiagramObjectPoint as PBDiagramObjectPoint
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectStyle_pb2 import DiagramObjectStyle as PBDiagramObjectStyle

from zepben.cimbend.common.translator.util import mrid_or_empty
from zepben.cimbend.cim.iec61970.base.diagramlayout import Diagram, DiagramObject, DiagramObjectPoint
from zepben.cimbend.common.translator.base_cim2proto import identifiedobject_to_pb

__all__ = ["diagram_to_pb", "diagramobject_to_pb", "diagramobjectpoint_to_pb"]


# IEC61970 DIAGRAMLAYOUT #
def diagram_to_pb(cim: Diagram) -> PBDiagram:
    return PBDiagram(io=identifiedobject_to_pb(cim),
                     diagramStyle=PBDiagramStyle.Value(cim.diagram_style.short_name),
                     orientationKind=PBOrientationKind.Value(cim.orientation_kind.short_name),
                     diagramObjectMRIDs=[str(io.mrid) for io in cim.diagram_objects])


def diagramobject_to_pb(cim: DiagramObject) -> PBDiagramObject:
    return PBDiagramObject(io=identifiedobject_to_pb(cim),
                           diagramMRID=mrid_or_empty(cim.diagram),
                           identifiedObjectMRID=cim.identified_object_mrid,
                           diagramObjectStyle=PBDiagramObjectStyle.Value(cim.style.short_name),
                           rotation=cim.rotation,
                           diagramObjectPoints=[diagramobjectpoint_to_pb(io) for io in cim.points])


def diagramobjectpoint_to_pb(cim: DiagramObjectPoint) -> PBDiagramObjectPoint:
    return PBDiagramObjectPoint(xPosition=cim.x_position, yPosition=cim.y_position)


Diagram.to_pb = diagram_to_pb
DiagramObject.to_pb = diagramobject_to_pb
DiagramObjectPoint.to_pb = diagramobjectpoint_to_pb
