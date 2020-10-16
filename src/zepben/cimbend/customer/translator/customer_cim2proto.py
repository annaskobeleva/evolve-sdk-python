#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61968.common.Agreement_pb2 import Agreement as PBAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement as PBCustomerAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerKind_pb2 import CustomerKind as PBCustomerKind
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure as PBPricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff as PBTariff

from zepben.cimbend.common.translator.util import mrid_or_empty
from zepben.cimbend.cim.iec61968.customers.customer import Customer
from zepben.cimbend.common.translator.base_cim2proto import document_to_pb, organisation_to_pb
from zepben.cimbend.cim.iec61968.common.document import Agreement
from zepben.cimbend.cim.iec61968.customers import CustomerAgreement, PricingStructure, Tariff

__all__ = ["agreement_to_pb", "customer_to_pb", "customeragreement_to_pb", "pricingstructure_to_pb", "tariff_to_pb"]


def agreement_to_pb(cim: Agreement) -> PBAgreement:
    return PBAgreement(doc=document_to_pb(cim))


def customer_to_pb(cim: Customer) -> PBCustomer:
    cust = PBCustomer(kind=PBCustomerKind.Value(cim.kind.short_name), agreementMRIDs=[str(io.mrid) for io in cim.agreements])
    setattr(cust, 'or', organisation_to_pb(cim))
    return cust


def customeragreement_to_pb(cim: CustomerAgreement) -> PBCustomerAgreement:
    return PBCustomerAgreement(agr=agreement_to_pb(cim),
                               customerMRID=mrid_or_empty(cim.customer),
                               pricingStructureMRIDs=[str(io.mrid) for io in cim.pricing_structures])


def pricingstructure_to_pb(cim: PricingStructure) -> PBPricingStructure:
    return PBPricingStructure(doc=document_to_pb(cim), tariffMRIDs=[str(io.mrid) for io in cim.tariffs])


def tariff_to_pb(cim: Tariff) -> PBTariff:
    return PBTariff(doc=document_to_pb(cim))


Agreement.to_pb = agreement_to_pb
Customer.to_pb = customer_to_pb
CustomerAgreement.to_pb = customeragreement_to_pb
PricingStructure.to_pb = pricingstructure_to_pb
Tariff.to_pb = tariff_to_pb

