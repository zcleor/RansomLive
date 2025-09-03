import requests
import json
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# === CONFIGURATION ===

API_URL = "https://www.ransomlook.io/api/recent"
KEYWORDS = [
"swiss", 
".ch", "Schweiz", "suisse", "Switzerland", "Svizzera", "defence", "militär", "military", "regierung", "verwaltung", "Zürich", "Zurich", "Vermögensverwaltung", "Genf", "Geneva", "Basel", "Bern", "Berne", "Lausanne", "Luzern", "Lucerne", "St. Gallen", "Winterthur", "Lugano", "Biel", "Bienne", "Thun", "Köniz", "Schaffhausen", "Chur", "Fribourg", "Freiburg", "Neuchâtel", "Neuenburg", "Sion", "Sitten", "Uster",
"Zweifel Chips",
"Zur Rose",
"Zimmer GmbH",
"Ziegler",
"Zehnder",
"Ypsomed",
"Würth-Gruppe",
"World Steel Trade",
"Wicor Holding",
"Weidmann Holding",
"Werco Trade",
"Weleda",
"Wasserwerke Zug",
"Walo Bertschinger",
"VZ Holding",
"Von Roll",
"Volg",
"Vitol",
"Visilab",
"Vinci Energies Schweiz",
"Villiger Söhne",
"Vifor Pharma",
"Victorinox",
"Vetropack",
"Verkehrsbetriebe Zürich",
"Veritas",
"Vebego Schweiz",
"VAT Group",
"Varo Energy Holding",
"Variosystems",
"Valora",
"Vacheron Constantin",
"V-Zug",
"UPC Schweiz",
"Universitätsspital Zürich",
"Universitätsspital Basel",
"Unilever",
"u-blox",
"TX Markets",
"Triumph International",
"Trisa Holding",
"Traveco Transporte",
"Transports publics genevois",
"Transocean",
"Transgourmet Holding",
"TopPharm Genossenschaft",
"TopCC",
"Top Tip/Lumimart",
"Tissot",
"Thermoplan",
"The Swatch Group",
"Tetra Pak International",
"Tertianum Management",
"Temenos Group",
"Tech Data (Schweiz)",
"Tecan Group",
"Tata Consultancy Services Switzerland",
"Tarchini FoxTown",
"Tamoil",
"Tamedia",
"TAG Heuer",
"T-Systems Schweiz",
"Syngenta",
"Symantec",
"Swissport",
"swisspor",
"Swisslog",
"Swissgrid",
"Swisscom",
"Swiss Prime Site",
"Swiss International Air Lines",
"Swiss Household Services",
"Swiss Automotive Group",
"SV Group",
"Sunrise Communications",
"Sulzer",
"Straumann Holding",
"Stäubli",
"Starrag Group",
"Stadtwerke St. Gallen",
"Stadtwerk Winterthur",
"Stadler Rail",
"St. Gallisch-Appenzellische Kraftwerke",
"SRG SSR",
"SR Technics Switzerland",
"Spitäler Schaffhausen",
"Spital Wallis",
"Spar Holding",
"Spaeter",
"Sonova",
"Solothurner",
"SoftwareONE",
"Socar Energy Trading",
"Skyguide",
"SIX Group",
"Sipro Stahl",
"Sika",
"Sigvaris Group",
"SIG Combibloc Group",
"Siemens Schweiz",
"Siegfried Holding",
"Sicpa Holding",
"SGS",
"SFS Holding",
"Services industriels de Genève",
"Sensirion",
"Selecta",
"Securitas",
"Scott Corporation",
"Schweizer Zucker",
"Schweizer Paraplegiker-Stiftung",
"Schweiter Technologies",
"Schurter",
"Schneider Logistics Group",
"Schneider Electric (Schweiz)",
"Schmolz + Bickenbach",
"Schmid Bauunternehmung",
"Schindler Holding",
"Schenker Storen",
"Schätzle",
"Scania Schweiz",
"SBB Cargo",
"SBB",
"Saviva",
"Sauter Building Control",
"SAP (Schweiz)",
"Sanitas Troesch",
"Samsung Electric (Schweiz)",
"Salt Mobile",
"Sabag Holding",
"Ruag",
"Ronal Group",
"Romande Energie",
"Rolex",
"Roche Holding",
"Robert Bosch",
"Ringier",
"Rieter",
"Ricola",
"Richemont",
"Richard Mille",
"Rhomberg Sersa Rail",
"Rhenus Alpina",
"Rhätische Bahn (RhB)",
"Repower",
"Renault Suisse",
"Reishauer",
"Reinhard Fromm Holding",
"Reichle & De-Massari",
"Rehau",
"Rational International",
"Randstad (Schweiz)",
"Rado Uhren",
"Quickline",
"PSP Swiss Property",
"Primeo Energie-Gruppe",
"PricewaterhouseCoopers",
"PostLogistics",
"PostAuto Schweiz",
"Poenina",
"Planzer Holding",
"Pistor Holding",
"Pilatus Flugzeugwerke",
"Phoenix Mecano",
"Pfister Arco Holding",
"Peach Property Group",
"Patek Philippe",
"Partners Group Holding",
"Otto’s",
"Ospelt Food",
"Orior",
"Orell Füssli Holding",
"Orascom Development Holding",
"Orange Business Service",
"Oracle Software",
"On Running Shoes",
"Omya",
"Omega",
"Offix Holding",
"Oettinger Davidoff",
"Octapharma",
"Ochsner Sport",
"OC Oerlikon Corporation",
"Novartis",
"Nobel Biocare Services",
"Neue Zürcher Zeitung",
"Nestlé",
"Müller Schweiz",
"Müller Martini",
"MSC Cruises",
"Montres Longines",
"Montres Breguet",
"Montana Tech Components",
"Montana Aerospace",
"Model Holding",
"Mobimo Holding",
"Mobilezone Holding",
"MIR Trade",
"Mikron Holding",
"Migros-Genossenschafts-Bund",
"Migros Online",
"Migrolino",
"Migrol",
"Mifroma",
"Microspot",
"Microsoft Schweiz",
"Micarna",
"Mibelle",
"Metrohm",
"Metall Zug",
"MET Group",
"Mercuria Energy Trading",
"Mercedes-Benz Schweiz",
"Merbag Holding",
"Mepha",
"Meier Tobler",
"Mediterranean Shipping Company",
"Mediclinic Switzerland",
"Media Markt Schweiz",
"Medela Holding",
"Medbase Gesundheitszentren",
"Medacta International",
"McDonalds Suisse",
"Maxon Motor",
"Maus Frères Holding",
"Marti Holding",
"Manor",
"Mammut Sports Group",
"Magazine zum Globus",
"M + R Spedag Group",
"LV-St.Gallen",
"Luzerner Kantonsspital",
"Losinger Marazzi",
"Loomis Schweiz",
"Lonza Group",
"Logitech International",
"Lindt & Sprüngli",
"Lindenhofgruppe",
"Liebherr International",
"Lidl Schweiz",
"Leonteq",
"Lenovo (Schweiz) GmbH",
"LEM Holding",
"Landis+Gyr",
"Landi",
"Lagerhäuser der Centralschweiz",
"LafargeHolcim",
"L.U. Chopard & Cie",
"Kühne + Nagel International",
"Kudelski",
"Krono Holding",
"KPMG",
"Komax Holding",
"Kolmar Group",
"Kistler Instrumente",
"Kirchhofer AG",
"Kinderspital Zürich",
"Kibag Holding",
"Keytrade",
"Kestenholz-Gruppe",
"Kernkraftwerk Leibstadt",
"Kernkraftwerk Gösgen-Däniken",
"Kardex",
"Kantonsspital Winterthur",
"Kantonsspital Thurgau",
"Kantonsspital St. Gallen",
"Kantonsspital Graubünden",
"Kantonsspital Freiburg",
"Kantonsspital Baselland",
"Kantonsspital Baden",
"Kantonsspital Aarau",
"Kabelwerke Brugg",
"Jura Elektroapparate",
"Jungbunzlauer Suisse",
"Jumbo-Markt",
"Jowa",
"Jansen AG",
"Jaeger-LeCoultre",
"Ivoclar Vivadent",
"ITRIS",
"ISS Schweiz",
"Interroute",
"Interroll Holding",
"International Watch Company",
"Interhome HHD",
"Interdiscount",
"Intel Semiconductor",
"Insel Gruppe",
"Ingram Micro",
"Infosys Consulting Holding",
"Infinigate Holding",
"Inficon Holding",
"Ineos Holdings",
"Industrielle Werke Basel",
"Induni",
"Implenia",
"IKEA",
"IBSA Institut Biochimique",
"IBM Schweiz",
"Hupac",
"Hublot",
"Huber+Suhner",
"Huawei Technologies Switzerland",
"HRS Holding",
"HP Schweiz",
"Hoval Gruppe",
"Hotelplan Group",
"Hostettler-Gruppe",
"Hôpitaux universitaires de Genève",
"Holdigaz",
"Hochdorf Holding",
"Hipp Holding",
"Hilti",
"Highlight Communications",
"HG Commerciale",
"Hewlett-Packard (Schweiz)",
"Hero",
"Hans Oetiker Holding",
"Hamilton Bonaduz",
"Halter AG",
"Hälg Holding",
"Haco",
"Habasit",
"H&M Hennes & Mauritz",
"GVFI International",
"Gurit Holding",
"Gunvor",
"Groupe Eldora",
"Groupe E",
"Griesser Holding",
"Google Switzerland",
"Glencore International",
"Givaudan",
"Georg Utz Holding",
"Georg Fischer AG",
"Genossenschaft Zentralschweizer Milchproduzenten ZMP",
"Geberit",
"Gaznat",
"Gategroup Holding",
"Gasverbund Mittelland",
"Galliker Transport",
"Galenica",
"Galderma Holding",
"Frutiger Unternehmungen",
"Franke Group",
"Fracht AG",
"Forbo Holding",
"Flughafen Zürich",
"Florin AG",
"Firmenich International",
"Festina - Candino Watch",
"Ferring Pharmaceuticals",
"Fenaco",
"Feldschlösschen Getränke",
"Feintool International",
"EWL Energie Wasser Luzern Holding",
"EuroChem",
"Eugster/Frismag",
"Estavayer Lait",
"ESA-Einkaufsorganisation",
"Ernst & Young",
"ERNI International",
"Erne Holding",
"Ericsson",
"Ente Ospedaliero Cantonale (EOC)",
"Engie Services",
"Energy Financing Team",
"Energiedienst Holding",
"Energie Wasser Bern",
"Energie 360°",
"Endress+Hauser",
"Ems-Chemie",
"Emmi AG",
"Emil Frey",
"EMC Computer Systems",
"Elektro-Material AG",
"Elektrizitätswerke des Kantons Zürich",
"Elektrizitätswerk der Stadt Zürich",
"Egon Zehnder International",
"EDAG Engineering Group",
"EBL (Genossenschaft Elektra Baselland)",
"DXT Commodities",
"Dufry",
"DSS International",
"Dottikon ES Holding",
"Dormakaba Holding",
"DKSH Holding",
"Digitec Galaxus",
"Die Schweizerische Post",
"Denner",
"Deloitte",
"Debrunner Koenig Holding",
"Debiopharm International",
"DB Schenker Schweiz",
"Dätwyler Holding",
"CSL Behring",
"CSC Switzerland GmbH",
"Cremo",
"CPH Chemie + Papier",
"Coop@home",
"Coop-Gruppe",
"Coop Vitality",
"Coop Mineraloel",
"Coop Bau+Hobby",
"Conzzeta",
"Conforama Suisse",
"Competec",
"Comet Holding",
"Coltene Holding",
"Colosseum Dental Group",
"Cognizant Technology Solutions",
"Coca-Cola HBC Schweiz",
"Clariant",
"Cisco Systems (Switzerland) GmbH",
"Cicor",
"Chocolat Frey",
"CH Media",
"Ceva Logistics",
"Centravo Holding",
"Centralschweizerische Kraftwerke",
"Cargo24",
"Cargill International",
"Capri Sun Group Holding",
"Canon (Schweiz)",
"Camion-Transport",
"Calida Holding",
"C&A Mode",
"Bystronic Laser",
"Burkhalter Holding",
"Burckhardt Compression",
"Bulgari Horlogerie",
"Bühler Holding",
"Bucherer",
"Bucher Industries",
"BT Switzerland",
"Breitling",
"Bossard Holding",
"Bobst Group",
"BMW (Schweiz)",
"BLS Cargo",
"BLS",
"Blancpain",
"BKW",
"BHP Billiton Group",
"Bettermann",
"Bertschi",
"Bernina International",
"Bell Food Group",
"Belimo Holding",
"Behr Bircher Cellpack BBC",
"Bechtle Holding Schweiz",
"BeautyAlliance Schweiz",
"BDO AG",
"Bauwerk Group",
"Baumer Holding",
"Basler Verkehrs-Betriebe",
"Barry Callebaut",
"Bachem Holding",
"B. Braun Medical",
"Azienda Elettrica Ticinese",
"AZ Medien",
"Axpo Holding",
"AWS (Switzerland)",
"Avaloq Evolution",
"Autoneum Holding",
"Audemars Piguet",
"Asstra - Associated Traffic",
"Ascom Holding",
"Aryzta",
"Artemis Holding",
"Archroma Management",
"Apple Switzerland",
"APG SGA",
"Anicom",
"Ammann Group Holding",
"Ameropa Holding",
"AMAG-Gruppe",
"AMAC Aerospace Switzerland",
"Aluflexpack",
"Also Holding",
"Alpiq Holding",
"Allreal Holding",
"Alfred Müller AG",
"Aldi Suisse",
"Alcon",
"Agrola",
"AFG Arbonia-Forster-Holding",
"AEW Energie",
"Aevis Holding",
"Aebi Schmidt Holding",
"Aduno Holding",
"Adobe Systems (Schweiz)",
"Adecco",
"Actelion",
"Acino Holding",
"Acer (Switzerland)",
"Accenture",
"ABB",
"A.H. Meyer & Cie",
]
STORAGE_FILE = "filtered_results.json"

# Webland Email Settings
EMAIL_SENDER = os.getenv('EMAIL_SCRIPT')
EMAIL_PASSWORD = os.getenv('PW_SCRIPT')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')  # or another address
SMTP_SERVER = os.getenv('EMAIL_SERVER')
SMTP_PORT = 465  # SSL

# === FUNCTIONS ===

def fetch_data():
    response = requests.get(API_URL, headers={"accept": "application/json"})
    return response.json()

def matches_keywords(entry):
    content = (
        (entry.get("post_title") or "") + " " +
        (entry.get("description") or "")
    ).lower()

    matched = []
    for keyword in KEYWORDS:
        kw_lower = keyword.lower()

        if kw_lower in [".ch", ".swiss"]:
            # Match domain-like endings: e.g., example.ch, domain.swiss
            if re.search(rf"\b[\w\-]+{re.escape(kw_lower)}\b", content):
                matched.append(keyword)
        else:
            # Whole word match
            if re.search(rf"\b{re.escape(kw_lower)}\b", content):
                matched.append(keyword)

    return matched

def load_previous_results():
    if not os.path.exists(STORAGE_FILE):
        return [], set()
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            entries = json.load(f)
            uuid_set = {entry["post_title"] + entry["discovered"] for entry in entries}
            return entries, uuid_set
    except (json.JSONDecodeError, KeyError):
        return [], set()

def save_results(entries):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

def send_email(subject, body, images):
    msg = MIMEMultipart("related")
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject

    # Create alternative (plain + html)
    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)

    # Plain text version
    msg_alternative.attach(MIMEText(body, "plain"))

    # HTML version
    html_body = "<html><body>"
    html_body += body.replace("\n", "<br>")

    # Embed images
    for cid, img_data in images.items():
        html_body += f'<br><img src="cid:{cid}"><br>'

    html_body += "</body></html>"
    msg_alternative.attach(MIMEText(html_body, "html"))

    # Attach images
    for cid, img_data in images.items():
        img = MIMEImage(img_data)
        img.add_header('Content-ID', f'<{cid}>')
        img.add_header('Content-Disposition', 'inline', filename=f"{cid}.png")
        msg.attach(img)

    # Send email
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    data = fetch_data()
    previous_entries, previous_uuids = load_previous_results()
    current_entries = list(previous_entries)  # copy list

    email_body = ""
    images = {}
    found = False
    counter = 1

    for entry in data:

        uuid = entry["post_title"] + entry["discovered"]
        if uuid in previous_uuids:
            continue

        matched_keywords = matches_keywords(entry)
        if matched_keywords:
            found = True
            previous_uuids.add(uuid)
            entry["matched_keywords"] = matched_keywords
            current_entries.append(entry)

            entry_info = (
                f"🔍 <b>Title:</b> {entry.get('post_title', 'N/A')}<br>"
                f"🕒 <b>Discovered:</b> {entry.get('discovered', 'N/A')}<br>"
                f"📝 <b>Description:</b> {entry.get('description', 'N/A')}<br>"
                f"👥 <b>Group:</b> {entry.get('group_name', 'N/A')}<br>"
                f"🧩 <b>Matched Keywords:</b> {', '.join(matched_keywords)}<br>"
                f"🔗 <b>Link on RansomLook:</b> <a href='https://www.ransomlook.io/group/{entry.get('group_name', '')}'>Click here</a><br>"
                f"🧲 <b>Magnet:</b> {entry.get('magnet', 'None')}<br>"
            )

            screenshot_url = f"https://www.ransomlook.io/{entry.get('screen', '')}"
            if entry.get("screen"):
                try:
                    screenshot_response = requests.get(screenshot_url)
                    if screenshot_response.status_code == 200:
                        img_cid = f"screenshot{counter}"
                        images[img_cid] = screenshot_response.content
                        entry_info += f"🖼️ Screenshot below:<br>"
                        entry_info += f"<img src='cid:{img_cid}'><br>"
                        counter += 1
                except Exception as e:
                    print(f"⚠️ Failed to download screenshot: {e}")

            entry_info += "<hr>"
            email_body += entry_info
            print(entry_info.replace("<br>", "\n"))

    if found:
        send_email("🔔 New RansomLook Match", email_body, images)

    save_results(current_entries)

if __name__ == "__main__":
    main()

