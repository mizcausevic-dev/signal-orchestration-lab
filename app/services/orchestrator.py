from __future__ import annotations

from collections import defaultdict, deque

import pandas as pd

from app.models import (
    DashboardSummary,
    GraphEdge,
    GraphResponse,
    OrchestrationInput,
    OrchestrationResponse,
    RoutedAction,
)


SEVERITY_WEIGHT = {
    "watch": 0.25,
    "moderate": 0.5,
    "high": 0.8,
    "critical": 1.0,
}


def _frame(payload: OrchestrationInput) -> pd.DataFrame:
    frame = pd.DataFrame([node.model_dump() for node in payload.nodes])
    frame["gap"] = frame["target_value"] - frame["current_value"]
    frame["severity_weight"] = frame["severity"].map(SEVERITY_WEIGHT)
    frame["dependency_count"] = frame["dependencies"].apply(len)
    frame["pressure"] = (
        frame["severity_weight"] * 45
        + frame["dependency_count"] * 8
        + (1 - frame["confidence"]) * 25
        + (14 - frame["due_in_days"]).clip(lower=0) * 1.7
    )
    return frame


def _status(score: int) -> str:
    if score <= 45:
        return "escalated"
    if score <= 72:
        return "coordinated"
    return "stable"


def _topological_order(payload: OrchestrationInput) -> list[str]:
    adjacency: dict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = {node.signal_id: 0 for node in payload.nodes}

    for node in payload.nodes:
        for dependency in node.dependencies:
            adjacency[dependency].append(node.signal_id)
            indegree[node.signal_id] += 1

    queue = deque(sorted([node_id for node_id, degree in indegree.items() if degree == 0]))
    order: list[str] = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in adjacency[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(payload.nodes):
        # Cycles should still resolve into a deterministic order for a portfolio demo.
        remaining = [node.signal_id for node in payload.nodes if node.signal_id not in order]
        order.extend(sorted(remaining))

    return order


def build_orchestration(payload: OrchestrationInput) -> OrchestrationResponse:
    frame = _frame(payload)
    score = max(0, min(100, int(round(100 - frame["pressure"].sum() / len(frame)))))
    status = _status(score)
    order = _topological_order(payload)

    ranked = frame.set_index("signal_id").loc[order].sort_values(
        by=["severity_weight", "dependency_count", "pressure"], ascending=[False, False, False]
    )

    actions = [
        RoutedAction(
            title=f"Coordinate around {row.title.lower()}",
            owner=row.owner,
            lane=row.lane,
            severity=row.severity,
            sequence_rank=index + 1,
            due_in_days=int(row.due_in_days),
            rationale=(
                f"{row.title} carries {row.dependency_count} downstream dependencies "
                f"and pressure score {row.pressure:.1f}."
            ),
        )
        for index, row in enumerate(ranked.itertuples())
    ]

    highest = ranked.iloc[0]
    clusters = [
        f"{lane.title()} pressure: {count} linked signals"
        for lane, count in frame.groupby("lane").size().sort_values(ascending=False).items()
    ]

    return OrchestrationResponse(
        status=status,
        score=score,
        orchestration_headline=(
            f"{payload.scenario_name} should anchor on {highest.title.lower()} "
            "before downstream pressure compounds."
        ),
        pressure_clusters=clusters,
        routed_actions=actions,
    )


def build_graph(payload: OrchestrationInput) -> GraphResponse:
    edges: list[GraphEdge] = []
    for node in payload.nodes:
        for dependency in node.dependencies:
            edges.append(
                GraphEdge(
                    source=dependency,
                    target=node.signal_id,
                    relationship="unblocks",
                )
            )
    return GraphResponse(nodes=payload.nodes, edges=edges)


def build_dashboard_summary(orchestrations: list[OrchestrationInput]) -> DashboardSummary:
    all_nodes = [node.model_dump() for orchestration in orchestrations for node in orchestration.nodes]
    frame = pd.DataFrame(all_nodes)
    analyses = [build_orchestration(item) for item in orchestrations]
    return DashboardSummary(
        orchestrations=len(orchestrations),
        nodes=len(all_nodes),
        escalated_paths=sum(1 for item in analyses if item.status == "escalated"),
        average_confidence=round(float(frame["confidence"].mean()), 2),
    )

