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
- bench --site <SITENAME> install-app erpnext_fattura_elettronica

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

- From the first week of October we will start to implement it.
- Complete development before the end of October (2018)
- Complete test before the first week of November (2018)

## Future implementation

An evolution of this process will be the capability to:
- apply Digital Signature using smart card reader;
- automatically send to SDI web service;
