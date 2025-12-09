import matplotlib.pyplot as plt


# def plot_mf(x, mf_set, title):
#     plt.figure(figsize=(8, 5))
#     for name, (u, l) in mf_set.items():
#         plt.fill_between(x, l, u, alpha=0.3, label=name)
#     plt.title(title)
#     plt.legend()
#     plt.grid(True)
#     plt.show()


def plot_all_mf(domains, mf):
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # 1. Tinggi Tanaman
    for name, (u, l) in mf["height"].items():
        axs[0].fill_between(domains["height"], l, u, alpha=0.3, label=name)
    axs[0].set_title("MF Tinggi Tanaman")
    axs[0].legend()
    axs[0].grid(True)

    # 2. Jarak Lampu
    for name, (u, l) in mf["distance"].items():
        axs[1].fill_between(domains["distance"], l, u, alpha=0.3, label=name)
    axs[1].set_title("MF Jarak Lampu")
    axs[1].legend()
    axs[1].grid(True)

    # 3. Gerak Lampu
    for name, (u, l) in mf["output"].items():
        axs[2].fill_between(domains["output"], l, u, alpha=0.3, label=name)
    axs[2].set_title("MF Gerak Lampu")
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()
