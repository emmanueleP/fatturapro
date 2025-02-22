from asn1crypto import cms
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_der_x509_certificate
import base64

class P7MHandler:
    def __init__(self):
        pass
        
    def extract_xml_from_p7m(self, p7m_content):
        """
        Estrae il contenuto XML da un file P7M
        """
        try:
            # Decodifica il contenuto P7M
            content_info = cms.ContentInfo.load(p7m_content)
            
            if content_info['content_type'].native != 'signed_data':
                raise ValueError("Il file non è una busta crittografica valida")
            
            # Ottiene il contenuto firmato
            signed_data = content_info['content']
            
            # Estrae il contenuto originale (XML)
            enc_content = signed_data['encap_content_info']['content']
            if enc_content is None:
                raise ValueError("Contenuto non trovato nella busta P7M")
                
            return enc_content.native
            
        except Exception as e:
            raise Exception(f"Errore nell'estrazione del contenuto XML: {str(e)}")
    
    def get_signer_info(self, p7m_content):
        """
        Estrae le informazioni sul firmatario
        """
        try:
            content_info = cms.ContentInfo.load(p7m_content)
            signed_data = content_info['content']
            
            signer_infos = []
            for signer in signed_data['signer_infos']:
                cert = None
                for signed_cert in signed_data['certificates']:
                    if signed_cert.chosen['tbs_certificate']['subject'] == signer['sid'].chosen['issuer']:
                        cert = signed_cert.chosen
                        break
                
                if cert:
                    signer_infos.append({
                        'nome': cert['tbs_certificate']['subject'].native,
                        'data_firma': signer['signed_time'].native if 'signed_time' in signer else None,
                        'certificato_da': cert['tbs_certificate']['issuer'].native
                    })
            
            return signer_infos
            
        except Exception as e:
            raise Exception(f"Errore nell'estrazione delle informazioni sul firmatario: {str(e)}") 