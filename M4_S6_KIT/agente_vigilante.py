"""Agente vigilante de la fuente. Sin modelo de lenguaje: observa, decide, actua, con limites."""
import os, sys, json, time, subprocess, datetime
from avisar import avisar

OBJETIVO       = "Mantener el reporte al dia cuando cambie la fuente"
FUENTE         = "datos/exportaciones.csv"
MAX_PASOS      = 5          # limite de pasos
MAX_FALLOS     = 2          # fallos seguidos antes de parar
APROBAR_AVISO  = False      # False = borrador: el aviso NO sale hasta que una persona lo apruebe
BITACORA       = "bitacora.jsonl"

def registrar(paso, observo, decido, hice):
    with open(BITACORA, "a", encoding="utf-8") as f:
        f.write(json.dumps({"hora": datetime.datetime.now().isoformat(timespec="seconds"),
                            "paso": paso, "observo": observo, "decido": decido, "hice": hice},
                           ensure_ascii=False) + "\n")

# HERRAMIENTAS PERMITIDAS (lista cerrada). Lo que no esta aqui, el agente no puede hacerlo.
def leer_fuente():                      # solo lectura
    s = os.stat(FUENTE); return (s.st_size, int(s.st_mtime))
def correr_flujo():                     # escribe archivos locales
    r = subprocess.run([sys.executable, "flujo_exportaciones.py"], capture_output=True, text=True)
    return r.returncode
def aviso(msg):                         # sale hacia fuera: requiere aprobacion
    if not APROBAR_AVISO:
        return "BORRADOR (no enviado): " + msg
    return "enviado por " + avisar(msg)

def agente(espera=2):
    ultimo, fallos = None, 0
    for paso in range(1, MAX_PASOS + 1):
        obs = leer_fuente()
        if obs == ultimo:
            registrar(paso, str(obs), "sin cambio: no hago nada", "-")
        else:
            codigo = correr_flujo()
            fallos = 0 if codigo == 0 else fallos + 1
            hice = aviso(f"flujo {'OK' if codigo == 0 else 'FALLO'} ({codigo})")
            registrar(paso, str(obs), "cambio: corro el flujo", hice)
            ultimo = obs
        if fallos >= MAX_FALLOS:
            registrar(paso, "-", "PARO: fallos seguidos", "-"); return "paro por fallos"
        time.sleep(espera)
    registrar(MAX_PASOS, "-", "PARO: limite de pasos", "-")
    return "paro por limite de pasos"

if __name__ == "__main__":
    print(agente())
