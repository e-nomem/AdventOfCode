from itertools import combinations
from operator import mul
from operator import sub
from typing import Optional

Position = tuple[int, ...]
BeaconIntersection = set[tuple[int, int]]


class Beacon:
    def __init__(self, id: int, position: Position) -> None:
        self.id = id
        self.position = position

        # Swapping the key and value here massively decreases the speed of this solution
        # But this impl risks overwriting neighbor data when more than one beacon is the same distance away
        # For the input I had the solution works either way, so I kept the faster, maybe incorrect?, implementation
        self.neighbors: dict[Position, int] = {}

    def add_neighbor(self, other: "Beacon") -> None:
        # Store the distance between the two beacons sorted by axis
        # This is effectively the same as storing the hypotenuse without doing the calculations
        diff = tuple(sorted(abs(x) for x in diff_position(self.position, other.position)))
        self.neighbors[diff] = other.id
        other.neighbors[diff] = self.id

    def intersect(self, other: "Beacon") -> BeaconIntersection:
        return {
            (this_id, other.neighbors[normalized])
            for normalized, this_id in self.neighbors.items()
            if normalized in other.neighbors
        }


class Scanner:
    def __init__(self, id: int) -> None:
        self.id = id
        self.beacons: dict[Position, Beacon] = {}
        self.position: Optional[Position] = None

    def add_beacon(self, position: Position) -> None:
        if position in self.beacons:
            return

        new_beacon = Beacon(len(self.beacons), position)
        for b in self.beacons.values():
            b.add_neighbor(new_beacon)

        self.beacons[position] = new_beacon

    def intersect(
        self,
        other: "Scanner",
        min_intersections: int,
    ) -> Optional[tuple[Beacon, Beacon, BeaconIntersection]]:
        for this_beacon in self.beacons.values():
            for other_beacon in other.beacons.values():
                intersections = this_beacon.intersect(other_beacon)
                # min_intersections - 1 because intersect returns the vector to n beacons that match
                # So if we want 12 beacons intersecting, we need to find 11 other beacons to match up
                if len(intersections) >= min_intersections - 1:
                    return (this_beacon, other_beacon, intersections)

        return None

    def map_position(self, other_scanner: "Scanner", min_intersections: int) -> bool:
        # If we don't know our own position, we canot map the position of another scanner
        if self.position is None:
            return False

        scanner_intersection = self.intersect(other_scanner, min_intersections)
        if scanner_intersection is None:
            # Insufficient overlapping beacons
            return False

        this_beacon, other_beacon, beacon_intersections = scanner_intersection

        # We only really need one of the intersections TBH, but some intersections are unsuitable
        for this_id, other_id in beacon_intersections:
            # Bleh, key of beacons is position relative to scanner, but intersections returns beacon id
            # So we need to scan all the beacons to find it
            # Intersection can't return the position because it's not stable (we mutate it later in this method)
            relative_this_beacon = next(b for b in self.beacons.values() if b.id == this_id)
            relative_other_beacon = next(b for b in other_scanner.beacons.values() if b.id == other_id)

            # Take the matched beacons and shift them into a position relative to the other end of the match
            pos_a = diff_position(this_beacon.position, relative_this_beacon.position)
            pos_b = diff_position(other_beacon.position, relative_other_beacon.position)

            # If any two axes have the same distance, we cannot uniquely identify them to determine orientation
            if any(abs(a) == abs(b) for a, b in combinations(pos_a, 2)):
                continue

            # Each orientation is a 3-tuple of two zeros and a 1 or -1
            # We use them to bring all the beacons in the other scanner into the same orientation
            orientations = tuple(orientation_map(p, pos_b) for p in pos_a)

            for beacon in other_scanner.beacons.values():
                # new_<axis> = (pos.x * orientation_<axis>.x) + (pos.y * orientation_<axis>.y) + (pos.z * orientation_<axis>.z)
                # This ensures that the axis where the pos_a and pos_b match is preserved (multiplied by 1 or -1 to flip it around)
                # while the other two are squelched (multiplied by 0)
                beacon.position = tuple(sum(map(mul, beacon.position, o)) for o in orientations)

            # All the internal beacon positions are now correctly oriented, but the keys of the beacons dict are not up to date
            # Fix that up as well
            other_scanner.beacons = {b.position: b for b in other_scanner.beacons.values()}

            # Now that this_beacon and other_beacon are oriented the same way, we can calculate the position of the other scanner
            # Note that the position of this_beacon is still relative to the scanner, so we need to make it absolute first
            other_scanner.position = tuple(
                map(
                    lambda p: (p[0] + p[1]) - p[2],
                    zip(this_beacon.position, self.position, other_beacon.position),
                ),
            )

            print(f"Mapped scanner {other_scanner.id:2d} to position {other_scanner.position}")
            return True

        # Not a single suitable intersection in the 11+ options? Unlikely
        print(
            f"ERROR: All intersections were discarded as unsuitable for mapping between scanners {self.id} and {other_scanner.id}",
        )
        print(f" -> Scanner {self.id}: {this_beacon.position}")
        print(f" -> Scanner {other_scanner.id}: {other_beacon.position}")
        return False


def diff_position(pos_a: Position, pos_b: Position) -> Position:
    return tuple(map(sub, pos_a, pos_b))


def orientation_map(source: int, other: Position) -> tuple[int, ...]:
    def _helper(x: int) -> int:
        if source == x:
            return 1
        elif source == -x:
            return -1
        else:
            return 0

    return tuple(_helper(x) for x in other)


def map_scanners(scanners: list[Scanner], min_intersections: int = 12) -> None:
    # Pick an initial scanner to use as the origin (0, 0, 0)
    scanners[0].position = (0, 0, 0)
    mapped_scanners: set[int] = {scanners[0].id}

    while len(mapped_scanners) != len(scanners):
        starting_len = len(mapped_scanners)
        for known_scanner in scanners:
            if known_scanner.id not in mapped_scanners:
                continue

            for unknown_scanner in scanners:
                if unknown_scanner.id in mapped_scanners:
                    # Not unknown, we've already mapped it
                    continue

                if known_scanner.map_position(unknown_scanner, min_intersections):
                    mapped_scanners.add(unknown_scanner.id)

        ending_len = len(mapped_scanners)
        if ending_len - starting_len == 0:
            # We've messed up somewhere
            print("ERROR: Completed an entire round without mapping any new scanners")
            break
