import base64
import binascii
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Tuple
from zipfile import BadZipFile, ZipFile

from cryptography.hazmat.primitives.serialization import pkcs7


@dataclass
class P7MAttachment:
    nome: str
    formato: str
    dimensione: int
    contenuto: bytes
    compression: Optional[str] = None


class P7MHandler:
    def __init__(self, openssl_path: Optional[str] = None):
        self.openssl_path = openssl_path or shutil.which("openssl") or "openssl"

    def extract_invoice_payload(self, p7m_content):
        """
        Restituisce il contenuto XML e la lista degli allegati presenti nella fattura P7M.
        Utilizza Cryptography per validare la busta e OpenSSL per estrarre il payload.
        """
        normalized_content = self._normalize_p7m_bytes(p7m_content)
        # Validazione e recupero certificati tramite cryptography
        self._ensure_pkcs7_is_valid(normalized_content)
        # Estrazione del payload XML via OpenSSL
        xml_bytes = self._extract_with_openssl(normalized_content)
        xml_text = self._decode_xml(xml_bytes)
        attachments = self.extract_attachments_from_xml(xml_text)
        return xml_text, attachments

    def extract_xml_from_p7m(self, p7m_content):
        """
        Mantiene la compatibilità con il vecchio comportamento restituendo solo l'XML.
        """
        xml_text, _ = self.extract_invoice_payload(p7m_content)
        return xml_text

    def extract_attachments_from_xml(self, xml_content):
        """
        Estrae gli Allegati dichiarati all'interno del documento XML,
        restituendo una lista di P7MAttachment.
        """
        if isinstance(xml_content, bytes):
            xml_content = self._decode_xml(xml_content)

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return []

        attachments: List[P7MAttachment] = []
        for allegati in root.iter():
            if not allegati.tag.endswith("Allegati"):
                continue

            nome = self._find_child_text(allegati, "NomeAttachment") or "allegato.bin"
            formato = self._find_child_text(allegati, "FormatoAttachment") or "application/octet-stream"
            algoritmo = self._find_child_text(allegati, "AlgoritmoCompressione")
            raw = self._find_child_text(allegati, "Attachment") or ""
            content_bytes = self._safe_b64decode(raw)
            content_bytes, nome = self._process_attachment_payload(content_bytes, algoritmo, nome)

            attachments.append(
                P7MAttachment(
                    nome=nome,
                    formato=formato,
                    dimensione=len(content_bytes),
                    contenuto=content_bytes,
                    compression=algoritmo or None,
                )
            )

        return attachments

    def get_signer_info(self, p7m_content):
        """
        Estrae le informazioni principali dei firmatari utilizzando i certificati contenuti nel PKCS#7.
        """
        normalized_content = self._normalize_p7m_bytes(p7m_content)
        certificates = self._ensure_pkcs7_is_valid(normalized_content)
        signing_times = self._extract_signing_times(normalized_content)

        signer_infos = []
        for cert in certificates:
            serial = cert.serial_number
            signer_infos.append(
                {
                    "nome": cert.subject.rfc4514_string(),
                    "data_firma": signing_times.get(serial),
                    "certificato_da": cert.issuer.rfc4514_string(),
                }
            )

        return signer_infos

    # --- Utility private ---

    def _normalize_p7m_bytes(self, p7m_content):
        """
        Converte il contenuto P7M in bytes DER, gestendo input binari, base64 o PEM.
        """
        if isinstance(p7m_content, (bytes, bytearray)):
            raw = bytes(p7m_content)
            if raw.startswith(b"-----BEGIN"):
                return self._decode_pem_block(raw.decode("ascii", errors="ignore"))
            if self._looks_like_base64(raw):
                decoded = base64.b64decode(raw, validate=False)
                if decoded and decoded[0] == 0x30:
                    return decoded
            return raw

        if isinstance(p7m_content, str):
            data = p7m_content.strip()
            if data.startswith("-----BEGIN"):
                return self._decode_pem_block(data)
            try:
                decoded = base64.b64decode(data.encode("ascii"), validate=True)
                if decoded and decoded[0] == 0x30:
                    return decoded
                return base64.b64decode(data.encode("ascii"), validate=False)
            except binascii.Error as e:
                raise ValueError(f"Contenuto P7M non valido o non riconosciuto: {str(e)}")

        raise TypeError("Il contenuto P7M deve essere bytes o stringa (Base64/PEM)")

    def _looks_like_base64(self, blob: bytes):
        sample = blob.strip()
        if not sample:
            return False
        allowed = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n\r"
        return all(ch in allowed for ch in sample[:256])

    def _decode_pem_block(self, pem_text):
        header = "-----BEGIN PKCS7-----"
        footer = "-----END PKCS7-----"
        if header not in pem_text or footer not in pem_text:
            raise ValueError("Blocco PEM PKCS7 non valido")
        base64_body = pem_text.replace(header, "").replace(footer, "").strip()
        return base64.b64decode(base64_body.encode("ascii"), validate=True)

    def _ensure_pkcs7_is_valid(self, normalized_content):
        """
        Usa cryptography per verificare che il PKCS#7 sia leggibile e restituisce i certificati presenti.
        """
        try:
            return pkcs7.load_der_pkcs7_certificates(normalized_content)
        except ValueError as exc:
            raise ValueError("Il contenuto P7M non è una busta PKCS#7 valida") from exc

    def _resolve_openssl(self):
        if os.path.isfile(self.openssl_path) and os.access(self.openssl_path, os.X_OK):
            return self.openssl_path

        resolved = shutil.which(self.openssl_path)
        if not resolved:
            raise FileNotFoundError("Comando 'openssl' non trovato sul sistema")
        self.openssl_path = resolved
        return resolved

    def _extract_with_openssl(self, normalized_content):
        openssl_bin = self._resolve_openssl()
        input_path = self._write_temp_file(normalized_content)
        output_fd, output_path = tempfile.mkstemp()
        os.close(output_fd)

        try:
            cmd = [
                openssl_bin,
                "smime",
                "-inform",
                "DER",
                "-verify",
                "-noverify",
                "-in",
                input_path,
                "-out",
                output_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(
                    f"OpenSSL ha restituito un errore: {result.stderr.strip() or result.stdout.strip()}"
                )

            with open(output_path, "rb") as extracted:
                data = extracted.read()

            if not data:
                raise ValueError("OpenSSL non ha prodotto alcun contenuto dalla busta P7M")

            return data
        finally:
            self._safe_remove(input_path)
            self._safe_remove(output_path)

    def _extract_signing_times(self, normalized_content):
        """
        Usa 'openssl cms -cmsout -print' per recuperare i signingTime dei firmatari.
        Restituisce un dict {seriale_certificato: signing_time_iso}.
        """
        openssl_bin = self._resolve_openssl()
        input_path = self._write_temp_file(normalized_content)
        try:
            cmd = [
                openssl_bin,
                "cms",
                "-cmsout",
                "-print",
                "-inform",
                "DER",
                "-in",
                input_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return {}

            signing_times = {}
            current_serial = None
            for line in result.stdout.splitlines():
                stripped = line.strip()
                if stripped.startswith("serialNumber:"):
                    serial_text = stripped.split("serialNumber:", 1)[1].strip()
                    try:
                        current_serial = int(serial_text, 16)
                    except ValueError:
                        try:
                            current_serial = int(serial_text)
                        except ValueError:
                            current_serial = None
                elif "signingTime" in stripped and "data:" in stripped and current_serial is not None:
                    timestamp = stripped.split("data:", 1)[1].strip()
                    signing_times[current_serial] = self._format_signing_time(timestamp)

            return signing_times
        finally:
            self._safe_remove(input_path)

    def _format_signing_time(self, timestamp):
        # timestamp esempio: 20240101010203Z
        if len(timestamp) == 15 and timestamp.endswith("Z"):
            return (
                f"{timestamp[6:8]}/{timestamp[4:6]}/{timestamp[0:4]} "
                f"{timestamp[8:10]}:{timestamp[10:12]}:{timestamp[12:14]} UTC"
            )
        return timestamp

    def _decode_xml(self, xml_bytes):
        try:
            return xml_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return xml_bytes.decode("latin-1", errors="ignore")

    def _find_child_text(self, element, suffix):
        for child in element:
            if child.tag.endswith(suffix):
                return (child.text or "").strip()
        return ""

    def _safe_b64decode(self, data):
        data = data.strip()
        if not data:
            return b""
        try:
            return base64.b64decode(data.encode("ascii"), validate=False)
        except binascii.Error:
            return b""

    def _process_attachment_payload(self, content_bytes: bytes, algoritmo: str, fallback_name: str) -> Tuple[bytes, str]:
        if not algoritmo:
            return content_bytes, fallback_name

        algo = algoritmo.strip().upper()
        if algo == "ZIP":
            try:
                with ZipFile(BytesIO(content_bytes)) as zipped:
                    members = [name for name in zipped.namelist() if not name.endswith("/")]
                    if not members:
                        return content_bytes, fallback_name
                    first_member = members[0]
                    extracted = zipped.read(first_member)
                    return extracted, Path(first_member).name or fallback_name
            except (BadZipFile, KeyError):
                return content_bytes, fallback_name

        return content_bytes, fallback_name

    def _write_temp_file(self, data: bytes):
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(data)
        return path

    def _safe_remove(self, path):
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except OSError:
            pass