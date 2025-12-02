# (C) British Crown Copyright 2025, Met Office.
# Please see LICENSE.md for license details.

from typing import Any, TypedDict
from dataclasses import dataclass

@dataclass
class Header():
    description: str
    opportunities_supported: list[str]
    priority_levels_supported: list[str]
    experiments_included: list[str]
    dreq_content_version: str
    dreq_content_file: str
    dreq_content_sha256_hash: str
    dreq_api_version: str

@dataclass
class VariablePriorities():
    core: list[str]
    high: list[str]
    medium: list[str]
    low: list[str]

@dataclass 
class Experiment():
    name: dict[str, VariablePriorities]

@dataclass
class DRExperimentMetadata():
    header: dict[Header]
    experiment: dict[Experiment]













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


