import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# CONFIG
st.set_page_config(page_title="Fuzzy Type-2 Grow Light", layout="wide")
st.title("🌱 Fuzzy Type-2 Grow Light Controller (Streamlit)")


# Fungsi
def gaussian_t2(x, mean, sigma_upper, sigma_lower):
    upper = np.exp(-0.5 * ((x - mean) / sigma_upper) ** 2)
    lower = np.exp(-0.5 * ((x - mean) / sigma_lower) ** 2)
    return upper, lower


def fuzzify(value, x, mf):
    upper = np.interp(value, x, mf[0])
    lower = np.interp(value, x, mf[1])
    return (upper + lower) / 2


def defuzz(x, upper, lower):
    if np.sum(upper) == 0 or np.sum(lower) == 0:
        return 0
    c_upper = np.sum(x * upper) / np.sum(upper)
    c_lower = np.sum(x * lower) / np.sum(lower)
    return (c_upper + c_lower) / 2


# Domain
x_height = np.linspace(0, 110, 300)
x_distance = np.linspace(0, 100, 300)
x_output = np.linspace(-50, 50, 300)

# Membership Functions
mf_height = {
    "Semai": gaussian_t2(x_height, 8, 4, 2),
    "Vegetatif": gaussian_t2(x_height, 30, 6, 3),
    "Generatif": gaussian_t2(x_height, 60, 6, 3),
    "Produktif": gaussian_t2(x_height, 90, 6, 3),
}

mf_distance = {
    "Sangat Dekat": gaussian_t2(x_distance, 5, 3, 1.5),
    "Dekat": gaussian_t2(x_distance, 15, 5, 3),
    "Sedang": gaussian_t2(x_distance, 30, 6, 3),
    "Jauh": gaussian_t2(x_distance, 50, 7, 4),
    "Sangat Jauh": gaussian_t2(x_distance, 80, 7, 4),
}

mf_output = {
    "Turun Banyak": gaussian_t2(x_output, -30, 6, 3),
    "Turun Sedikit": gaussian_t2(x_output, -15, 5, 2),
    "Diam": gaussian_t2(x_output, 0, 4, 2),
    "Naik Sedikit": gaussian_t2(x_output, 15, 5, 2),
    "Naik Banyak": gaussian_t2(x_output, 30, 6, 3),
}

# Sidebar Input
st.sidebar.header("🔧 Input Sensor")

plant_height = st.sidebar.slider("Tinggi Tanaman (cm)", 0.0, 110.0, 30.0)
lamp_distance = st.sidebar.slider("Jarak Lampu (cm)", 0.0, 100.0, 40.0)
max_epoch = st.sidebar.slider("Batas Epoch Simulasi", 5, 50, 15)
stabil_threshold = st.sidebar.slider("Threshold Stabil (cm)", 0.01, 1.0, 0.05)

# Layout
col1, col2 = st.columns(2)

# PLOT Membership
with col1:
    st.subheader("📊 Membership Functions")

    fig, axs = plt.subplots(3, 1, figsize=(7, 10))

    # Height
    for name, (u, l) in mf_height.items():
        axs[0].fill_between(x_height, l, u, alpha=0.3, label=name)
    axs[0].set_title("Membership Tinggi Tanaman")
    axs[0].legend()
    axs[0].grid(True)

    # Distance
    for name, (u, l) in mf_distance.items():
        axs[1].fill_between(x_distance, l, u, alpha=0.3, label=name)
    axs[1].set_title("Membership Jarak Lampu")
    axs[1].legend()
    axs[1].grid(True)

    # Output
    for name, (u, l) in mf_output.items():
        axs[2].fill_between(x_output, l, u, alpha=0.3, label=name)
    axs[2].set_title("Membership Gerak Lampu")
    axs[2].legend()
    axs[2].grid(True)

    st.pyplot(fig)

# FUZZIFIKASI
with col2:
    st.subheader("🔎 Fuzzifikasi")

    μ = {
        "Semai": fuzzify(plant_height, x_height, mf_height["Semai"]),
        "Vegetatif": fuzzify(plant_height, x_height, mf_height["Vegetatif"]),
        "Generatif": fuzzify(plant_height, x_height, mf_height["Generatif"]),
        "Produktif": fuzzify(plant_height, x_height, mf_height["Produktif"]),
        "Sangat Dekat": fuzzify(lamp_distance, x_distance, mf_distance["Sangat Dekat"]),
        "Dekat": fuzzify(lamp_distance, x_distance, mf_distance["Dekat"]),
        "Sedang": fuzzify(lamp_distance, x_distance, mf_distance["Sedang"]),
        "Jauh": fuzzify(lamp_distance, x_distance, mf_distance["Jauh"]),
        "Sangat Jauh": fuzzify(lamp_distance, x_distance, mf_distance["Sangat Jauh"]),
    }

    for k, v in μ.items():
        st.write(f"{k}: **{v:.3f}**")

# INFERENSI + SIMULASI
st.subheader("⚙️ Simulasi Kontrol Lampu")

if st.button("Mulai Simulasi"):
    current_distance = lamp_distance
    history = []

    placeholder = st.empty()

    for epoch in range(max_epoch):

        μ_d = {
            "Sangat Dekat": fuzzify(
                current_distance, x_distance, mf_distance["Sangat Dekat"]
            ),
            "Dekat": fuzzify(current_distance, x_distance, mf_distance["Dekat"]),
            "Sedang": fuzzify(current_distance, x_distance, mf_distance["Sedang"]),
            "Jauh": fuzzify(current_distance, x_distance, mf_distance["Jauh"]),
            "Sangat Jauh": fuzzify(
                current_distance, x_distance, mf_distance["Sangat Jauh"]
            ),
        }

        μ_h = {
            "Semai": fuzzify(plant_height, x_height, mf_height["Semai"]),
            "Vegetatif": fuzzify(plant_height, x_height, mf_height["Vegetatif"]),
            "Generatif": fuzzify(plant_height, x_height, mf_height["Generatif"]),
            "Produktif": fuzzify(plant_height, x_height, mf_height["Produktif"]),
        }

        rules = [
            ("Semai", "Sangat Dekat", "Naik Sedikit"),
            ("Semai", "Dekat", "Diam"),
            ("Semai", "Sedang", "Turun Sedikit"),
            ("Semai", "Jauh", "Turun Banyak"),
            ("Semai", "Sangat Jauh", "Turun Banyak"),
            ("Vegetatif", "Sangat Dekat", "Naik Banyak"),
            ("Vegetatif", "Dekat", "Naik Sedikit"),
            ("Vegetatif", "Sedang", "Diam"),
            ("Vegetatif", "Jauh", "Turun Sedikit"),
            ("Vegetatif", "Sangat Jauh", "Turun Banyak"),
            ("Generatif", "Sangat Dekat", "Naik Banyak"),
            ("Generatif", "Dekat", "Naik Sedikit"),
            ("Generatif", "Sedang", "Diam"),
            ("Generatif", "Jauh", "Turun Sedikit"),
            ("Generatif", "Sangat Jauh", "Turun Sedikit"),
            ("Produktif", "Sangat Dekat", "Naik Banyak"),
            ("Produktif", "Dekat", "Naik Sedikit"),
            ("Produktif", "Sedang", "Naik Sedikit"),
            ("Produktif", "Jauh", "Diam"),
            ("Produktif", "Sangat Jauh", "Diam"),
        ]

        aggregated_upper = np.zeros_like(x_output)
        aggregated_lower = np.zeros_like(x_output)

        for h, d, out in rules:
            strength = min(μ_h[h], μ_d[d])
            out_u, out_l = mf_output[out]
            aggregated_upper = np.fmax(aggregated_upper, np.fmin(strength, out_u))
            aggregated_lower = np.fmax(aggregated_lower, np.fmin(strength, out_l))

        move = defuzz(x_output, aggregated_upper, aggregated_lower)

        new_distance = current_distance + move
        delta = abs(new_distance - current_distance)

        history.append((epoch + 1, current_distance, move, new_distance, delta))

        current_distance = new_distance

        if delta < stabil_threshold:
            break

    # ===============================
    # Tampilkan hasil
    # ===============================
    st.write("### 🔄 Hasil Simulasi")

    st.table(
        {
            "Epoch": [h[0] for h in history],
            "Jarak Awal (cm)": [round(h[1], 2) for h in history],
            "Gerak Lampu (cm)": [round(h[2], 2) for h in history],
            "Jarak Baru (cm)": [round(h[3], 2) for h in history],
            "Delta": [round(h[4], 4) for h in history],
        }
    )
