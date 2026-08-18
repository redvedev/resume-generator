from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RequirementImportance(str, Enum):
    REQUIRED = "required"
    PREFERRED = "preferred"
    OPTIONAL = "optional"


class RequirementMatchType(str, Enum):
    EXACT = "EXACT"
    RELATED = "RELATED"
    CONCEPTUAL = "CONCEPTUAL"
    NONE = "NONE"


class EvidenceStrength(str, Enum):
    EXPLICIT = "EXPLICIT"
    STRONG = "STRONG"
    WEAK = "WEAK"
    NONE = "NONE"


class RequirementCategory(str, Enum):
    TECHNOLOGY = "technology"
    PROGRAMMING_LANGUAGE = "programming_language"
    DATABASE = "database"
    CLOUD = "cloud"
    FRAMEWORK = "framework"
    TOOL = "tool"
    METHODOLOGY = "methodology"
    DOMAIN = "domain"
    EDUCATION = "education"
    CERTIFICATION = "certification"
    RESPONSIBILITY = "responsibility"
    SOFT_SKILLS = "soft_skills"
    SENIORITY = "seniority"
    OTHER = "other"


class JobRequirement(BaseModel):
    requirement: str = Field(description="Normalized requirement phrase from the job description")
    category: str = Field(default="other", description="Requirement category")
    importance: RequirementImportance = Field(default=RequirementImportance.OPTIONAL)
    exact_keywords: list[str] = Field(default_factory=list)


class RequirementMatch(BaseModel):
    requirement: str
    importance: RequirementImportance = RequirementImportance.OPTIONAL
    match_type: RequirementMatchType = RequirementMatchType.NONE
    evidence_strength: EvidenceStrength = EvidenceStrength.NONE
    candidate_evidence: list[str] = Field(default_factory=list)
    candidate_technologies: list[str] = Field(default_factory=list)
    transferable: bool = False


class RequirementAnalysis(BaseModel):
    matches: list[RequirementMatch] = Field(default_factory=list)


class ResumeValidation(BaseModel):
    valid: bool = True
    issues: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    invented_technologies: list[str] = Field(default_factory=list)
    invented_responsibilities: list[str] = Field(default_factory=list)
    invented_metrics: list[str] = Field(default_factory=list)
    invented_team_sizes: list[str] = Field(default_factory=list)
    invented_project_names: list[str] = Field(default_factory=list)
