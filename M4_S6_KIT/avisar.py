"""Aviso de estado. Por defecto NO sale nada de la maquina: escribe en avisos.log."""
import os, json, logging, datetime
import urllib.request, urllib.parse

def avisar(mensaje, canal="archivo"):
    """canal: 'archivo' (por defecto), 'telegram' o 'gmail'. Solo se envia el ESTADO, nunca datos."""
    sello = datetime.datetime.now().isoformat(timespec="seconds")
    if canal == "telegram":
        token, chat = os.environ.get("TELEGRAM_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
        if not token or not chat:
            logging.warning("telegram sin secretos: se escribe en archivo"); canal = "archivo"
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            datos = urllib.parse.urlencode({"chat_id": chat, "text": mensaje}).encode()
            urllib.request.urlopen(urllib.request.Request(url, data=datos), timeout=10)
            return "telegram"
    if canal == "gmail":
        import smtplib; from email.message import EmailMessage
        usuario, clave, destino = (os.environ.get(k) for k in ("GMAIL_USER","GMAIL_APP_PASSWORD","GMAIL_DESTINO"))
        if not (usuario and clave and destino):
            logging.warning("gmail sin secretos: se escribe en archivo"); canal = "archivo"
        else:
            msg = EmailMessage(); msg["From"], msg["To"], msg["Subject"] = usuario, destino, "Estado del flujo"
            msg.set_content(mensaje)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as s:
                s.login(usuario, clave); s.send_message(msg)
            return "gmail"
    with open("avisos.log", "a", encoding="utf-8") as f:
        f.write(f"{sello} {mensaje}\n")
    return "archivo"
