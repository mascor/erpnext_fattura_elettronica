## Erpnext Fattura Elettronica ver. 0.0.1

App to export electronic invoice as mandated by the Italian Government

#### License

GPLv3

Reference (document issued by Italian Government):
https://www.agenziaentrate.gov.it/wps/wcm/connect/a8316033-6124-4667-99d8-ed143dc72c20/Provvedimento_30042018+.pdf?MOD=AJPERES&CACHEID=a8316033-6124-4667-99d8-ed143dc72c20

Requirements:

- Generate (at the end of the day) a unique XML file that exports all the selected Sales Invoice;
- The user will be able to select the invoices for a period and select using row checkboxes;
- User will click on "Export XML Invoices" and will be able to download the XML file containing the selected invoices;

For details about XML Schema see here:
http://www.fatturapa.gov.it/export/fatturazione/en/normativa/f-2.htm

This software will be a Frappe Custom App but can be part of the future Italian Localization

Plan:
- From the first week of October we will start to implement it.
- We will try to complete development before 12th of October (2018)
- Complete test before the end of October (2018)

Future implementation:
This is the first step, an evolution of this process will be the capability to:
- apply Digital Signature using smart card reader;
- automatically send to SDI web service;
