# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.

from typing import Any, TypedDict

HEADER = TypedDict("Header", {
    "Description": str,
    "Opportunities supported": list[str],
    "Priority levels supported": list[str],
    "Experiments included": list[str],
    "dreq content version": str,
    "dreq content file": str,
    "dreq content sha256 hash": str,
    "dreq api version": str,
}, total=True)

DATA_REQUEST_INFO = TypedDict("DataRequestInfo", {
    "Branded variable name": str,
    "CF standard name": str,
    "CMIP6 Differences": str,
    "Cell measures": str,
    "Cell methods": str,
    "Comment": str,
    "Dimensions": str,
    "Frequency": str,
    "Long name": str,
    "Modeling realm": str,
    "Positive": str,
    "Processing notes": str,
    "Region": str,
    "Units": str,
    "Variable status": str
}, total=True)

MAPPING_INFO = TypedDict("MappingInfo", {
    "Expression HadGEM3-GC3.1": str,
    "Expression HadGEM3-GC5": str,
    "Expression UKESM1": str,
    "Expression UKESM1-3": str
}, total=True)

STASH_ENTRY = TypedDict("StashEntry", {
    "STASH": str,
    "domain_profile": str,
    "model": str,
    "stash_number": str,
    "time_profile": str,
    "usage_profile": str
}, total=True)

VARIABLE_MAPPING = TypedDict("VariableMapping", {
    "Data Request information": DATA_REQUEST_INFO,
    "Mapping information": MAPPING_INFO,
    "STASH entries": list[STASH_ENTRY],
    "XIOS entries": dict[str, Any],
    "issue_number": int,
    "labels": list[str],
    "title": str
}, total=False)


class VARIABLE_DATA(TypedDict, total=True):
    header: HEADER
    experiment: dict[str, dict[str, list[str]]]


class VALIDATION_DATA(TypedDict, total=False):
    file: str
    failures: bool
    missing_sections: list[str]
    unexpected_sections: list[str]
    missing_keys: list[str]
    unexpected_keys: list[str]
    missing_values: list[str]
    unexpected_values: list[str]
    invalid_values: list[str]
