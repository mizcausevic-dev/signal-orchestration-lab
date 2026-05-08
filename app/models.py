from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal["watch", "moderate", "high", "critical"]
Lane = Literal["revenue", "growth", "ops", "security", "ai", "customer"]
PlaybookStatus = Literal["stable", "coordinated", "escalated"]


class SignalNode(BaseModel):
    signal_id: str
    lane: Lane
    title: str
    owner: str
    metric: str
    current_value: float
    target_value: float
    confidence: float = Field(ge=0.0, le=1.0)
    severity: Severity
    due_in_days: int
    dependencies: list[str] = Field(default_factory=list)
    note: str


class OrchestrationInput(BaseModel):
    orchestration_id: str
    scenario_name: str
    environment: Literal["production", "staging", "executive-review"]
    nodes: list[SignalNode]


class RoutedAction(BaseModel):
    title: str
    owner: str
    lane: Lane
    severity: Severity
    sequence_rank: int
    due_in_days: int
    rationale: str


class OrchestrationResponse(BaseModel):
    status: PlaybookStatus
    score: int
    orchestration_headline: str
    pressure_clusters: list[str]
    routed_actions: list[RoutedAction]


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str


class GraphResponse(BaseModel):
    nodes: list[SignalNode]
    edges: list[GraphEdge]


class DashboardSummary(BaseModel):
    orchestrations: int
    nodes: int
    escalated_paths: int
    average_confidence: float

