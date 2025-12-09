import numpy as np
import matplotlib.pyplot as plt


# ==============================================================
# 1️⃣ Fungsi Gaussian Type-2
# ==============================================================
def gaussian_t2(x, mean, sigma_upper, sigma_lower):
    upper = np.exp(-0.5 * ((x - mean) / sigma_upper) ** 2)
    lower = np.exp(-0.5 * ((x - mean) / sigma_lower) ** 2)
    return upper, lower


# ==============================================================
# 2️⃣ Domain (Semesta Pembahasan)
# ==============================================================
x_height = np.linspace(0, 110, 300)  # tinggi tanaman (cm)
x_distance = np.linspace(0, 100, 300)  # jarak lampu (cm)
x_output = np.linspace(-50, 50, 300)  # pergerakan lampu (cm)

# ==============================================================
# 3️⃣ Fuzzy Set (Fungsi Keanggotaan)
# ==============================================================
# Tinggi tanaman berdasarkan Fasenya
semai_u, semai_l = gaussian_t2(x_height, 8, 4, 2)  # Semai
vegetatif_u, vegetatif_l = gaussian_t2(x_height, 30, 6, 3)  # Vegetatif
generatif_u, generatif_l = gaussian_t2(x_height, 60, 6, 3)  # Generatif
produktif_u, produktif_l = gaussian_t2(x_height, 90, 6, 3)  # Produktif

# Jarak lampu
sangat_dekat_u, sangat_dekat_l = gaussian_t2(x_distance, 5, 3, 1.5)  # Sangat Dekat
dekat_u, dekat_l = gaussian_t2(x_distance, 15, 5, 3)  # Dekat
sedang_u, sedang_l = gaussian_t2(x_distance, 30, 6, 3)  # Sedang
jauh_u, jauh_l = gaussian_t2(x_distance, 50, 7, 4)  # Jauh
sangat_jauh_u, sangat_jauh_l = gaussian_t2(x_distance, 80, 7, 4)  # Sangat Jauh

# Pergerakan lampu
turun_banyak_u, turun_banyak_l = gaussian_t2(x_output, -30, 6, 3)  # Turun Banyak
turun_sedikit_u, turun_sedikit_l = gaussian_t2(x_output, -15, 5, 2)  # Turun Sedikit
diam_u, diam_l = gaussian_t2(x_output, 0, 4, 2)  # Diam
naik_sedikit_u, naik_sedikit_l = gaussian_t2(x_output, 15, 5, 2)  # Naik Sedikit
naik_banyak_u, naik_banyak_l = gaussian_t2(x_output, 30, 6, 3)  # Naik Banyak

# ==============================================================
# 4️⃣ Plot Membership Function
# ==============================================================
# ---- Plot tinggi tanaman ----
plt.figure(figsize=(8, 5))
plt.fill_between(x_height, semai_l, semai_u, alpha=0.3, label="Semai")
plt.fill_between(x_height, vegetatif_l, vegetatif_u, alpha=0.3, label="Vegetatif")
plt.fill_between(x_height, generatif_l, generatif_u, alpha=0.3, label="Generatif")
plt.fill_between(x_height, produktif_l, produktif_u, alpha=0.3, label="Produktif")
plt.title("Fuzzy Type-2 Membership Functions (Tinggi Tanaman)")
plt.xlabel("Tinggi (cm)")
plt.ylabel("Derajat Keanggotaan")
plt.legend()
plt.grid(True)
plt.show()

# ---- Plot jarak lampu ----
plt.figure(figsize=(8, 5))
plt.fill_between(
    x_distance, sangat_dekat_l, sangat_dekat_u, alpha=0.3, label="Sangat Dekat"
)
plt.fill_between(x_distance, dekat_l, dekat_u, alpha=0.3, label="Dekat")
plt.fill_between(x_distance, sedang_l, sedang_u, alpha=0.3, label="Sedang")
plt.fill_between(x_distance, jauh_l, jauh_u, alpha=0.3, label="Jauh")
plt.fill_between(
    x_distance, sangat_jauh_l, sangat_jauh_u, alpha=0.3, label="Sangat Jauh"
)
plt.title("Fuzzy Type-2 Membership Functions (Jarak Lampu)")
plt.xlabel("Jarak (cm)")
plt.ylabel("Derajat Keanggotaan")
plt.legend()
plt.grid(True)
plt.show()

# ---- Plot output lampu ----
plt.figure(figsize=(8, 5))
plt.fill_between(
    x_output, turun_banyak_l, turun_banyak_u, alpha=0.3, label="Turun Banyak"
)
plt.fill_between(
    x_output, turun_sedikit_l, turun_sedikit_u, alpha=0.3, label="Turun Sedikit"
)
plt.fill_between(x_output, diam_l, diam_u, alpha=0.3, label="Diam")
plt.fill_between(
    x_output, naik_sedikit_l, naik_sedikit_u, alpha=0.3, label="Naik Sedikit"
)
plt.fill_between(x_output, naik_banyak_l, naik_banyak_u, alpha=0.3, label="Naik Banyak")
plt.title("Fuzzy Type-2 Membership Functions (Pergerakan Lampu)")
plt.xlabel("Pergerakan (cm)")
plt.ylabel("Derajat Keanggotaan")
plt.legend()
plt.grid(True)
plt.show()


# ==============================================================
# 5️⃣ Input dari Sensor (Simulasi)
# ==============================================================
plant_height = float(input("Tinggi Tanaman (cm): "))
lamp_distance = float(input("Jarak Lampu (cm): "))

# Proteksi agar tetap dalam domain
plant_height = np.clip(plant_height, x_height.min(), x_height.max())
lamp_distance = np.clip(lamp_distance, x_distance.min(), x_distance.max())


# ==============================================================
# 6️⃣ Fuzzifikasi
# ==============================================================
def fuzzify(value, x, mf):
    upper = np.interp(value, x, mf[0])
    lower = np.interp(value, x, mf[1])
    return (upper + lower) / 2  # ambil rata-rata


μ_semai = fuzzify(plant_height, x_height, (semai_u, semai_l))
μ_vegetatif = fuzzify(plant_height, x_height, (vegetatif_u, vegetatif_l))
μ_generatif = fuzzify(plant_height, x_height, (generatif_u, generatif_l))
μ_produktif = fuzzify(plant_height, x_height, (produktif_u, produktif_l))


# ==============================
# Fuzzifikasi jarak lampu
# ==============================
μ_sangat_dekat = fuzzify(lamp_distance, x_distance, (sangat_dekat_u, sangat_dekat_l))
μ_dekat = fuzzify(lamp_distance, x_distance, (dekat_u, dekat_l))
μ_sedang = fuzzify(lamp_distance, x_distance, (sedang_u, sedang_l))
μ_jauh = fuzzify(lamp_distance, x_distance, (jauh_u, jauh_l))
μ_sangat_jauh = fuzzify(lamp_distance, x_distance, (sangat_jauh_u, sangat_jauh_l))


# ==============================================================
# 7️⃣ Rule Base (Deskriptif)
# ==============================================================
rules = [
    # ==============================
    # SEMAI
    # ==============================
    (
        "Semai & Sangat Jauh",
        "Lampu TURUN BANYAK",
        min(μ_semai, μ_sangat_jauh),
        (turun_banyak_u, turun_banyak_l),
    ),
    (
        "Semai & Jauh",
        "Lampu TURUN BANYAK",
        min(μ_semai, μ_jauh),
        (turun_banyak_u, turun_banyak_l),
    ),
    (
        "Semai & Sedang",
        "Lampu TURUN SEDIKIT",
        min(μ_semai, μ_sedang),
        (turun_sedikit_u, turun_sedikit_l),
    ),
    ("Semai & Dekat", "Lampu DIAM", min(μ_semai, μ_dekat), (diam_u, diam_l)),
    (
        "Semai & Sangat Dekat",
        "Lampu NAIK SEDIKIT",
        min(μ_semai, μ_sangat_dekat),
        (naik_sedikit_u, naik_sedikit_l),
    ),
    # ==============================
    # VEGETATIF
    # ==============================
    (
        "Vegetatif & Sangat Jauh",
        "Lampu TURUN BANYAK",
        min(μ_vegetatif, μ_sangat_jauh),
        (turun_banyak_u, turun_banyak_l),
    ),
    (
        "Vegetatif & Jauh",
        "Lampu TURUN SEDIKIT",
        min(μ_vegetatif, μ_jauh),
        (turun_sedikit_u, turun_sedikit_l),
    ),
    ("Vegetatif & Sedang", "Lampu DIAM", min(μ_vegetatif, μ_sedang), (diam_u, diam_l)),
    (
        "Vegetatif & Dekat",
        "Lampu NAIK SEDIKIT",
        min(μ_vegetatif, μ_dekat),
        (naik_sedikit_u, naik_sedikit_l),
    ),
    (
        "Vegetatif & Sangat Dekat",
        "Lampu NAIK BANYAK",
        min(μ_vegetatif, μ_sangat_dekat),
        (naik_banyak_u, naik_banyak_l),
    ),
    # ==============================
    # GENERATIF
    # ==============================
    (
        "Generatif & Sangat Jauh",
        "Lampu TURUN SEDIKIT",
        min(μ_generatif, μ_sangat_jauh),
        (turun_sedikit_u, turun_sedikit_l),
    ),
    (
        "Generatif & Jauh",
        "Lampu TURUN SEDIKIT",
        min(μ_generatif, μ_jauh),
        (turun_sedikit_u, turun_sedikit_l),
    ),
    ("Generatif & Sedang", "Lampu DIAM", min(μ_generatif, μ_sedang), (diam_u, diam_l)),
    (
        "Generatif & Dekat",
        "Lampu NAIK SEDIKIT",
        min(μ_generatif, μ_dekat),
        (naik_sedikit_u, naik_sedikit_l),
    ),
    (
        "Generatif & Sangat Dekat",
        "Lampu NAIK BANYAK",
        min(μ_generatif, μ_sangat_dekat),
        (naik_banyak_u, naik_banyak_l),
    ),
    # ==============================
    # PRODUKTIF
    # ==============================
    (
        "Produktif & Sangat Jauh",
        "Lampu DIAM",
        min(μ_produktif, μ_sangat_jauh),
        (diam_u, diam_l),
    ),
    ("Produktif & Jauh", "Lampu DIAM", min(μ_produktif, μ_jauh), (diam_u, diam_l)),
    (
        "Produktif & Sedang",
        "Lampu NAIK SEDIKIT",
        min(μ_produktif, μ_sedang),
        (naik_sedikit_u, naik_sedikit_l),
    ),
    (
        "Produktif & Dekat",
        "Lampu NAIK SEDIKIT",
        min(μ_produktif, μ_dekat),
        (naik_sedikit_u, naik_sedikit_l),
    ),
    (
        "Produktif & Sangat Dekat",
        "Lampu NAIK BANYAK",
        min(μ_produktif, μ_sangat_dekat),
        (naik_banyak_u, naik_banyak_l),
    ),
]


# ==============================================================
# 8️⃣ Agregasi Output
# ==============================================================
aggregated_upper = np.zeros_like(x_output)
aggregated_lower = np.zeros_like(x_output)

print("=== RULE AKTIF ===")
for desc, action, strength, mf in rules:
    print(f"Jika {desc} → {action} (derajat: {strength:.2f})")
    aggregated_upper = np.fmax(aggregated_upper, np.fmin(strength, mf[0]))
    aggregated_lower = np.fmax(aggregated_lower, np.fmin(strength, mf[1]))


# ==============================================================
# 9️⃣ Defuzzifikasi (Centroid)
# ==============================================================
def defuzz(x, upper, lower):
    try:
        c_upper = np.sum(x * upper) / np.sum(upper)
        c_lower = np.sum(x * lower) / np.sum(lower)
        return (c_upper + c_lower) / 2
    except ZeroDivisionError:
        return 0


lamp_movement = defuzz(x_output, aggregated_upper, aggregated_lower)

print(f"\nHasil Akhir: Lampu bergerak sebesar {lamp_movement:.2f} cm")


# ==============================================================
# 🔟 Visualisasi Output Akhir
# ==============================================================
plt.figure(figsize=(8, 5))
plt.fill_between(
    x_output, aggregated_lower, aggregated_upper, color="orange", alpha=0.5
)
plt.title("Output Fuzzy Type-2: Pergerakan Lampu Gantung")
plt.xlabel("Pergerakan Lampu (cm)")
plt.ylabel("Derajat Keanggotaan")
plt.grid(True)
plt.show()


# ==============================================================
# 🔁 11️⃣ Simulasi Closed-Loop Sampai Stabil
# ==============================================================

# Parameter simulasi
max_epoch = 50
threshold_stable = 0.1  # cm (batas stabil)
lamp_position = lamp_distance  # posisi awal lampu

print("\n=== SIMULASI GERAK LAMPU SAMPAI STABIL ===")

for epoch in range(max_epoch):
    # Hitung ulang jarak aktual lampu ke pucuk
    current_distance = lamp_position

    # Re-fuzzifikasi jarak (continuous update)
    μ_sangat_dekat = fuzzify(
        current_distance, x_distance, (sangat_dekat_u, sangat_dekat_l)
    )
    μ_dekat = fuzzify(current_distance, x_distance, (dekat_u, dekat_l))
    μ_sedang = fuzzify(current_distance, x_distance, (sedang_u, sedang_l))
    μ_jauh = fuzzify(current_distance, x_distance, (jauh_u, jauh_l))
    μ_sangat_jauh = fuzzify(
        current_distance, x_distance, (sangat_jauh_u, sangat_jauh_l)
    )

    # Rebuild rules strength
    aggregated_upper[:] = 0
    aggregated_lower[:] = 0

    for desc, action, _, mf in rules:
        # Hitung ulang strength dari kondisi terbaru
        if "Semai" in desc:
            hμ = μ_semai
        elif "Vegetatif" in desc:
            hμ = μ_vegetatif
        elif "Generatif" in desc:
            hμ = μ_generatif
        else:
            hμ = μ_produktif

        if "Sangat Dekat" in desc:
            dμ = μ_sangat_dekat
        elif "Dekat" in desc:
            dμ = μ_dekat
        elif "Sedang" in desc:
            dμ = μ_sedang
        elif "Sangat Jauh" in desc:
            dμ = μ_sangat_jauh
        else:
            dμ = μ_jauh

        strength = min(hμ, dμ)

        aggregated_upper = np.fmax(aggregated_upper, np.fmin(strength, mf[0]))
        aggregated_lower = np.fmax(aggregated_lower, np.fmin(strength, mf[1]))

    # Defuzz hasil epoch ini
    movement = defuzz(x_output, aggregated_upper, aggregated_lower)

    # Update posisi lampu
    new_position = lamp_position + movement

    # Print hasil epoch
    print(
        f"Epoch {epoch+1:02d} | "
        f"Jarak: {lamp_position:.2f} cm | "
        f"Gerak: {movement:.2f} cm | "
        f"Posisi Baru: {new_position:.2f} cm"
    )

    # Cek stabil
    if abs(movement) < threshold_stable:
        print("\n✅ Lampu sudah stabil.")
        break

    lamp_position = new_position
else:
    print("\n⚠️ Maksimum epoch tercapai, sistem belum sepenuhnya stabil.")
