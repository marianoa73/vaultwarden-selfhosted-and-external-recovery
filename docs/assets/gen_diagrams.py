#!/usr/bin/env python3
"""Rebuild every diagram in English (*.en) and Spanish (*.es) as SVG + PNG. Needs Pillow for the PNG files.
Run: python3 docs/assets/gen_diagrams.py"""
import math
from html import escape
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
BG, BOX, FG, MUTED, ACCENT, LINE = '#0F1115', '#202630', '#EDF0F4', '#BBC5D4', '#C0602B', '#596778'
SAFE = '#4F8F6B'


class D:
    def __init__(self, title, subtitle, h=840, w=1400):
        self.w, self.h = w, h
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><rect width="{w}" height="{h}" fill="{BG}"/>']
        self.im = Image.new('RGB', (w, h), BG)
        self.d = ImageDraw.Draw(self.im)
        if title:
            self.text(50, 48, title, 34, FG, True)
            self.text(50, 95, subtitle, 20, MUTED)

    def text(self, x, y, t, size=21, color=FG, bold=False, anchor='left'):
        f = ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf', size)
        self.d.text((x, y), t, font=f, fill=color, anchor='mm' if anchor == 'middle' else ('rm' if anchor == 'right' else 'lm'))
        a = {'middle': 'middle', 'right': 'end'}.get(anchor, 'start')
        self.svg.append(f'<text x="{x}" y="{y}" dominant-baseline="middle" text-anchor="{a}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(t)}</text>')

    def rect(self, x, y, w, h, fill=BOX, stroke=LINE, r=16, sw=3):
        self.d.rounded_rectangle((x, y, x + w, y + h), radius=r, fill=fill, outline=None if stroke == 'none' else stroke, width=sw)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def box(self, x, y, w, h, title, lines=(), accent=False, fs=23):
        self.rect(x, y, w, h, BOX, ACCENT if accent else LINE)
        start = y + h / 2 - (len(lines) * 30) / 2
        self.text(x + w / 2, start, title, fs, FG, True, 'middle')
        for i, t in enumerate(lines):
            self.text(x + w / 2, start + (i + 1) * 30, t, 19, MUTED, False, 'middle')

    def line(self, pts):
        self.d.line(pts, fill=ACCENT, width=4)
        self.svg.append('<polyline points="' + ' '.join(f'{a},{b}' for a, b in pts) + f'" fill="none" stroke="{ACCENT}" stroke-width="4"/>')

    def arrow(self, pts, label=None):
        self.d.line(pts, fill=ACCENT, width=4, joint='curve')
        x, y = pts[-1]; px, py = pts[-2]; a = math.atan2(y - py, x - px)
        tri = [(x, y), (x - 14 * math.cos(a - .5), y - 14 * math.sin(a - .5)), (x - 14 * math.cos(a + .5), y - 14 * math.sin(a + .5))]
        self.d.polygon(tri, fill=ACCENT)
        self.svg.append('<polyline points="' + ' '.join(f'{a},{b}' for a, b in pts) + f'" fill="none" stroke="{ACCENT}" stroke-width="4"/>')
        self.svg.append('<polygon points="' + ' '.join(f'{a},{b}' for a, b in tri) + f'" fill="{ACCENT}"/>')
        if label:
            self.text(*label, 18, FG)

    def save(self, name):
        (OUT / (name + '.svg')).write_text(''.join(self.svg) + '</svg>\n')
        self.im.save(OUT / (name + '.png'))



def overview(L, T):
    s = D(T['t1'], T['s1'], 920)
    s.box(50, 190, 250, 140, T['dev'][0], T['dev'][1])
    s.box(370, 190, 250, 140, T['vpn'][0], T['vpn'][1])
    s.arrow([(300, 260), (370, 260)]); s.arrow([(620, 260), (690, 260)])
    s.rect(690, 150, 660, 220, '#171C24', ACCENT, 20)
    s.text(1020, 182, T['primary'], 23, FG, True, 'middle')
    s.box(715, 210, 290, 130, T['vw'][0], T['vw'][1])
    s.box(1035, 210, 290, 130, T['data'][0], T['data'][1])
    s.arrow([(1005, 275), (1035, 275)])
    s.arrow([(1020, 370), (1020, 470)], (1210, 420, T['nightly']))
    s.rect(690, 470, 660, 230, '#171C24', LINE, 20)
    s.text(1020, 502, T['remote'], 23, FG, True, 'middle')
    s.box(715, 530, 290, 140, T['copies'][0], T['copies'][1], True)
    s.box(1035, 530, 290, 140, T['standby'][0], T['standby'][1])
    s.box(50, 470, 250, 140, T['paper'][0], T['paper'][1])
    s.box(370, 470, 250, 140, T['emerg'][0], T['emerg'][1])
    s.text(50, 850, T['foot'], 20, MUTED)
    s.save(f'01-overview.{L}')


def layers(L, T):
    s = D(T['t2'], T['s2'], 900)
    ys = [170, 330, 490, 650]
    for y, (a, b, c) in zip(ys, T['layers']):
        s.box(50, y, 300, 130, a, [b], True)
        s.box(420, y, 450, 130, c[0], c[1:])
        s.arrow([(350, y + 65), (420, y + 65)])
    s.box(940, 170, 410, 280, T['sees'][0], T['sees'][1:])
    s.box(940, 490, 410, 290, T['never'][0], T['never'][1:], True)
    s.save(f'02-encryption.{L}')


def backup(L, T):
    s = D(T['t3'], T['s3'], 780)
    for i, (a, b) in enumerate(T['steps']):
        col, row = i % 4, i // 4
        s.box(50 + col * 335, 170 + row * 240, 290, 150, a, b, i in (2, 6))
        if col < 3:
            s.arrow([(340 + col * 335, 245 + row * 240), (385 + col * 335, 245 + row * 240)])
    s.arrow([(1200, 320), (1200, 360), (195, 360), (195, 410)])
    s.text(50, 700, T['foot3'], 21)
    s.save(f'03-backup.{L}')


def contingency(L, T):
    s = D(T['t4'], T['s4'], 960)
    for i, (a, b) in enumerate(T['steps']):
        col, row = i % 4, i // 4
        s.box(50 + col * 335, 170 + row * 240, 290, 150, a, b, i in (3, 6))
        if col < 3:
            s.arrow([(340 + col * 335, 245 + row * 240), (385 + col * 335, 245 + row * 240)])
        if col == 3 and row == 0:
            s.arrow([(1200, 320), (1200, 360), (195, 360), (195, 410)])
    s.box(50, 650, 1290, 130, T['after'][0], T['after'][1])
    s.arrow([(1200, 560), (1200, 650)])
    s.text(50, 850, T['foot4'], 21)
    s.save(f'04-contingency.{L}')


def keys(L, T):
    s = D(T['t5'], T['s5'], 900)
    s.text(50, 140, T['hdr'][0], 19, MUTED, True); s.text(390, 140, T['hdr'][1], 19, MUTED, True); s.text(850, 140, T['hdr'][2], 19, MUTED, True)
    for i, (a, b, c) in enumerate(T['rows']):
        y = 170 + i * 135
        s.box(50, y, 300, 115, a[0], a[1:], i == 2)
        s.rect(390, y, 420, 115); s.text(405, y + 30, b[0], 20, FG, True); s.text(405, y + 62, b[1], 18, MUTED); s.text(405, y + 90, b[2], 18, MUTED)
        s.rect(850, y, 500, 115); s.text(865, y + 30, c[0], 20, FG, True); s.text(865, y + 62, c[1], 18, MUTED); s.text(865, y + 90, c[2], 18, MUTED)
    s.save(f'05-keys.{L}')


def emergency(L, T):
    s = D(T['t6'], T['s6'], 760)
    for i, (a, b) in enumerate(T['steps']):
        col, row = i % 4, i // 4
        s.box(50 + col * 335, 170 + row * 240, 290, 150, a, b, i == 5)
        if col < 3 and i < len(T['steps']) - 1:
            s.arrow([(340 + col * 335, 245 + row * 240), (385 + col * 335, 245 + row * 240)])
    s.arrow([(1200, 320), (1200, 360), (195, 360), (195, 410)])
    s.text(50, 680, T['foot6'], 21)
    s.save(f'06-emergency.{L}')


def banner(L, T):
    s = D('', '', 420)
    s.d.rectangle((0, 0, 1400, 12), fill=ACCENT); s.svg.append(f'<rect width="1400" height="12" fill="{ACCENT}"/>')
    s.text(70, 135, 'Vaultwarden Self-Hosted', 58, FG, True)
    s.text(70, 205, '& External Recovery', 58, FG, True)
    s.text(70, 275, T['tag'], 25, MUTED)
    x = 70
    for i, (w, lab) in enumerate(zip([190, 190, 190, 190], T['tl'])):
        hot = i == 2
        s.rect(x, 330, w, 44, BG if hot else BOX, ACCENT if hot else LINE, 8, 2)
        s.text(x + w / 2, 352, lab, 17, ACCENT if hot else MUTED, hot, 'middle')
        x += w + 14
    s.save(f'banner.{L}')


EN = dict(
    t1='01 · Overview', s1='A self-hosted password vault, an encrypted copy off-site and a standby that is switched on only in a contingency',
    dev=('Your devices', ['phone, computers', 'official client apps']), vpn=('Private network', ['mesh VPN, not exposed', 'to the internet']),
    primary='Primary server (local)', vw=('Vaultwarden', ['container, loopback only', 'sign-ups closed']), data=('Encrypted vault', ['items encrypted on', 'the device first']),
    nightly='nightly, encrypted', remote='Remote VPS (off-site)', copies=('Encrypted archives', ['last 14 copies + checksums', 'cannot be opened here']), standby=('Standby server', ['same image, switched OFF', 'started on contingency']),
    paper=('Offline papers', ['recovery codes and', 'backup passphrase']), emerg=('Emergency contact', ['second account,', 'view-only, with a delay']),
    foot='Nothing is exposed to the internet; no single place holds both the archives and the passphrase.',
    t2='02 · Encryption layers', s2='Four independent protections; losing one does not expose the vault',
    layers=[('1 · Vault', 'master password', ['Client-side encryption', 'Argon2id key derivation']), ('2 · Login', 'second factor', ['Authenticator app + hardware', 'keys; recovery codes offline']),
            ('3 · Backup', 'separate passphrase', ['GnuPG symmetric, AES-256', 'verified by decrypting']), ('4 · Transport', 'restricted SSH key', ['SSH forced command', 'private network path'])],
    sees=('What each place can read', 'Primary server: ciphertext only', 'Remote VPS: an encrypted archive', 'Cloud copy (optional): same archive', 'Network: encrypted traffic'),
    never=('Never stored together', 'master password', 'backup passphrase', 'recovery codes', 'and the archives themselves'),
    t3='03 · Nightly backup', s3='Every step is checked; a bad backup never replaces a good one',
    steps=[('Snapshot', ['SQLite backup API', 'server keeps running']), ('Encrypt', ['GnuPG symmetric', 'AES-256']), ('Verify', ['decrypt it again', 'integrity check passes']), ('Checksum', ['SHA-256 file', 'next to the archive']),
           ('Rotate', ['keep the last 14', 'delete older ones']), ('Send', ['SSH, forced command', 'already encrypted']), ('Receive', ['label and file type', 'validated, not opened']), ('Report', ['summary in the daily', 'status message'])],
    foot3='The remote side never has the passphrase: it can store and rotate archives, not read them.',
    t4='04 · Contingency activation', s4='The primary is lost or unreachable: bring the vault back on the standby',
    steps4=None,
    after=('After the contingency', ['sign in with master password and second factor; decide: repair or rebuild the primary and restore there', 'then stop the standby and wipe the restored database; the encrypted archives stay']),
    foot4='A person types the passphrase on a real terminal; nothing is ever saved or sent by chat.',
    t5='05 · Keys needed to recover', s5='What each secret is for and what happens without it (categories only, no locations)',
    hdr=('Secret', 'Needed for', 'If it is lost'),
    rows=[(('Master password', 'memorised'), ('Unlock the vault', 'every device, every day', 'no recovery by design'), ('No way back into the vault', 'the server cannot reset it', 'protect the emergency access')),
          (('Second-factor', 'recovery codes'), ('Sign in if a device is lost', 'printed, kept offline', 'separate from the devices'), ('Locked out of the account', 'use another key or the', 'emergency contact')),
          (('Backup passphrase', '≠ master password'), ('Open the encrypted archives', 'only at restore time', 'typed, never stored online'), ('Archives become unreadable', 'keep an offline copy', 'in a different place')),
          (('Receiver SSH key', 'on the primary'), ('Send archives off-site', 'cannot run anything else', 'one forced command'), ('Replace the key', 'nothing else is lost', 'the vault is untouched'))],
    t6='06 · Emergency access (view-only)', s6='A trusted second account can request access; nothing opens without a waiting period',
    steps6=None,
    foot6='The waiting time and the notifications give the owner a chance to say no. View-only avoids taking over the account.',
    tag='Self-hosted vault, encrypted off-site copy and a tested contingency, with no exposure.', tl=['primary', 'encrypted copy', 'standby', 'emergency'],
)
EN['steps4'] = [('Detect', ['primary lost or', 'unreachable']), ('Connect', ['to the remote host', 'on a real terminal']), ('List and choose', ['latest archive by', 'default']), ('Verify checksum', ['damaged or altered', 'files are refused']),
                ('Type passphrase', ['not shown, not saved']), ('Integrity check', ['users and items', 'counted before replacing']), ('Confirm', ['type YES; previous data', 'kept (last 3)']), ('Start standby', ['same image,', 'private network'])]
EN['steps6'] = [('Invite', ['owner invites a', 'trusted second account']), ('Accept', ['the contact accepts', 'and creates the account']), ('Confirm', ['owner verifies the', 'fingerprint']), ('Request', ['in an emergency the', 'contact asks for access']),
                ('Wait', ['e.g. 7 days; owner is', 'notified and can reject']), ('View-only', ['access granted', 'without taking over'])]
ES = dict(
    t1='01 · Vista general', s1='Una bóveda de contraseñas propia, una copia cifrada fuera de sitio y un respaldo que se enciende sólo en una contingencia',
    dev=('Tus dispositivos', ['celular, computadoras', 'apps oficiales']), vpn=('Red privada', ['VPN en malla, sin', 'exposición a internet']),
    primary='Servidor principal (local)', vw=('Vaultwarden', ['contenedor, sólo loopback', 'registro cerrado']), data=('Bóveda cifrada', ['los datos se cifran', 'primero en el dispositivo']),
    nightly='cada noche, cifrada', remote='VPS remoto (fuera de sitio)', copies=('Archivos cifrados', ['últimas 14 copias + hash', 'no se pueden abrir acá']), standby=('Servidor de respaldo', ['misma imagen, APAGADO', 'se inicia en contingencia']),
    paper=('Papeles offline', ['códigos de rescate y', 'frase del backup']), emerg=('Contacto emergencia', ['segunda cuenta,', 'sólo lectura, con demora']),
    foot='Nada queda expuesto a internet; ningún lugar guarda a la vez los archivos y la frase.',
    t2='02 · Capas de cifrado', s2='Cuatro protecciones independientes; perder una no expone la bóveda',
    layers=[('1 · Bóveda', 'contraseña maestra', ['Cifrado en el cliente', 'derivación Argon2id']), ('2 · Ingreso', 'segundo factor', ['App autenticadora + llaves', 'físicas; códigos offline']),
            ('3 · Backup', 'frase propia', ['GnuPG simétrico, AES-256', 'verificado al descifrar']), ('4 · Transporte', 'clave SSH restringida', ['SSH, comando forzado', 'por la red privada'])],
    sees=('Qué puede leer cada lugar', 'Servidor principal: sólo cifrado', 'VPS remoto: un archivo cifrado', 'Copia en nube (opcional): igual', 'Red: tráfico cifrado'),
    never=('Nunca guardados juntos', 'contraseña maestra', 'frase del backup', 'códigos de recuperación', 'ni los archivos cifrados'),
    t3='03 · Backup nocturno', s3='Cada paso se controla; un backup malo nunca reemplaza a uno bueno',
    steps=[('Foto', ['API de backup de SQLite', 'el servidor sigue andando']), ('Cifrar', ['GnuPG simétrico', 'AES-256']), ('Verificar', ['se descifra de nuevo', 'pasa el chequeo de la base']), ('Hash', ['archivo SHA-256', 'junto al backup']),
           ('Rotar', ['conserva los últimos 14', 'borra los más viejos']), ('Enviar', ['SSH, comando forzado', 'ya cifrado']), ('Recibir', ['valida nombre y tipo', 'sin abrirlo']), ('Informar', ['resumen en el estado', 'diario'])],
    foot3='El lado remoto nunca tiene la frase: puede guardar y rotar archivos, no leerlos.',
    t4='04 · Activación de la contingencia', s4='El principal se perdió o no responde: se recupera la bóveda en el respaldo',
    after=('Después de la contingencia', ['ingresar con contraseña maestra y segundo factor; decidir: reparar o reconstruir el principal y restaurar allí', 'luego apagar el respaldo y borrar la base restaurada; los archivos cifrados quedan']),
    foot4='Una persona tipea la frase en una terminal real; nunca se guarda ni se envía por chat.',
    t5='05 · Claves necesarias para recuperar', s5='Para qué sirve cada secreto y qué pasa sin él (sólo categorías, sin ubicaciones)',
    hdr=('Secreto', 'Sirve para', 'Si se pierde'),
    rows=[(('Contraseña maestra', 'memorizada'), ('Abrir la bóveda', 'todos los dispositivos', 'sin recuperación, a propósito'), ('No hay vuelta atrás', 'el servidor no la restablece', 'proteger el acceso de emergencia')),
          (('Códigos de rescate', 'del segundo factor'), ('Ingresar si se pierde un', 'dispositivo; impresos y', 'guardados offline, aparte'), ('Cuenta bloqueada', 'usar otra llave o el', 'contacto de emergencia')),
          (('Frase del backup', '≠ contraseña maestra'), ('Abrir los archivos cifrados', 'sólo al restaurar', 'se tipea, nunca online'), ('Archivos ilegibles', 'guardar una copia offline', 'en otro lugar')),
          (('Clave SSH del envío', 'en el principal'), ('Enviar archivos afuera', 'no puede ejecutar nada', 'más: un comando forzado'), ('Se reemplaza la clave', 'no se pierde nada más', 'la bóveda queda intacta'))],
    t6='06 · Acceso de emergencia (sólo lectura)', s6='Una segunda cuenta de confianza puede pedir acceso; nada se abre sin un tiempo de espera',
    foot6='La espera y los avisos le dan al dueño la chance de decir que no. Sólo lectura evita tomar la cuenta.',
    tag='Bóveda propia, copia cifrada fuera de sitio y una contingencia probada, sin exposición.', tl=['principal', 'copia cifrada', 'respaldo', 'emergencia'],
)
ES['steps4'] = [('Detectar', ['el principal se perdió', 'o no responde']), ('Conectar', ['al host remoto, en una', 'terminal real']), ('Listar y elegir', ['el archivo más nuevo', 'por defecto']), ('Verificar hash', ['archivos dañados o', 'alterados se rechazan']),
                ('Tipear la frase', ['no se muestra ni', 'se guarda']), ('Chequeo de la base', ['se cuentan usuarios y', 'elementos antes de pisar']), ('Confirmar', ['escribir SI; lo anterior', 'se conserva (últimas 3)']), ('Iniciar respaldo', ['misma imagen,', 'red privada'])]
ES['steps6'] = [('Invitar', ['el dueño invita a una', 'segunda cuenta de confianza']), ('Aceptar', ['el contacto acepta y', 'crea su cuenta']), ('Confirmar', ['el dueño verifica la', 'huella']), ('Solicitar', ['en una emergencia el', 'contacto pide acceso']),
                ('Esperar', ['p. ej. 7 días; se avisa', 'al dueño y puede rechazar']), ('Sólo lectura', ['acceso concedido', 'sin tomar la cuenta'])]

if __name__ == '__main__':
    for L, T in (('en', EN), ('es', ES)):
        T['steps'] if False else None
        overview(L, T); layers(L, T); backup(L, T); banner(L, T); emergency(L, {**T, 'steps': T['steps6']}); keys(L, T)
        contingency(L, {**T, 'steps': T['steps4']})
    print('OK', len(list(OUT.glob('*.png'))), 'PNG')
