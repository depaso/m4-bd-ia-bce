import re

boletin = (
    "Las exportaciones sumaron 3.253,37 millones de USD, con corte al 30 de septiembre de 2026. "
    "Las importaciones fueron 1.252,41 millones de USD, con un aumento de 4,5% frente al mes anterior. "
    "Los servicios llegaron a 387,11 millones de USD."
)

patron = re.compile(r"(\d{1,3}(?:\.\d{3})*(?:,\d+)?)\s+millones de USD")
convertir = lambda s: float(s.replace(".", "").replace(",", "."))

textos = patron.findall(boletin)
print(textos)
print([convertir(t) for t in textos])

try:
    float("3.253,37")
except ValueError as e:
    print("float directo falla:", e)

MESES = {"enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,"julio":7,
         "agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12}
p_fecha = re.compile(r"corte al (\d{1,2}) de (" + "|".join(MESES) + r") de (\d{4})")
d, mes, a = p_fecha.search(boletin).groups()
print(f"{a}-{MESES[mes]:02d}-{int(d):02d}")

p_pct = re.compile(r"(\d{1,3}(?:,\d+)?)%")
print(float(p_pct.search(boletin).group(1).replace(",", ".")))
