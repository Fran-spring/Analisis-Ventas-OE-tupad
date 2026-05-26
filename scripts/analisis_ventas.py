import pandas as pd
import matplotlib.pyplot as plt
import os

DATOS_PATH = os.path.join("datos", "ventas.csv")

if not os.path.exists(DATOS_PATH):
    print("Dataset no encontrado. Generando datos de ejemplo...")
    import numpy as np

    os.makedirs("datos", exist_ok=True)

    np.random.seed(42)
    productos = ["Laptop", "Mouse", "Teclado", "Monitor", "Auriculares"]
    fechas = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")

    rows = []
    for fecha in fechas:
        n_ventas = np.random.randint(1, 6)
        for _ in range(n_ventas):
            producto = np.random.choice(productos)
            cantidad = np.random.randint(1, 10)
            precio_unitario = {
                "Laptop": 1200,
                "Mouse": 25,
                "Teclado": 45,
                "Monitor": 350,
                "Auriculares": 80,
            }[producto]
            rows.append(
                {
                    "fecha": fecha.strftime("%Y-%m-%d"),
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                }
            )

    df_ejemplo = pd.DataFrame(rows)
    df_ejemplo.to_csv(DATOS_PATH, index=False)
    print(f"Dataset de ejemplo guardado en: {DATOS_PATH}")

df = pd.read_csv(DATOS_PATH, parse_dates=["fecha"])
print(f"\nDataset cargado: {len(df)} registros.")
print(df.head())


df["monto_total"] = df["cantidad"] * df["precio_unitario"]

df["mes"] = df["fecha"].dt.to_period("M")


ventas_totales = df["monto_total"].sum()
print(f"\n--- INDICADORES ---")
print(f"Ventas totales: $ {ventas_totales:,.2f}")

ventas_por_producto = (
    df.groupby("producto")["cantidad"].sum().sort_values(ascending=False)
)
producto_top = ventas_por_producto.index[0]
cantidad_top = ventas_por_producto.iloc[0]
print(f"Producto más vendido: {producto_top} ({cantidad_top} unidades)")

ventas_por_mes = df.groupby("mes")["monto_total"].sum()
print("\nVentas por mes:")
print(ventas_por_mes.to_string())


os.makedirs("resultados", exist_ok=True)

ventas_por_mes_df = ventas_por_mes.reset_index()
ventas_por_mes_df.columns = ["mes", "monto_total"]
ventas_por_mes_df.to_csv(
    os.path.join("resultados", "ventas_por_mes.csv"), index=False
)
print("\nResumen mensual guardado en resultados/ventas_por_mes.csv")

ventas_por_producto.to_csv(
    os.path.join("resultados", "ventas_por_producto.csv")
)
print("Resumen por producto guardado en resultados/ventas_por_producto.csv")


fig, ax = plt.subplots(figsize=(12, 5))

meses_str = [str(m) for m in ventas_por_mes.index]
ax.plot(
    meses_str,
    ventas_por_mes.values,
    marker="o",
    linewidth=2,
    color="#2563EB",
    markerfacecolor="#1D4ED8",
    markersize=6,
)
ax.fill_between(
    range(len(meses_str)),
    ventas_por_mes.values,
    alpha=0.15,
    color="#2563EB",
)

ax.set_title("Evolución de Ventas Mensuales – 2024", fontsize=14, fontweight="bold")
ax.set_xlabel("Mes", fontsize=11)
ax.set_ylabel("Monto de Ventas ($)", fontsize=11)
ax.set_xticks(range(len(meses_str)))
ax.set_xticklabels(meses_str, rotation=45, ha="right")
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x:,.0f}")
)
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

grafico_path = os.path.join("resultados", "evolucion_ventas.png")
plt.savefig(grafico_path, dpi=150)
plt.show()
print(f"\nGráfico guardado en: {grafico_path}")


print("\n========== RESUMEN FINAL ==========")
print(f"Total de registros analizados : {len(df)}")
print(f"Ventas totales                : $ {ventas_totales:,.2f}")
print(f"Producto más vendido          : {producto_top} ({cantidad_top} uds.)")
print(f"Mes con mayor venta           : {ventas_por_mes.idxmax()} "
      f"($ {ventas_por_mes.max():,.2f})")
print(f"Mes con menor venta           : {ventas_por_mes.idxmin()} "
      f"($ {ventas_por_mes.min():,.2f})")
