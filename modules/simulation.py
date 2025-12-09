from inference import infer
from defuzzification import defuzz


def simulate(
    domains, mf, rules, plant_height, lamp_distance, max_epoch=50, stable_th=1
):
    xo = domains["output"]
    pos = lamp_distance

    print("\n=== SIMULASI CLOSED LOOP ===")

    for i in range(max_epoch):
        agg_u, agg_l = infer(plant_height, pos, domains, mf, rules)
        move = defuzz(xo, agg_u, agg_l)
        new_pos = pos + move

        print(f"Epoch {i+1:02d} | Pos: {pos:.2f} | Move: {move:.2f}")

        if abs(move) < stable_th:
            print("✅ Sistem stabil")
            break

        pos = new_pos
