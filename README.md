## ERPNext Fattura Elettronica ver. 0.0.1

App to export electronic invoices as mandated by the Italian Government

#### License

GPLv3

Reference (document issued by Italian Government):
https://www.agenziaentrate.gov.it/wps/wcm/connect/a8316033-6124-4667-99d8-ed143dc72c20/Provvedimento_30042018+.pdf?MOD=AJPERES&CACHEID=a8316033-6124-4667-99d8-ed143dc72c20

http://www.fatturapa.gov.it/export/fatturazione/sdi/Specifiche_tecniche_del_formato_FatturaPA_v1.2.1.pdf

## Requirements

At scheduled time the system can generate email alerts about the documents that must be exported. The user can manage the schelude choose between (1 hour, 2 hour, or a fixed time of the day).

The user will manage the export process using a new doctype: "EFE XML Export"
In this doctype the user will be able to select a period and after then can select the Documents to export
The system will generate an XML file for every Customer;

The XML file will be complaint to:
http://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-2.htm
and will be tested here:
http://sdi.fatturapa.gov.it/SdI2FatturaPAWeb/AccediAlServizioAction.do?pagina=controlla_fattura

These files can be used to send electronic invoices to SDI using a service like this:
https://guide.pec.it/fatturazione-elettronica/menu-carica-fattura/upload-fatture-in-formato-xml.aspx

This software is a Frappe Custom App but will be part of the Italian Localization

## Setup

- bench get-app https://github.com/mascor/erpnext_fattura_elettronica.git
- bench --site SITENAME install-app erpnext_fattura_elettronica

## ERPNext Customization

Doctype updates:
- Company
- Customer Group
- Customer
- Sales Invoice

New Doctypes:
- EFE XML Export
- Regime Fiscale
- Tipo Documento
- Natura
- Transporter

## Plan

- Complete development before the second week of November (2018)
- Complete test before the last week of November (2018)

## Implementation

Reference: 
- http://www.fatturapa.gov.it/export/fatturazione/sdi/Specifiche_tecniche_del_formato_FatturaPA_v1.2.1.pdf
- http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/Rappresentazione_tabellare_del_tracciato_FatturaPA_versione_1.2.1.pdf

###### Company fields

- Ragione Sociale
  - Mandatory: ERPNEXT.Company.company_name
  - 1.2.1.3.1 Denominazione
- Partita IVA
  - Mandatory: ERPNEXT.Company.tax_id
  - 1.1.1.2 IdCodice, 1.2.1.1.2 IdCodice
- Codice Fiscale
  - Mandatory: ERPNEXT_EFE.Company.codice_fiscale (Data)
  - 1.2.1.2 CodiceFiscale
- Titolo
  - NOT Mandatory: ERPNEXT_EFE.Company.titolo (Select)
  - (Avvocato, Dottore, ecc.);
  - 1.2.1.3.4 Titolo
- Nome
  - Mandatory if ERPNEXT_EFE.tipo_soggetto == "Persona fisica": ERPNEXT_EFE.Company.nome (Data)
  - 1.2.1.3.2 Nome
- Cognome
  - Mandatory if ERPNEXT_EFE.tipo_soggetto == "Persona fisica": ERPNEXT_EFE.Company.cognome (Data)
  - 1.2.1.3.3 Cognome
- Regime Fiscale
  - Mandatory: ERPNEXT_EFE.Company.RegimeFiscale (Select)
  - 1.2.1.8 RegimeFiscale
- Causale
  - Mandatory: ERPNEXT_EFE.Company.Causale (Select)
  - 2.1.1.11 Causale
- Progressivo invio
  - Mandatory: ERPNEXT_EFE.Company.ProgressivoInvio (Int)
  - 1.1.2 <ProgressivoInvio
- Telefono
  - Mandatory: ERPNEXT.Company.phone_no
  - 1.1.5.1 Telefono, 1.2.5.1 Telefono
- Email
  - Mandatory: ERPNEXT.Company.email
  - 1.1.5.2 Email, 1.2.5.3 Email
- Indirizzo
  - Mandatory: ERPNEXT.Company.Address[0].address_line1
  - 1.2.2.1 Indirizzo
- CAP
  - Mandatory: ERPNEXT.Company.Address[0].pincode
  - 1.2.2.3 CAP
- Comune
  - Mandatory: ERPNEXT.Company.Address[0].city
  - 1.2.2.4 Comune
- Provincia
  - Mandatory: ERPNEXT.Company.Address[0].county
  - 1.2.2.5 Provincia
- Nazione
  - Mandatory: ERPNEXT.Company.Address[0].country
  - 1.2.2.6 Nazione
- Fax
  - Not Mandatory: ERPNEXT.Company.fax
  - 1.2.5.2 Fax
  
###### Customer Fields

- Codice Destinatario
  - Mandatory: ERPNEXT_EFE.Customer.codicedestinatario
  - Default: 0000000 if Company
  - 1.1.4 CodiceDestinatario
- PEC Destinatario
  - Mandatory if ERPNEXT_EFE.Customer.codicedestinatario == “0000000”: ERPNEXT_EFE.Customer.pecdestinatario
  - 1.1.6 PECDestinatario
- Partita IVA
  - Mandatory: ERPNEXT.Customer.tax_id
  - 1.2.1.1.2 IdCodice
- Codice Fiscale
  - Not Mandatory: ERPNEXT_EFE.Customer.codicefiscale
  - 1.2.1.2 CodiceFiscale
- Denominazione
  - Mandatory: ERPNEXT.Customer.customer_name
  - 1.4.1.3.1 Denominazione
- Nome
  - Not Mandatory: ERPNEXT_EFE.Customer.nome
  - 1.4.1.3.2 Nome
- Cognome
  - Not Mandatory: ERPNEXT_EFE.Customer.cognome
  - 1.4.1.3.2 Cognome
- Indirizzo
  - Mandatory: ERPNEXT.Customer.Address[0].address_line1
  - 1.2.2.1 Indirizzo
- CAP
  - Mandatory: ERPNEXT.Customer.Address[0].pincode
  - 1.2.2.3 CAP
- Comune
  - Mandatory: ERPNEXT.Customer.Address[0].city
  - 1.2.2.4 Comune
- Provincia
  - Mandatory: ERPNEXT.Customer.Address[0].county
  - 1.2.2.5 Provincia
- Nazione
  - Mandatory: ERPNEXT.Customer.Address[0].country
  - 1.2.2.6 Nazione
  
##### Document Fields

- TipoDocumento
  - Mandatory: ERPNEXT_EFE.tipo_documento
  - This table will be use to bind ERPNext Document to admitted documents in Fattura Elettronica
  - 2.1.1.1 TipoDocumento
- Divisa
  - CONSTANT = EUR
  - 2.1.1.2 Divisa
- Data
  - Mandatory: ERPNEXT.DOCTYPE.posting_date
  - 2.1.1.3 Data
- Numero
  - Mandatory: ERPNEXT.DOCTYPE.naming_series
  - This field will be splitted and taken the integer from second token
  - 2.1.1.4 Numero
- ImportoTotaleDocumento
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.1.1.9 ImportoTotaleDocumento
- Causale
  - Mandatory: ERPNEXT_EFE.Company.Causale (Select)
- Natura
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.2.2 Natura
- ImponibileImporto
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.2.5 ImponibileImporto
- Imposta
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.2.6 Imposta
- EsigibilitaIVA
  - CONSTANT = I
  - 2.2.2.6 EsigibilitaIVA

##### Document Rows Fields

- NumeroLinea
  - COUNTER
  - 2.2.1.1 NumeroLinea
- CodiceTipo
  - CONSTANT = CODE
  - 2.2.1.3.1 CodiceTipo
- CodiceValore  
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.1.3.2 CodiceValore
- Descrizione
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.1.4 Descrizione
- Quantità
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.1.5 Quantita
- PrezzoUnitario
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.1.9 PrezzoUnitario
- PrezzoTotale
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.1.11 PrezzoTotale
- AliquotaIVA
  - Mandatory: ERPNEXT.DOCTYPE.XXXXX
  - 2.2.1.12 AliquotaIVA
  - 2.2.2.1 AliquotaIVA
  
**TO BE COMPLETED: 2.4.1 CondizioniPagamento**

**TO BE COMPLETED: 2.4.2 DettaglioPagamento**

**ACTUAL DEVELOPMENT BRANCH: electronic-invoice-lxml**

## Future implementation

An evolution of this process will be the capability to:
- apply Digital Signature using smart card reader;
- automatically send to SDI web service;
