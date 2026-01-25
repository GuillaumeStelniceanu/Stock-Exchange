import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from ipywidgets import interact
from IPython.display import display

# --- Simulation PEA (imposition à la sortie) ---
def simulate_pea(initial, monthly, rate, months, tax_rate=0.172):
    values = []
    total_invested = initial
    value = initial

    for i in range(months):
        value = value * (1 + rate) + monthly
        total_invested += monthly
        values.append(value)

    gain = value - total_invested
    tax = gain * tax_rate if gain > 0 else 0
    net_value = value - tax
    net_gain = gain - tax

    # Calcul de la courbe nette mois par mois (pro-rata)
    pea_values_net = [v - ((v - total_invested) * tax_rate) for v in values]

    return net_value, total_invested, net_gain, tax, values, pea_values_net

# --- Simulation CTO (imposition annuelle au PFU) ---
def simulate_cto(initial, monthly, rate, months, tax_rate=0.30):
    values = []
    total_invested = initial
    value = initial
    total_tax = 0

    for i in range(months):
        new_value = value * (1 + rate) + monthly
        total_invested += monthly

        # Impôt une fois par an
        if (i + 1) % 12 == 0:
            gain = new_value - value - 12 * monthly
            if gain > 0:
                tax = gain * tax_rate
                new_value -= tax
                total_tax += tax

        value = new_value
        values.append(value)

    net_value = value
    net_gain = net_value - total_invested
    return net_value, total_invested, net_gain, total_tax, values

# --- Fonction principale interactive ---
def simulate(capital_initial=2000, versement_mensuel=200, annual_return=0.08, years=5):
    months = years * 12
    monthly_return = (1 + annual_return) ** (1/12) - 1

    pea_net, pea_invested, pea_gain_net, pea_tax, pea_values, pea_values_net = simulate_pea(
        capital_initial, versement_mensuel, monthly_return, months
    )
    cto_net, cto_invested, cto_gain_net, cto_tax, cto_values = simulate_cto(
        capital_initial, versement_mensuel, monthly_return, months
    )

    # Tableau comparatif
    df = pd.DataFrame({
        "Compte": ["PEA", "CTO"],
        "Capital investi (€)": [pea_invested, cto_invested],
        "Impôt payé (€)": [pea_tax, cto_tax],
        "Gain net (€)": [pea_gain_net, cto_gain_net],
        "Valeur nette finale (€)": [pea_net, cto_net]
    })

    display(df)

    # Graphique
    plt.figure(figsize=(10, 6))
    plt.plot(pea_values_net, label=f"PEA (net après PS à la sortie)", color="green")
    plt.plot(cto_values, label=f"CTO (imposition annuelle PFU)", color="red")
    plt.axhline(y=pea_net, color="green", linestyle="--", label=f"PEA net final: {pea_net:.0f} €")
    plt.axhline(y=cto_net, color="red", linestyle="--", label=f"CTO net final: {cto_net:.0f} €")
    plt.title("Évolution du portefeuille : PEA vs CTO (net après impôts)")
    plt.xlabel("Mois")
    plt.ylabel("Valeur du portefeuille (€)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- Interface interactive ---
interact(
    simulate,
    capital_initial=widgets.IntSlider(value=2000, min=0, max=20000, step=500, description="Capital initial (€)"),
    versement_mensuel=widgets.IntSlider(value=200, min=0, max=2000, step=50, description="Versement mensuel (€)"),
    annual_return=widgets.FloatSlider(value=0.08, min=0.01, max=0.20, step=0.01, description="Rendement annuel"),
    years=widgets.IntSlider(value=5, min=1, max=30, step=1, description="Durée (années)")
)
