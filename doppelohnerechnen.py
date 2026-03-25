#########################################################################
# Doppel Ohne Rechnen
#   
#   Dieses Skript berechnet aus einer gegebenen Liste an Spielern 
#   mit ihren Startpositionen alle möglichen Doppelkombinationen 
#   und Aufstellungsreihenfolgen. Dabei werden die Regeln der 
#   Spielsysteme berücksichtigt.
#   Die unterstützten Spielsysteme sind: 
#       6er- und 4er-Paarkreutz (6PK, 4PK).
#   
#   4er-Paarkreutz (4PK):
#    - Das erste Doppel muss die niedrigere Summe an Startpositionen 
#      haben als das zweite Doppel.
#   6er-Paarkreutz (6PK):
#    - Es gibt drei Doppelpaarungen
#    - Das erste Doppel darf frei gewählt werden
#    - Das zweite Doppel muss die niedrigere Summe an Startpositionen
#      haben als das dritte Doppel
#
#   Beispiel: 
#      Input: 
#           --players [("Alice", 1), ("Bob", 2), ("Charlie", 3), 
#                      ("David", 4), ("Eve", 5), ("Frank", 6)]
#           --system 6PK
#      Output für eine mögliche Aufstellung:
#           Alice/Bob (3), Charlie/David (7), Eve/Frank (11)
###########################################################################

import argparse
from itertools import combinations

def pair_to_string(pair):
    return f"{pair[0][0]}/{pair[1][0]} ({pair[0][1] + pair[1][1]})"

def calculate_combinations_4erpk(players):
    valid_combinations = []
    for combo in combinations(players, 4):  # deterministisch, wenn players sortiert ist
        # Genau die 3 eindeutigen Paarungen der 4 Spieler.
        unique_pairings = [
            ((0, 1), (2, 3)),
            ((0, 2), (1, 3)),
            ((0, 3), (1, 2)),
        ]

        for pair1_idx, pair2_idx in unique_pairings:
            pair1 = (combo[pair1_idx[0]], combo[pair1_idx[1]])
            pair2 = (combo[pair2_idx[0]], combo[pair2_idx[1]])

            sum1 = pair1[0][1] + pair1[1][1]
            sum2 = pair2[0][1] + pair2[1][1]

            # Kanonische Reihenfolge: zuerst kleinere Summe; bei Gleichstand per Tie-Break.
            if sum1 > sum2:
                pair1, pair2 = pair2, pair1
            elif sum1 == sum2:
                min_pair1 = min(pair1[0][1], pair1[1][1])
                min_pair2 = min(pair2[0][1], pair2[1][1])
                if min_pair1 > min_pair2:
                    pair1, pair2 = pair2, pair1

            valid_combinations.append((pair1, pair2))

    return valid_combinations

def calculate_combinations_6erpk(players):
    valid_combinations = []
    for combo in combinations(players, 6):  # deterministisch, wenn players sortiert ist
        for i, j in combinations(range(6), 2):
            pair1 = (combo[i], combo[j])
            remaining = [k for k in range(6) if k not in (i, j)]
            a, b, c, d = remaining

            # Genau die 3 eindeutigen Paarungen der 4 Restspieler.
            unique_pairings = [
                ((a, b), (c, d)),
                ((a, c), (b, d)),
                ((a, d), (b, c)),
            ]

            for pair2_idx, pair3_idx in unique_pairings:
                pair2 = (combo[pair2_idx[0]], combo[pair2_idx[1]])
                pair3 = (combo[pair3_idx[0]], combo[pair3_idx[1]])

                sum2 = pair2[0][1] + pair2[1][1]
                sum3 = pair3[0][1] + pair3[1][1]

                # Kanonische Reihenfolge: zuerst kleinere Summe; bei Gleichstand per Tie-Break.
                if sum2 > sum3:
                    pair2, pair3 = pair3, pair2
                elif sum2 == sum3:
                    # Bei gleicher Summe kommt das Paar mit kleinerem Minimum zuerst.
                    min_pair2 = min(pair2[0][1], pair2[1][1])
                    min_pair3 = min(pair3[0][1], pair3[1][1])
                    if min_pair2 > min_pair3:
                        pair2, pair3 = pair3, pair2

                valid_combinations.append((pair1, pair2, pair3))
    return valid_combinations

def exclude_doubles(combinations, exclude_pairs):
    filtered_combinations = []
    for combo in combinations:
        if not any(pair in combo for pair in exclude_pairs):
            filtered_combinations.append(combo)
    return filtered_combinations

def print_combinations(combinations):
    counter = 1
    for combo in combinations:
        print(f"Option {counter}: " + ", ".join(pair_to_string(pair) for pair in combo))
        counter += 1

def print_possible_doubles(players):
    print("Mögliche Doppelpaarungen:")
    for pair in combinations(players, 2):
        print(pair_to_string(pair))

def main():
    parser = argparse.ArgumentParser(description="Doppel Ohne Rechnen")
    parser.add_argument("--players", nargs="+", help="List of players with their start positions")
    parser.add_argument("--system", choices=["6PK", "4PK"], help="The system to use")

    args = parser.parse_args()

    if not args.players or not args.system:
        parser.print_help()
        return

    players = []
    for player in args.players:
        name, position = player.split(":")
        players.append((name.strip(), int(position.strip())))
    # sort by position to ensure deterministic combinations
    players.sort(key=lambda x: x[1])

    combinations = []
    if args.system == "6PK":
        # Implement 6er-Paarkreutz logic
        combinations_6pk = calculate_combinations_6erpk(players)
        combinations.extend(combinations_6pk)
    elif args.system == "4PK":
        # Implement 4er-Paarkreutz logic
        combinations_4pk = calculate_combinations_4erpk(players)
        combinations.extend(combinations_4pk)

    # Output the results
    print_combinations(combinations)

def test_calculate_combinations_4erpk():
    players = [("Alice", 1), ("Bob", 2), ("Charlie", 3), ("David", 4)]
    combinations = calculate_combinations_4erpk(players)
    # print_combinations(combinations)
    assert len(combinations) == 3

def test_calculate_combinations_6erpk():
    players = [("Alice", 1), ("Bob", 2), ("Charlie", 3), ("David", 4), ("Eve", 5), ("Frank", 6)]
    combinations = calculate_combinations_6erpk(players)
    # print_combinations(combinations)
    assert len(combinations) == 45
    
if __name__ == "__main__":
    # main()
    static_players = [("Timo", 1), ("Aaron", 2), ("Andreas", 3), ("Philipp", 4), ("Holger", 5), ("Marco", 6)]
    print_possible_doubles(static_players)
    combinations_6pk = calculate_combinations_6erpk(static_players)
    combinations_6pk = exclude_doubles(combinations_6pk, [(("Aaron", 2), ("Andreas", 3)), (("Aaron", 2), ("Holger", 5)), (("Andreas", 3), ("Holger", 5)), (("Timo", 1), ("Marco", 6)), (("Andreas", 3), ("Marco", 6))])
    print_combinations(combinations_6pk)
