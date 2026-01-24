import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Paramètres
capital_initial = 2000          # Montant initial investi sur chaque compte
versement_mensuel = 200         # Versements mensuels réguliers
annual_return = 0.08            # Rendement annuel estimé (8%)
years = 5
months = years * 12
monthly_return = (1 + annual_return) ** (1/12) - 1  # Rendement mensuel

# Fiscalité
fiscal_pea = 0.172   # PEA : PS uniquement à la sortie
fiscal_cto = 0.30    # CTO : PFU chaque année

# --- Simulation PEA (imposition uniquement à la sortie) ---
def simulate_pea(initial, monthly, rate, months, tax_rate):
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
    return net_value, total_invested, net_gain, tax, values

# --- Simulation CTO (imposition annuelle sur les gains) ---
def simulate_cto(initial, monthly, rate, months, tax_rate):
    values = []
    total_invested = initial
    value = initial

    for i in range(months):
        # Croissance brute du portefeuille
        new_value = value * (1 + rate) + monthly
        total_invested += monthly

        # Gain de l'année (si on est à la fin d'une année complète)
        if (i + 1) % 12 == 0:  # chaque année
            gain = new_value - value - 12 * monthly  # gains de l'année
            if gain > 0:
                tax = gain * tax_rate
                new_value -= tax

        value = new_value
        values.append(value)

    net_value = value
    gain = value - total_invested
    net_gain = gain
    tax_total = (total_invested + net_gain + 1) - value  # approximation du cumul d’impôts
    return net_value, total_invested, net_gain, tax_total, values

# Simulations
pea_net, pea_invested, pea_gain_net, pea_tax, pea_values = simulate_pea(
    capital_initial, versement_mensuel, monthly_return, months, fiscal_pea
)
cto_net, cto_invested, cto_gain_net, cto_tax, cto_values = simulate_cto(
    capital_initial, versement_mensuel, monthly_return, months, fiscal_cto
)

# Résumé comparatif
df = pd.DataFrame({
    "Compte": ["PEA", "CTO"],
    "Capital investi (€)": [pea_invested, cto_invested],
    "Impôt payé (€)": [pea_tax, cto_tax],
    "Gain net (€)": [pea_gain_net, cto_gain_net],
    "Valeur nette finale (€)": [pea_net, cto_net]
})

print(df)

# Graphique comparatif
plt.figure(figsize=(10, 6))
plt.plot(pea_values, label=f"PEA (net après PS à la sortie)", color="green")
plt.plot(cto_values, label=f"CTO (imposition annuelle au PFU)", color="red")
plt.axhline(y=pea_net, color="green", linestyle="--", label=f"PEA net final: {pea_net:.0f} €")
plt.axhline(y=cto_net, color="red", linestyle="--", label=f"CTO net final: {cto_net:.0f} €")
plt.title("Évolution portefeuille : PEA vs CTO (simulation réaliste)")
plt.xlabel("Mois")
plt.ylabel("Valeur du portefeuille (€)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
