import json
import math
import os
from collections import deque
from pathlib import Path

import requests


BASE_URL = "https://tds-network-games.sanand.workers.dev"
EMAIL = "23f3001415@ds.study.iitm.ac.in"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": f"{BASE_URL}",
    "Referer": f"{BASE_URL}/labyrinth/",
    "Content-Type": "application/json",
}
STATE_PATH = Path(__file__).with_name("labyrinth_state.json")
DIR_OFFSETS = {
    "north": -11,
    "south": 11,
    "west": -1,
    "east": 1,
}
OPPOSITE = {
    "north": "south",
    "south": "north",
    "west": "east",
    "east": "west",
}
EXIT_ROOM = 120


class LabyrinthClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.state = self._load_state()
        token = self.state.get("session_token")
        if token:
            self.session.headers["X-Session-Token"] = token

    def _load_state(self) -> dict:
        if STATE_PATH.exists():
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return {
            "session_token": "",
            "week_id": "",
            "question": None,
            "current_room": None,
            "rooms": {},
            "collected_rooms": [],
            "inventory": [],
        }

    def save_state(self) -> None:
        STATE_PATH.write_text(json.dumps(self.state, indent=2), encoding="utf-8")

    def api(self, method: str, path: str, body: dict | None = None) -> dict:
        response = self.session.request(method, f"{BASE_URL}{path}", json=body, timeout=60)
        response.raise_for_status()
        return response.json()

    def start_or_restore(self) -> None:
        if self.state.get("session_token"):
            try:
                room = self.look()
                self.state["current_room"] = room["room_id"]
                self.state["inventory"] = self.inventory()["fragments"]
                self.save_state()
                return
            except requests.HTTPError:
                self.state["session_token"] = ""
                self.session.headers.pop("X-Session-Token", None)

        data = self.api("POST", "/labyrinth/start", {"email": EMAIL})
        self.state["session_token"] = data["session_token"]
        self.state["week_id"] = data["week_id"]
        self.state["question"] = data["question"]
        self.state["current_room"] = data["current_room"]
        self.session.headers["X-Session-Token"] = data["session_token"]
        self.look()
        self.state["inventory"] = self.inventory()["fragments"]
        self.save_state()

    def look(self) -> dict:
        data = self.api("GET", "/labyrinth/look")
        room_id = data["room_id"]
        self.state["current_room"] = room_id
        self.state["rooms"][str(room_id)] = data
        self.save_state()
        return data

    def inventory(self) -> dict:
        data = self.api("GET", "/labyrinth/inventory")
        self.state["question"] = data["question"]
        self.state["inventory"] = data["fragments"]
        self.save_state()
        return data

    def move(self, direction: str) -> dict:
        data = self.api("POST", "/labyrinth/move", {"direction": direction})
        self.state["current_room"] = data["room_id"]
        self.state["rooms"][str(data["room_id"])] = data
        self.save_state()
        return data

    def collect(self) -> dict:
        data = self.api("POST", "/labyrinth/collect", {})
        room_id = self.state["current_room"]
        collected_rooms = set(self.state.get("collected_rooms", []))
        collected_rooms.add(room_id)
        self.state["collected_rooms"] = sorted(collected_rooms)
        self.state["inventory"] = self.inventory()["fragments"]
        self.look()
        self.save_state()
        return data

    def submit(self, answer: str) -> dict:
        data = self.api("POST", "/labyrinth/submit", {"answer": answer})
        self.save_state()
        return data


def room_neighbor(room_id: int, direction: str) -> int:
    return room_id + DIR_OFFSETS[direction]


def shortest_path(rooms: dict[str, dict], start: int, target: int) -> list[str]:
    queue = deque([(start, [])])
    seen = {start}
    while queue:
        room_id, path = queue.popleft()
        if room_id == target:
            return path
        room = rooms[str(room_id)]
        for direction in room["exits"]:
            nxt = room_neighbor(room_id, direction)
            if nxt in seen or str(nxt) not in rooms:
                continue
            seen.add(nxt)
            queue.append((nxt, path + [direction]))
    raise ValueError(f"No path from {start} to {target}")


def navigate(client: LabyrinthClient, target: int) -> None:
    current = client.state["current_room"]
    if current == target:
        return
    for direction in shortest_path(client.state["rooms"], current, target):
        client.move(direction)
        client.look()


def is_useful_fragment(fragment: dict) -> bool:
    return fragment.get("type") != "distractor"


def is_complete_record(fragment: dict) -> bool:
    if not is_useful_fragment(fragment):
        return False
    if fragment.get("quality") not in {"ok", "complete"}:
        return False
    data = fragment.get("data", {})
    queue_depth = data.get("queue_depth")
    response_ms = data.get("response_ms")
    if queue_depth in (None, "", "CORRUPT") or response_ms in (None, "", "CORRUPT"):
        return False
    return True


def weighted_mean_queue_depth(fragments: list[dict]) -> float:
    numerator = 0.0
    denominator = 0.0
    for fragment in fragments:
        if not is_complete_record(fragment):
            continue
        data = fragment["data"]
        weight = float(data["response_ms"])
        value = float(data["queue_depth"])
        numerator += value * weight
        denominator += weight
    if denominator == 0:
        raise ValueError("No complete records available for weighted mean.")
    return numerator / denominator


def normalize_answer(value: float) -> str:
    # Keep enough precision for grading while avoiding scientific notation.
    text = f"{value:.10f}"
    return text.rstrip("0").rstrip(".")


def explore_all(client: LabyrinthClient) -> None:
    visited = set()

    def dfs(room_id: int) -> None:
        room = client.look()
        assert room["room_id"] == room_id
        visited.add(room_id)

        if room.get("has_item") and not room.get("item_collected"):
            client.collect()
            room = client.look()

        for direction in room["exits"]:
            nxt = room_neighbor(room_id, direction)
            if nxt in visited:
                continue
            client.move(direction)
            dfs(nxt)
            client.move(OPPOSITE[direction])
            client.look()

    dfs(client.state["current_room"])


def summarize_inventory(fragments: list[dict]) -> dict:
    useful = [f for f in fragments if is_useful_fragment(f)]
    complete = [f for f in useful if is_complete_record(f)]
    return {
        "total_collected": len(fragments),
        "useful_collected": len(useful),
        "complete_useful": len(complete),
        "types": sorted({f.get("type", "") for f in fragments}),
        "qualities": sorted({f.get("quality", "") for f in fragments}),
    }


def main() -> None:
    client = LabyrinthClient()
    client.start_or_restore()
    explore_all(client)

    inventory = client.inventory()["fragments"]
    summary = summarize_inventory(inventory)
    answer = normalize_answer(weighted_mean_queue_depth(inventory))

    navigate(client, EXIT_ROOM)
    client.look()
    submit_data = client.submit(answer)

    output = {
        "week_id": client.state["week_id"],
        "question": client.state["question"],
        "inventory_summary": summary,
        "answer": answer,
        "submit_response": submit_data,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
