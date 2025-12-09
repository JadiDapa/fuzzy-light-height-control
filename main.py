import numpy as np
import matplotlib.pyplot as plt


# ==============================================================
# 1. Gaussian Type-2
# ==============================================================
def gaussian_t2(x, mean, sigma_u, sigma_l):
    upper = np.exp(-0.5 * ((x - mean) / sigma_u) ** 2)
    lower = np.exp(-0.5 * ((x - mean) / sigma_l) ** 2)
    return upper, lower


# ==============================================================
# 2. Domain Generator
# ==============================================================
def create_domains():
    return {
        "height": np.linspace(0, 110, 300),
        "distance": np.linspace(0, 100, 300),
        "output": np.linspace(-50, 50, 300),
    }


# ==============================================================
# 3. Membership Function Builder
# ==============================================================
def build_memberships(domains):
    xh, xd, xo = domains["height"], domains["distance"], domains["output"]

    mf = {
        "height": {
            "semai": gaussian_t2(xh, 8, 4, 2),
            "vegetatif": gaussian_t2(xh, 30, 6, 3),
            "generatif": gaussian_t2(xh, 60, 6, 3),
            "produktif": gaussian_t2(xh, 90, 6, 3),
        },
        "distance": {
            "sangat_dekat": gaussian_t2(xd, 5, 3, 1.5),
            "dekat": gaussian_t2(xd, 15, 5, 3),
            "sedang": gaussian_t2(xd, 30, 6, 3),
            "jauh": gaussian_t2(xd, 50, 7, 4),
            "sangat_jauh": gaussian_t2(xd, 80, 7, 4),
        },
        "output": {
            "turun_banyak": gaussian_t2(xo, -30, 6, 3),
            "turun_sedikit": gaussian_t2(xo, -15, 5, 2),
            "diam": gaussian_t2(xo, 0, 4, 2),
            "naik_sedikit": gaussian_t2(xo, 15, 5, 2),
            "naik_banyak": gaussian_t2(xo, 30, 6, 3),
        },
    }
    return mf


# ==============================================================
# 4. Plotter
# ==============================================================
def plot_mf(x, mf_set, title):
    plt.figure(figsize=(8, 5))
    for name, (u, l) in mf_set.items():
        plt.fill_between(x, l, u, alpha=0.3, label=name)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Membership")
    plt.legend()
    plt.grid(True)
    plt.show()


# ==============================================================
# 5. Fuzzification
# ==============================================================
def fuzzify(val, x, mf):
    u = np.interp(val, x, mf[0])
    l = np.interp(val, x, mf[1])
    return (u + l) / 2


# ==============================================================
# 6. Rule Base Builder
# ==============================================================
def build_rules(mf_out):
    return [
        ("semai", "sangat_jauh", "turun_banyak"),
        ("semai", "jauh", "turun_banyak"),
        ("semai", "sedang", "turun_sedikit"),
        ("semai", "dekat", "diam"),
        ("semai", "sangat_dekat", "naik_sedikit"),
        ("vegetatif", "sangat_jauh", "turun_banyak"),
        ("vegetatif", "jauh", "turun_sedikit"),
        ("vegetatif", "sedang", "diam"),
        ("vegetatif", "dekat", "naik_sedikit"),
        ("vegetatif", "sangat_dekat", "naik_banyak"),
        ("generatif", "sangat_jauh", "turun_sedikit"),
        ("generatif", "jauh", "turun_sedikit"),
        ("generatif", "sedang", "diam"),
        ("generatif", "dekat", "naik_sedikit"),
        ("generatif", "sangat_dekat", "naik_banyak"),
        ("produktif", "sangat_jauh", "diam"),
        ("produktif", "jauh", "diam"),
        ("produktif", "sedang", "naik_sedikit"),
        ("produktif", "dekat", "naik_sedikit"),
        ("produktif", "sangat_dekat", "naik_banyak"),
    ]


# ==============================================================
# 7. Inference Engine
# ==============================================================
def infer(mf, domains, h_val, d_val, rules):
    xh, xd, xo = domains["height"], domains["distance"], domains["output"]

    μh = {k: fuzzify(h_val, xh, v) for k, v in mf["height"].items()}
    μd = {k: fuzzify(d_val, xd, v) for k, v in mf["distance"].items()}

    agg_u = np.zeros_like(xo)
    agg_l = np.zeros_like(xo)

    print("\n=== RULE AKTIF ===")
    for h, d, out in rules:
        strength = min(μh[h], μd[d])
        print(f"{h.upper()} & {d.upper()} -> {out.upper()} ({strength:.2f})")

        out_u, out_l = mf["output"][out]
        agg_u = np.fmax(agg_u, np.fmin(strength, out_u))
        agg_l = np.fmax(agg_l, np.fmin(strength, out_l))

    return agg_u, agg_l


# ==============================================================
# 8. Defuzzification
# ==============================================================
def defuzz(x, u, l):
    try:
        cu = np.sum(x * u) / np.sum(u)
        cl = np.sum(x * l) / np.sum(l)
        return (cu + cl) / 2
    except ZeroDivisionError:
        return 0


# ==============================================================
# 9. Closed Loop Simulation
# ==============================================================
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


# ==============================================================
# 10. Main Program
# ==============================================================
def main():
    domains = create_domains()
    mf = build_memberships(domains)
    rules = build_rules(mf)

    # Plot
    plot_mf(domains["height"], mf["height"], "MF Tinggi Tanaman")
    plot_mf(domains["distance"], mf["distance"], "MF Jarak Lampu")
    plot_mf(domains["output"], mf["output"], "MF Output Lampu")

    # Input
    plant_height = float(input("Tinggi Tanaman (cm): "))
    lamp_distance = float(input("Jarak Lampu (cm): "))

    simulate(domains, mf, rules, plant_height, lamp_distance)


if __name__ == "__main__":
    main()
