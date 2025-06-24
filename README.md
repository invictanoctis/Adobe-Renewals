## Adobe Renewal Tool

**Version:** v1.0

**Author:** Maximilian Menne // @invictanoctis on github

**Build Date:** v1.0 published at 24.06.2025 

**Target Platform:** Windows (.exe standalone)  

-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

## Deutsch

-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

## Beschreibung

Das **Adobe Renewal Tool** ist ein Automatisierungswerkzeug zur Erstellung und Versendung von Adobe Renewal Notices. Es liest Informationen aus streng strukturierten Excel-Dateien aus und integriert diese in einen automatisierten E-Mail-Prozess. Aufgrund des fest definierten Formats dieser Vorlagen ist eine Nutzung außerhalb der Organisation nur eingeschränkt möglich.

Der Versand erfolgt über einen globalen, applikationsbasierten Sign-In-Prozess, was die externe Nutzung zusätzlich einschränkt.  
Die Authentifizierung erfolgt über einen Azure Client Secret.

Zur Nachvollziehbarkeit und Transparenz stehen die verwendeten Excel-Vorlagen unten zum Download bereit.

---

## Erforderlich

- Eine Datei mit dem Namen 'reseller_information.xlsb' (fest codiert zur Fehlervermeidung)
- Eine Datei mit dem Namen 'renewal_overview.xlsb' (fest codiert zur Fehlervermeidung)
- Ein freigegebenes Microsoft 365-Postfach
- Eine Azure-Anwendung mit Graph API 'sendAs'-Berechtigung und aktivierter Client-Secret-Authentifizierung

---

## Anwendung

1. Doppelklicken Sie auf 'AdobeRenewalTool.exe', um das Tool zu starten — keine Installation erforderlich.
2. Folgen Sie der einfachen, geführten Benutzeroberfläche, um den Renewal-Workflow abzuschließen und den Versandprozess zu starten.
3. Wichtig: Jedes Mal, wenn das Datum geändert wurde, muss die zweite Excel-Datei ('renewal_overview.xlsb') neu geladen werden, da es sonst zu Problemen beim Parsen kommt.
4. Alle Aktionen werden in individuellen Logdateien protokolliert. Diese dienen gleichzeitig als Versandnachweis, da bei applikationsbasiertem Sign-In in der Regel kein 'Sent'-Ordner verfügbar ist.
5. Die Logdateien werden pro Sitzung im Unterordner 'logs/' gespeichert.

## Mailing

Die folgenden Platzhalter können im E-Mail-Text oder im Betreff verwendet werden. Sie werden bei der Verarbeitung automatisch mit den Werten aus der jeweiligen Zeile der Excel-Daten ersetzt:

| Platzhalter           | Ersetzt durch                                      |
|-----------------------|----------------------------------------------------|
| '[SAP-ID]'            | Die SAP-Nummer des Vertrags                        |
| '[Endkunden-Name]'    | Der Name des Endkunden                             |
| '[Endkunden-ID]'      | Die Adobe-ID des Endkunden                         |
| '[Kunden-Name]'       | Der Name des direkten Kunden/Resellers             |
| '[Kunden-ID]'         | Die Adobe-ID des direkten Kunden/Resellers         |
| '[Kunden-Mail]'       | Die E-Mail-Adresse des Kunden                      |
| '[Vertrags-Info]'     | Verlängerung/Kündigung Infromation                 |
| '[Ablaufdatum]'       | Das Vertragsablaufdatum (z.B. TT.MM.JJJJ)          |
| '[Produkt-Name]'      | Der Name des Produkts                              |
| '[Kondition-Text]'    | Ein bedingter Text basierend auf '[Vertrags-Info]' |

-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

## English

-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------


## Description

The **Adobe Renewal Tool** is an automation utility for Adobe renewal notices. It parses information from strictly structured Excel files and integrates it into an automated mailing process. Due to the rigid format of these Excel templates, use outside of the organization is only possible to a limited extent.

The mailing feature uses a global, application-based sign-in process, which further restricts external usage. 
Authentication is handled via Azure Client Secret.

Nevertheless, the Excel templates are provided below for download to ensure transparency and reproducibility.

---

## Required

- A file named 'reseller_information.xlsb' (hardcoded to prevent errors)
- A file named 'renewal_overview.xlsb' (hardcoded to prevent errors)
- A shared Microsoft 365 mailbox
- An Azure application with Graph API 'sendAs' permission and client secret authentication enabled

---

## How to Use

1. Double-click 'AdobeRenewalTool.exe' to launch the tool — no installation required.
2. Follow the simple, guided on-screen UI to complete the renewal workflow and initiate the sending process.
3. Important: Each time the date is changed, the second Excel file ('renewal_overview.xlsb') must be reloaded due to parsing-related limitations.
4. All actions are logged to individual log files. These also serve as a record of sent emails, since application-based sign-in typically does not retain messages in a 'Sent' folder.
5. Logging output is saved in the 'logs/' subfolder, with a new file created for each session.

## Mailing 

The following placeholders can be used in the email body or subject. They will automatically be replaced with values from each row of the Excel input data during processing:

| Placeholder           | Replaced With                                      |
|-----------------------|----------------------------------------------------|
| '[SAP-ID]'            | The SAP number of the contract                     |
| '[Endkunden-Name]'    | The name of the final (end) customer               |
| '[Endkunden-ID]'      | The Adobe ID of the final (end) customer           |
| '[Kunden-Name]'       | The name of the direct customer/reseller           |
| '[Kunden-ID]'         | The Adobe ID of the direct customer/reseller       |
| '[Kunden-Mail]'       | The customer's email address                       |
| '[Vertrags-Info]'     | Renewal/Termination Information                    |
| '[Ablaufdatum]'       | The contract's end date (e.g., DD.MM.YYYY)         |
| '[Produkt-Name]'      | The name of the product                            |
| '[Kondition-Text]'    | A conditional text based on '[Vertrags-Info]'      |

-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

##  Files Included

| File Name              | Description                                    |
|------------------------|------------------------------------------------|
| main.py                | main executable, backloop                      |
| lists.py               | Excel parcing, filtering and merging           |
| logs.py                | dynamic logging                                |
| mail.py                | dynamic mail subject and body text parcing     |
| ui.py                  | interface creation                             |
| authentication.py      | azure/graph token and sign-in                  |
| README.md              | This instruction file                          |
| .env                   | azure credentials                              |
| ressources/png         | customizable logo                              |

> All files are self-contained, frozen and require **no external Python installation**

-----------------------------------------------------------------------------------------------------------------------------------------------------------------