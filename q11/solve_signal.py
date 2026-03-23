import re
from collections import deque

import requests

BASE_URL = "https://tds-network-games.sanand.workers.dev/signal"
EMAIL = "23f3001415@ds.study.iitm.ac.in"

GRAPH = {
    "ENTRANCE_HALL": {
        "north": ("SERVER_ROOM_A", None),
        "east": ("STORAGE_ROOM", None),
    },
    "SERVER_ROOM_A": {
        "south": ("ENTRANCE_HALL", None),
        "east": ("SERVER_ROOM_B", None),
        "north": ("MAINTENANCE_BAY", None),
    },
    "SERVER_ROOM_B": {
        "west": ("SERVER_ROOM_A", None),
    },
    "STORAGE_ROOM": {
        "west": ("ENTRANCE_HALL", None),
        "south": ("LABORATORY", "SPECIMEN_KEY"),
    },
    "LABORATORY": {
        "north": ("STORAGE_ROOM", "SPECIMEN_KEY"),
        "east": ("CONTROL_ROOM", None),
    },
    "MAINTENANCE_BAY": {
        "south": ("SERVER_ROOM_A", None),
        "east": ("POWER_ROOM", None),
        "west": ("CONTROL_ROOM", None),
    },
    "POWER_ROOM": {
        "west": ("MAINTENANCE_BAY", None),
    },
    "CONTROL_ROOM": {
        "east": ("ARCHIVE_ROOM", None),
        "north": ("MAINTENANCE_BAY", None),
        "south": ("CORE_CHAMBER", "REPAIRED_ACCESS_CARD"),
        "west": ("LABORATORY", None),
    },
    "ARCHIVE_ROOM": {
        "west": ("CONTROL_ROOM", None),
    },
    "CORE_CHAMBER": {
        "north": ("CONTROL_ROOM", None),
    },
}


class SignalClient:
    def __init__(self, email):
        self.email = email
        self.session = requests.Session()
        self.session_token = ""

    def start(self):
        data = self.api("POST", "/start", {"email": self.email}, needs_auth=False)
        self.session_token = data["session_token"]
        self.session.headers["X-Session-Token"] = self.session_token
        return data

    def clear(self, week_id):
        return self.api(
            "POST",
            "/clear",
            {"email": self.email, "week": week_id},
        )

    def api(self, method, path, body=None, needs_auth=True, params=None):
        headers = {"Content-Type": "application/json"}
        if needs_auth and self.session_token:
            headers["X-Session-Token"] = self.session_token
        response = self.session.request(
            method,
            BASE_URL + path,
            headers=headers,
            json=body,
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def look(self):
        return self.api("GET", "/look")

    def inventory(self):
        return self.api("GET", "/inventory")

    def examine(self, target):
        return self.api("GET", "/examine", params={"target": target})

    def move(self, direction):
        return self.api("POST", "/move", {"direction": direction})

    def take(self, item):
        return self.api("POST", "/take", {"item": item})

    def combine(self, item_a, item_b):
        return self.api("POST", "/combine", {"item_a": item_a, "item_b": item_b})

    def use(self, target, value=None, inputs=None):
        body = {"target": target}
        if value is not None:
            body["value"] = value
        if inputs is not None:
            body["inputs"] = inputs
        return self.api("POST", "/use", body)


def inventory_names(inventory_data):
    return {entry["item"] for entry in inventory_data["inventory"]}


def bfs_path(start_room, target_room, items):
    queue = deque([(start_room, [])])
    seen = {start_room}
    while queue:
        room, path = queue.popleft()
        if room == target_room:
            return path
        for direction, (next_room, required_item) in GRAPH[room].items():
            if required_item and required_item not in items:
                continue
            if next_room in seen:
                continue
            seen.add(next_room)
            queue.append((next_room, path + [direction]))
    raise RuntimeError(f"No path from {start_room} to {target_room}")


def navigate(client, target_room):
    while True:
        state = client.look()
        if state["room"] == target_room:
            return state
        items = inventory_names(client.inventory())
        path = bfs_path(state["room"], target_room, items)
        client.move(path[0])


def take_if_present(client, room, wanted_items):
    state = navigate(client, room)
    items_here = set(state.get("items_here", []))
    for item in wanted_items:
        if item in items_here:
            client.take(item)


def solve_pin(client, puzzles):
    if puzzles["PUZZLE_1_PIN"]["solved"]:
        return puzzles["PUZZLE_1_PIN"]["fragment"]
    navigate(client, "SERVER_ROOM_A")
    cert = client.examine("INSPECTION_CERTIFICATE")["description"]
    note = client.examine("NOTEBOOK")["description"]
    year = int(re.search(r"Inspection date: (\d{4})", cert).group(1))
    sublevel = int(re.search(r"Level (\d+) sublevel", note).group(1))
    result = client.use("PIN_TERMINAL", value=year + sublevel)
    return result["fragment_revealed"]


def craft_if_needed(client):
    items = inventory_names(client.inventory())
    if "DEMAGNETISER" not in items and {"CLEANING_CLOTH", "SOLVENT_BOTTLE"} <= items:
        client.combine("CLEANING_CLOTH", "SOLVENT_BOTTLE")
        items = inventory_names(client.inventory())
    if "REPAIRED_ACCESS_CARD" not in items and {"ACCESS_CARD", "DEMAGNETISER"} <= items:
        client.combine("ACCESS_CARD", "DEMAGNETISER")
        items = inventory_names(client.inventory())
    if "POWERED_TUNER" not in items and {"FREQUENCY_TUNER", "POWER_CELL"} <= items:
        client.combine("FREQUENCY_TUNER", "POWER_CELL")


def solve_frequency(client, puzzles):
    if puzzles["PUZZLE_2_FREQUENCY"]["solved"]:
        return puzzles["PUZZLE_2_FREQUENCY"]["fragment"]
    backup = client.examine("BACKUP_LOG")["description"]
    signal = client.examine("SIGNAL_LOG")["description"]
    backup_freqs = set(re.findall(r"\d+\.\d+", backup))
    signal_freqs = set(re.findall(r"\d+\.\d+", signal))
    common = sorted(backup_freqs & signal_freqs)
    if len(common) != 1:
        raise RuntimeError(f"Expected one shared frequency, found {common}")
    navigate(client, "MAINTENANCE_BAY")
    result = client.use("RADIO_TRANSMITTER", value=float(common[0]))
    return result["fragment_revealed"]


def solve_verify(client, puzzles, frag1, frag2):
    if puzzles["PUZZLE_3_VERIFY"]["solved"]:
        return puzzles["PUZZLE_3_VERIFY"]["fragment"]
    navigate(client, "CONTROL_ROOM")
    result = client.use("TERMINAL_3", inputs=[frag1, frag2])
    return result["fragment_revealed"]


def solve_exit(client, puzzles, frag1, frag2, frag3):
    if puzzles["PUZZLE_4_PASSCODE"]["solved"]:
        raise RuntimeError("Session is already completed. Start a fresh session if you want a new token.")
    passcode = frag1 + frag2 + frag3
    navigate(client, "CORE_CHAMBER")
    result = client.use("EXIT_KEYPAD", value=passcode)
    return passcode, result["completion_token"]


def main():
    client = SignalClient(EMAIL)
    start_data = client.start()
    if start_data.get("status") == "completed":
        client.clear(start_data["week_id"])
        start_data = client.start()
    print(f"Week: {start_data['week_id']}")
    print(f"Start room: {start_data['current_room']}")

    take_if_present(client, "ENTRANCE_HALL", ["MAINTENANCE_KEY", "FACILITY_MAP"])
    take_if_present(client, "SERVER_ROOM_A", ["INSPECTION_CERTIFICATE", "NOTEBOOK"])
    take_if_present(client, "SERVER_ROOM_B", ["SYSTEM_BADGE", "TORN_MANUAL", "UV_TORCH", "ACCESS_CARD"])
    take_if_present(client, "MAINTENANCE_BAY", ["SPECIMEN_KEY", "FREQUENCY_TUNER"])
    take_if_present(client, "POWER_ROOM", ["CLEANING_CLOTH", "BROKEN_RADIO", "SOLVENT_BOTTLE", "POWER_CELL"])
    craft_if_needed(client)
    take_if_present(client, "ARCHIVE_ROOM", ["BACKUP_LOG", "SIGNAL_LOG"])

    inventory_data = client.inventory()
    puzzles = inventory_data["puzzles"]
    frag1 = solve_pin(client, puzzles)

    inventory_data = client.inventory()
    puzzles = inventory_data["puzzles"]
    craft_if_needed(client)
    frag2 = solve_frequency(client, puzzles)

    inventory_data = client.inventory()
    puzzles = inventory_data["puzzles"]
    frag3 = solve_verify(client, puzzles, frag1, frag2)

    inventory_data = client.inventory()
    puzzles = inventory_data["puzzles"]
    passcode, token = solve_exit(client, puzzles, frag1, frag2, frag3)

    print(f"Fragment 1: {frag1}")
    print(f"Fragment 2: {frag2}")
    print(f"Fragment 3: {frag3}")
    print(f"Passcode: {passcode}")
    print("\nCompletion JWT:\n")
    print(token)


if __name__ == "__main__":
    main()
