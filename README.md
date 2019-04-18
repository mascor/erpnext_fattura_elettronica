## This Custom App works only with ERPNext v10.
## Part of the code of this app was included in ERPNext V11. To use the updated version, please refer to ERPNext Project: https://github.com/frappe/erpnext

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

- bench new-site SITENAME --install-app erpnext
- bench get-app --branch develop https://github.com/mascor/erpnext_fattura_elettronica.git
- bench --site SITENAME install-app erpnext_fattura_elettronica

##### Company Setup:

- Set Tax ID (Partita IVA)
- Set Regime Fiscale
- Set Company Address (Address Line 1, City/ Town, State (Provincia), Pincode (CAP)) 

##### Chart of accounts Setup:

If you need to use other kind of taxes, different from 22%, you can add it on the Item Master -> Item Tax. If you set to 0% it will ask to you the Natura.

##### Customers Setup:

- Codice Destinatario (by default 0000000)
- if Codice Destinario is 0000000, PEC Destinatario is mandatory
- Tax ID (Partita IVA)
- Set Customer Address (Address Line 1, City/ Town, State (Provincia), Pincode (CAP))

##### Items Setup:

- Create some Items, optionally setting the in the Item Tax section, a different Tax Account instead 22%

##### Sales Invoices Setup:

- Customer
- Insert some Items

##### EFE XML Export:

- Type of Document
- Company
- From Date
- To Date
Export

## How to Test

If you find an error or you're not able to validate your XML files, please open an Issue.
In every Issue you should write these informations:
- If is an ERPNext Exception, please explain the procedure you did step by step;
- If is a validation error write the Validation Code and attach the XML File;
- In every case attach screenshots errors or other screenshots could be useful for debug;

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

## Plan

- Complete development before the second week of November (2018)
- Complete test before the last week of November (2018)

## Implementation

Reference: 
- http://www.fatturapa.gov.it/export/fatturazione/sdi/Specifiche_tecniche_del_formato_FatturaPA_v1.2.1.pdf
- http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/Rappresentazione_tabellare_del_tracciato_FatturaPA_versione_1.2.1.pdf
