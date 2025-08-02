class PDFLayout:
    def __init__(self):
        self.html_template = """
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;
                    margin: 20px;
                    color: #333;
                    line-height: 1.4;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background: #fff;
                }}
                .header {{
                    border-bottom: 2px solid #ccc;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    color: #333;
                    font-size: 24px;
                    margin: 0;
                    padding: 0;
                }}
                .header .tipo-doc {{
                    color: #666;
                    font-size: 14px;
                    margin-top: 5px;
                }}
                .header .version {{
                    color: #999;
                    font-size: 12px;
                    margin-top: 5px;
                    font-style: italic;
                }}
                .section {{
                    margin: 15px 0;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 5px;
                }}
                .section h2 {{
                    color: #333;
                    font-size: 16px;
                    margin: 0 0 10px 0;
                    padding-bottom: 5px;
                    border-bottom: 1px solid #ddd;
                }}
                .grid-container {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                }}
                .info-group {{
                    margin-bottom: 10px;
                }}
                .info-label {{
                    font-weight: bold;
                    color: #666;
                    font-size: 13px;
                }}
                .info-value {{
                    margin-top: 2px;
                    font-size: 14px;
                }}
                .info-code {{
                    color: #007bff;
                    font-weight: bold;
                    font-size: 12px;
                }}
                .payment-info {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                }}
                th {{
                    background: #f0f0f0;
                    padding: 8px;
                    text-align: left;
                    font-size: 14px;
                    border-bottom: 2px solid #ddd;
                }}
                td {{
                    padding: 8px;
                    border-bottom: 1px solid #ddd;
                    font-size: 14px;
                }}
                .totali {{
                    margin-top: 20px;
                    text-align: right;
                }}
                .totali-row {{
                    display: flex;
                    justify-content: flex-end;
                    margin: 5px 0;
                }}
                .totali-label {{
                    font-weight: bold;
                    margin-right: 20px;
                    min-width: 150px;
                    text-align: right;
                }}
                .totali-value {{
                    min-width: 100px;
                    text-align: right;
                }}
                .totale-documento {{
                    font-size: 16px;
                    font-weight: bold;
                    color: #007bff;
                    border-top: 2px solid #007bff;
                    padding-top: 10px;
                    margin-top: 10px;
                }}
                .nazione {{
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>FATTURA ELETTRONICA</h1>
                    <div class="tipo-doc">
                        Numero: {numero} del {data}<br>
                        Tipo documento: {tipo_documento} - {tipo_documento_desc}
                    </div>
                    <div class="version">
                        Versione specifiche tecniche: {version}
                    </div>
                </div>

                <div class="grid-container">
                    <div class="section">
                        <h2>CEDENTE/PRESTATORE</h2>
                        <div class="info-group">
                            <div class="info-label">Denominazione:</div>
                            <div class="info-value">{denominazione_cedente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Identificativo fiscale ai fini IVA:</div>
                            <div class="info-value">{id_fiscale_iva_cedente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Partita IVA:</div>
                            <div class="info-value">{partita_iva_cedente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Regime Fiscale:</div>
                            <div class="info-value">{regime_fiscale_cedente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Indirizzo:</div>
                            <div class="info-value">
                                {indirizzo_cedente}<br>
                                {cap_cedente} {citta_cedente} ({provincia_cedente})
                                <span class="nazione">{nazione_cedente}</span>
                            </div>
                        </div>
                    </div>

                    <div class="section">
                        <h2>CESSIONARIO/COMMITTENTE</h2>
                        <div class="info-group">
                            <div class="info-label">Denominazione:</div>
                            <div class="info-value">{denominazione_committente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Partita IVA:</div>
                            <div class="info-value">{partita_iva_committente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Codice Fiscale:</div>
                            <div class="info-value">{codice_fiscale_committente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">PEC:</div>
                            <div class="info-value">{pec_committente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Codice Destinatario:</div>
                            <div class="info-value">{codice_destinatario_committente}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Indirizzo:</div>
                            <div class="info-value">
                                {indirizzo_committente}<br>
                                {cap_committente} {citta_committente} ({provincia_committente})
                                <span class="nazione">{nazione_committente}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>DATI BENI/SERVIZI</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Descrizione</th>
                                <th>Codice Articolo</th>
                                <th>Quantità</th>
                                <th>Unità di Misura</th>
                                <th>Prezzo Unitario</th>
                                <th>Importo</th>
                                <th>IVA %</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dati_beni_servizi}
                        </tbody>
                    </table>
                </div>

                <div class="section">
                    <h2>RIEPILOGO IVA E TOTALI</h2>
                    <table class="riepilogo-table">
                        <thead>
                            <tr>
                                <th>IVA %</th>
                                <th>Imponibile</th>
                                <th>Imposta</th>
                                <th>Esigibilità IVA</th>
                                <th>Riferimenti Normativi</th>
                            </tr>
                        </thead>
                        <tbody>
                            {riepilogo_iva}
                        </tbody>
                    </table>
                    
                    <div class="totali">
                        <div class="totali-row">
                            <div class="totali-label">Totale Imponibile:</div>
                            <div class="totali-value">€ {imponibile:.2f}</div>
                        </div>
                        <div class="totali-row">
                            <div class="totali-label">Totale Imposta:</div>
                            <div class="totali-value">€ {imposta:.2f}</div>
                        </div>
                        <div class="totali-row">
                            <div class="totali-label">Spese Accessorie:</div>
                            <div class="totali-value">€ {spese_accessorie:.2f}</div>
                        </div>
                        <div class="totali-row">
                            <div class="totali-label">Arrotondamento:</div>
                            <div class="totali-value">€ {arrotondamento:.2f}</div>
                        </div>
                        <div class="totali-row totale-documento">
                            <div class="totali-label">Totale Documento:</div>
                            <div class="totali-value">€ {totale:.2f}</div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>MODALITÀ DI PAGAMENTO</h2>
                    <div class="payment-info">
                        <div class="info-group">
                            <div class="info-label">Modalità:</div>
                            <div class="info-value">
                                <span class="info-code">{modalita_pagamento}</span><br>
                                {modalita_pagamento_desc}
                            </div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Termini:</div>
                            <div class="info-value">
                                <span class="info-code">{termini_pagamento}</span><br>
                                {termini_pagamento_desc}
                            </div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">IBAN:</div>
                            <div class="info-value">{iban_pagamento}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Scadenza:</div>
                            <div class="info-value">{scadenza_pagamento}</div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>CAUSALE</h2>
                    <div class="info-value">{causale}</div>
                </div>
            </div>
        </body>
        </html>
        """

    def generate_invoice_html(self, invoice_data):
        # Estrae i dati dalla struttura della fattura
        header = invoice_data.get('header', {})
        supplier = invoice_data.get('supplier', {})
        customer = invoice_data.get('customer', {})
        items = invoice_data.get('items', [])
        totals = invoice_data.get('totals', {})
        payment = invoice_data.get('payment', {})
        version = invoice_data.get('version', 'N/D')
        
        # Genera le righe della tabella beni/servizi
        dati_beni_servizi = ""
        for item in items:
            dati_beni_servizi += f"""
                <tr>
                    <td>{item.get('descrizione', 'N/D')}</td>
                    <td>{item.get('codice_articolo', 'N/D')}</td>
                    <td>{item.get('quantita', 0):.2f}</td>
                    <td>{item.get('unita_misura', 'N/D')}</td>
                    <td>€ {item.get('prezzo_unitario', 0):.2f}</td>
                    <td>€ {item.get('importo', 0):.2f}</td>
                    <td>{item.get('aliquota_iva', 0):.0f}%</td>
                </tr>
            """
        
        # Genera il riepilogo IVA
        riepilogo_iva = ""
        for riepilogo in totals.get('riepilogo_aliquote', []):
            riepilogo_iva += f"""
                <tr>
                    <td>{riepilogo.get('aliquota', 0):.0f}%</td>
                    <td>€ {riepilogo.get('imponibile', 0):.2f}</td>
                    <td>€ {riepilogo.get('imposta', 0):.2f}</td>
                    <td>{riepilogo.get('esigibilita', 'N/D')}</td>
                    <td>{riepilogo.get('riferimenti', 'N/D')}</td>
                </tr>
            """
        
        # Calcola il totale
        totale = (totals.get('imponibile', 0) + 
                 totals.get('imposta', 0) + 
                 totals.get('spese_accessorie', 0) + 
                 totals.get('arrotondamento', 0))
        
        # Sostituisce i valori nel template
        html_content = self.html_template.format(
            # Header
            numero=header.get('numero', 'N/D'),
            data=header.get('data', 'N/D'),
            tipo_documento=header.get('tipo_documento', 'N/D'),
            tipo_documento_desc=header.get('tipo_documento_desc', 'N/D'),
            version=version,
            
            # Cedente/Prestatore
            denominazione_cedente=supplier.get('denominazione', 'N/D'),
            id_fiscale_iva_cedente=supplier.get('id_fiscale_iva', 'N/D'),
            partita_iva_cedente=supplier.get('partita_iva', 'N/D'),
            regime_fiscale_cedente=supplier.get('regime_fiscale', 'N/D'),
            indirizzo_cedente=supplier.get('indirizzo', 'N/D'),
            cap_cedente=supplier.get('cap', 'N/D'),
            citta_cedente=supplier.get('citta', 'N/D'),
            provincia_cedente=supplier.get('provincia', 'N/D'),
            nazione_cedente=supplier.get('nazione', 'IT'),
            
            # Cessionario/Committente
            denominazione_committente=customer.get('denominazione', 'N/D'),
            partita_iva_committente=customer.get('partita_iva', 'N/D'),
            codice_fiscale_committente=customer.get('codice_fiscale', 'N/D'),
            pec_committente=customer.get('pec', 'N/D'),
            codice_destinatario_committente=customer.get('codice_destinatario', 'N/D'),
            indirizzo_committente=customer.get('indirizzo', 'N/D'),
            cap_committente=customer.get('cap', 'N/D'),
            citta_committente=customer.get('citta', 'N/D'),
            provincia_committente=customer.get('provincia', 'N/D'),
            nazione_committente=customer.get('nazione', 'IT'),
            
            # Dati beni/servizi
            dati_beni_servizi=dati_beni_servizi,
            
            # Riepilogo IVA
            riepilogo_iva=riepilogo_iva,
            
            # Totali
            imponibile=totals.get('imponibile', 0),
            imposta=totals.get('imposta', 0),
            spese_accessorie=totals.get('spese_accessorie', 0),
            arrotondamento=totals.get('arrotondamento', 0),
            totale=totale,
            
            # Pagamento
            modalita_pagamento=payment.get('modalita', 'N/D'),
            modalita_pagamento_desc=payment.get('modalita_desc', 'N/D'),
            termini_pagamento=payment.get('termini', 'N/D'),
            termini_pagamento_desc=payment.get('termini_desc', 'N/D'),
            iban_pagamento=payment.get('iban', 'N/D'),
            scadenza_pagamento=payment.get('scadenza', 'N/D'),
            
            # Causale
            causale=customer.get('causale', 'N/D')
        )
        
        return html_content 