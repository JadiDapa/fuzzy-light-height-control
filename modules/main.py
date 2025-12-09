from domains import create_domains
from membership import build_memberships
from rules import build_rules
from simulation import simulate
from plotting import plot_all_mf


def main():
    domains = create_domains()
    mf = build_memberships(domains)
    rules = build_rules()

    # Plot
    plot_all_mf(domains, mf)

    # Input
    plant_height = float(input("Tinggi tanaman (cm): "))
    lamp_distance = float(input("Jarak lampu (cm): "))

    simulate(domains, mf, rules, plant_height, lamp_distance)


if __name__ == "__main__":
    main()
