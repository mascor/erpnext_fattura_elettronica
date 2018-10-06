## ERPNext Fattura Elettronica ver. 0.0.1

App to export electronic invoice as mandated by the Italian Government

#### License

GPLv3

Reference (document issued by Italian Government):
https://www.agenziaentrate.gov.it/wps/wcm/connect/a8316033-6124-4667-99d8-ed143dc72c20/Provvedimento_30042018+.pdf?MOD=AJPERES&CACHEID=a8316033-6124-4667-99d8-ed143dc72c20

http://www.fatturapa.gov.it/export/fatturazione/sdi/Specifiche_tecniche_del_formato_FatturaPA_v1.2.1.pdf

## Requirements

Generate (at the end of the day) a unique XML file that exports all the selected Sales Invoice; The XML file will be complaint to:
http://www.fatturapa.gov.it/export/fatturazione/it/normativa/f-2.htm
and will be tested here:
http://sdi.fatturapa.gov.it/SdI2FatturaPAWeb/AccediAlServizioAction.do?pagina=controlla_fattura

This software will be a Frappe Custom App but can be part of the future Italian Localization

## Setup

- TO BE COMPLETED...

## User Manual

- User will filter Sales Invoices using ERPNext Sales Invoices List;
- After selecting Sales Invoices, user will click on "Export XML Invoices" and will be able to download the XML files containing the selected invoices;
- The system will generate one XML files for every customer
- These files can be used to send electronic invoices to SDI using a service like this:
https://guide.pec.it/fatturazione-elettronica/menu-carica-fattura/upload-fatture-in-formato-xml.aspx

## Plan

- From the first week of October we will start to implement it.
- We will try to complete development before 12th of October (2018)
- Complete test before the end of October (2018)

## Future implementation

An evolution of this process will be the capability to:
- apply Digital Signature using smart card reader;
- automatically send to SDI web service;
