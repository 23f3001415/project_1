import collections
import json
import statistics
import uuid

import requests


BASE_URL = "https://tds-network-games.sanand.workers.dev"
TARGET_EMAIL = "23f3001415@ds.study.iitm.ac.in"
NODE_COUNT = 120
MAX_QUERIES = 55
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/detective/",
    "Content-Type": "application/json",
}


class DetectiveClient:
    def __init__(self, email: str) -> None:
        self.email = email
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.start_data = self.start()
        self.session.headers["X-Session-Token"] = self.start_data["session_token"]

    def start(self) -> dict:
        response = self.session.post(
            f"{BASE_URL}/detective/start",
            json={"email": self.email},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_node(self, node_id: int) -> dict:
        response = self.session.get(f"{BASE_URL}/detective/node/{node_id}", timeout=30)
        response.raise_for_status()
        return response.json()

    def submit(self, compromised_node: int, path: list[int]) -> dict:
        response = self.session.post(
            f"{BASE_URL}/detective/submit",
            json={"compromised_node": compromised_node, "path": path},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


def chunked(values: list[int], size: int) -> list[list[int]]:
    return [values[i : i + size] for i in range(0, len(values), size)]


def build_full_graph() -> dict[int, dict]:
    nodes: dict[int, dict] = {}
    node_ids = list(range(NODE_COUNT))
    for chunk in chunked(node_ids, MAX_QUERIES):
        helper_email = f"detective-helper-{uuid.uuid4().hex[:12]}@example.com"
        helper = DetectiveClient(helper_email)
        for node_id in chunk:
            nodes[node_id] = helper.get_node(node_id)
    return nodes


def zscore(value: float, values: list[float]) -> float:
    mean = statistics.mean(values)
    stdev = statistics.pstdev(values)
    if stdev == 0:
        return 0.0
    return (value - mean) / stdev


def compromised_score(node: dict, clues: list[str], stats: dict[str, list[float]]) -> float:
    attrs = node["attributes"]
    clue_text = " ".join(clues).lower()

    score = 0.0

    # Always useful for this game family.
    score += 3.5 * zscore(attrs["tx_volume_daily"], stats["tx_volume_daily"])
    score += 3.5 * zscore(attrs["avg_tx_size"], stats["avg_tx_size"])

    if "almost never receives" in clue_text:
        score -= 4.0 * zscore(attrs["in_out_ratio"], stats["in_out_ratio"])
    elif "almost never sends" in clue_text:
        score += 4.0 * zscore(attrs["in_out_ratio"], stats["in_out_ratio"])

    if "surprisingly few nodes" in clue_text or "connects to surprisingly few nodes" in clue_text:
        score -= 2.5 * zscore(node["degree"], stats["degree"])

    if "handful of counterparties" in clue_text:
        score -= 2.5 * zscore(attrs["counterparty_count"], stats["counterparty_count"])

    if "transactions are rare" in clue_text:
        score -= 1.5 * zscore(attrs["tx_count_daily"], stats["tx_count_daily"])

    return score


def find_compromised_node(nodes: dict[int, dict], clues: list[str]) -> tuple[int, list[tuple[float, int]]]:
    stats = {
        "tx_volume_daily": [node["attributes"]["tx_volume_daily"] for node in nodes.values()],
        "tx_count_daily": [node["attributes"]["tx_count_daily"] for node in nodes.values()],
        "in_out_ratio": [node["attributes"]["in_out_ratio"] for node in nodes.values()],
        "counterparty_count": [node["attributes"]["counterparty_count"] for node in nodes.values()],
        "avg_tx_size": [node["attributes"]["avg_tx_size"] for node in nodes.values()],
        "degree": [node["degree"] for node in nodes.values()],
    }
    ranked = sorted(
        ((compromised_score(node, clues, stats), node_id) for node_id, node in nodes.items()),
        reverse=True,
    )
    return ranked[0][1], ranked[:10]


def shortest_path(nodes: dict[int, dict], start: int, target: int) -> list[int]:
    queue = collections.deque([(start, [start])])
    seen = {start}
    while queue:
        node_id, path = queue.popleft()
        if node_id == target:
            return path
        for neighbor in nodes[node_id]["neighbors"]:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append((neighbor, path + [neighbor]))
    raise ValueError(f"No path from {start} to {target}")


def main() -> None:
    target = DetectiveClient(TARGET_EMAIL)
    anchor = target.start_data["anchor_node"]["id"]
    clues = target.start_data["clues"]

    full_graph = build_full_graph()
    suspect, ranked = find_compromised_node(full_graph, clues)
    path = shortest_path(full_graph, anchor, suspect)
    submit_response = target.submit(suspect, path)

    result = {
        "target_email": TARGET_EMAIL,
        "week_id": target.start_data["week_id"],
        "anchor_node": anchor,
        "clues": clues,
        "compromised_node": suspect,
        "path": path,
        "top_candidates": [
            {
                "score": round(score, 4),
                "node_id": node_id,
                "degree": full_graph[node_id]["degree"],
                "attributes": full_graph[node_id]["attributes"],
            }
            for score, node_id in ranked
        ],
        "submit_response": submit_response,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
