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
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>FATTURA ELETTRONICA</h1>
                    <div class="tipo-doc">
                        Numero: {numero} del {data}<br>
                        Tipo documento: {tipo_documento}
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
                                <th>Quantità</th>
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
                            <div class="info-value">{modalita_pagamento}</div>
                        </div>
                        <div class="info-group">
                            <div class="info-label">Termini:</div>
                            <div class="info-value">{termini_pagamento}</div>
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
        dati_beni_servizi = ""
        for item in invoice_data['items']:
            dati_beni_servizi += f"""
                <tr>
                    <td>{item['descrizione']}</td>
                    <td>{item['quantita']}</td>
                    <td>€ {item['prezzo_unitario']:.2f}</td>
                    <td>€ {item['importo']:.2f}</td>
                    <td>{item['aliquota_iva']}%</td>
                </tr>
            """

        # Genera il riepilogo IVA
        riepilogo_iva = ""
        for aliquota in invoice_data['totals']['riepilogo_aliquote']:
            riepilogo_iva += f"""
                <tr>
                    <td>{aliquota['aliquota']}%</td>
                    <td>€ {aliquota['imponibile']:.2f}</td>
                    <td>€ {aliquota['imposta']:.2f}</td>
                    <td>{aliquota['esigibilita']}</td>
                    <td>{aliquota['riferimenti']}</td>
                </tr>
            """

        return self.html_template.format(
            numero=invoice_data['header']['numero'],
            data=invoice_data['header']['data'],
            tipo_documento=invoice_data['header']['tipo_documento'],
            denominazione_cedente=invoice_data['supplier']['denominazione'],
            id_fiscale_iva_cedente=invoice_data['supplier']['id_fiscale_iva'],
            regime_fiscale_cedente=invoice_data['supplier']['regime_fiscale'],
            partita_iva_cedente=invoice_data['supplier']['partita_iva'],
            indirizzo_cedente=invoice_data['supplier']['indirizzo'],
            cap_cedente=invoice_data['supplier']['cap'],
            citta_cedente=invoice_data['supplier']['citta'],
            provincia_cedente=invoice_data['supplier']['provincia'],
            denominazione_committente=invoice_data['customer']['denominazione'],
            partita_iva_committente=invoice_data['customer']['partita_iva'],
            indirizzo_committente=invoice_data['customer']['indirizzo'],
            cap_committente=invoice_data['customer']['cap'],
            citta_committente=invoice_data['customer']['citta'],
            provincia_committente=invoice_data['customer']['provincia'],
            codice_fiscale_committente=invoice_data['customer']['codice_fiscale'],
            pec_committente=invoice_data['customer']['pec'],
            codice_destinatario_committente=invoice_data['customer']['codice_destinatario'],
            causale=invoice_data['customer']['causale'],
            dati_beni_servizi=dati_beni_servizi,
            imponibile=invoice_data['totals']['imponibile'],
            imposta=invoice_data['totals']['imposta'],
            totale=invoice_data['totals']['imponibile'] + invoice_data['totals']['imposta'],
            modalita_pagamento=invoice_data['payment']['modalita'],
            termini_pagamento=invoice_data['payment']['termini'],
            iban_pagamento=invoice_data['payment']['iban'],
            scadenza_pagamento=invoice_data['payment']['scadenza'],
            riepilogo_iva=riepilogo_iva,
            spese_accessorie=invoice_data['totals']['spese_accessorie'],
            arrotondamento=invoice_data['totals']['arrotondamento']
        ) 