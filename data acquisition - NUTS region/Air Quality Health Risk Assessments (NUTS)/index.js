// node js import fetch and Deno.writeFile

const fs = require("fs");
const zlib = require("zlib");

// load all the cities from the csv file in "../EuroStat (Meta) - Cities"
const cities = [
  "Abruzzo",
  "Alentejo",
  "Algarve",
  "Alsace",
  "Andalucía",
  "Aquitaine",
  "Aragón",
  "Arnsberg",
  "Auvergne",
  "Basilicata",
  "Basse-Normandie",
  "Berlin",
  "Bourgogne",
  "Brandenburg",
  "Bratislavský kraj",
  "Braunschweig",
  "Bremen",
  "Bretagne",
  "Bucureşti - Ilfov",
  "Budapest",
  "Burgenland",
  "Calabria",
  "Campania",
  "Cantabria",
  "Castilla y León",
  "Castilla-La Mancha",
  "Cataluña",
  "Centre-Val de Loire",
  "Centro (PT)",
  "Centru",
  "Champagne-Ardenne",
  "Chemnitz",
  "Ciudad Autónoma de Ceuta",
  "Ciudad Autónoma de Melilla",
  "Comunidad Foral de Navarra",
  "Comunidad Valenciana",
  "Comunidad de Madrid",
  "Corse",
  "Darmstadt",
  "Detmold",
  "Dolnośląskie",
  "Drenthe",
  "Dresden",
  "Dél-Alföld",
  "Dél-Dunántúl",
  "Düsseldorf",
  "Eastern and Midland",
  "Eesti",
  "Emilia-Romagna",
  "Etelä-Suomi",
  "Extremadura",
  "Flevoland",
  "Franche-Comté",
  "Freiburg",
  "Friesland (NL)",
  "Friuli-Venezia Giulia",
  "Galicia",
  "Gelderland",
  "Gießen",
  "Grad Zagreb",
  "Groningen",
  "Hamburg",
  "Hannover",
  "Haute-Normandie",
  "Helsinki-Uusimaa",
  "Hovedstaden",
  "Illes Balears",
  "Jadranska Hrvatska",
  "Jihovýchod",
  "Jihozápad",
  "Karlsruhe",
  "Kassel",
  "Koblenz",
  "Kujawsko-pomorskie",
  "Kärnten",
  "Köln",
  "Közép-Dunántúl",
  "La Rioja",
  "Languedoc-Roussillon",
  "Latvija",
  "Lazio",
  "Leipzig",
  "Liguria",
  "Limburg (NL)",
  "Limousin",
  "Lombardia",
  "Lorraine",
  "Lubelskie",
  "Lubuskie",
  "Luxembourg",
  "Länsi-Suomi",
  "Lüneburg",
  "Malta",
  "Marche",
  "Mazowiecki regionalny",
  "Małopolskie",
  "Mecklenburg-Vorpommern",
  "Mellersta Norrland",
  "Midi-Pyrénées",
  "Midtjylland",
  "Mittelfranken",
  "Molise",
  "Moravskoslezsko",
  "Münster",
  "Niederbayern",
  "Niederösterreich",
  "Noord-Brabant",
  "Noord-Holland",
  "Nord-Est",
  "Nord-Pas-de-Calais",
  "Nord-Vest",
  "Nordjylland",
  "Norra Mellansverige",
  "Norte",
  "Northern and Western",
  "Nyugat-Dunántúl",
  "Oberbayern",
  "Oberfranken",
  "Oberpfalz",
  "Oberösterreich",
  "Opolskie",
  "Overijssel",
  "Panonska Hrvatska",
  "Pays-de-la-Loire",
  "País Vasco",
  "Pest",
  "Picardie",
  "Piemonte",
  "Podkarpackie",
  "Podlaskie",
  "Pohjois- ja Itä-Suomi",
  "Poitou-Charentes",
  "Pomorskie",
  "Praha",
  "Principado de Asturias",
  "Prov. Antwerpen",
  "Prov. Brabant wallon",
  "Prov. Hainaut",
  "Prov. Limburg (BE)",
  "Prov. Liège",
  "Prov. Luxembourg (BE)",
  "Prov. Namur",
  "Prov. Oost-Vlaanderen",
  "Prov. Vlaams-Brabant",
  "Prov. West-Vlaanderen",
  "Provence-Alpes-Côte d_Azur",
  "Provincia Autonoma di Bolzano/Bozen",
  "Provincia Autonoma di Trento",
  "Puglia",
  "Región de Murcia",
  "Rheinhessen-Pfalz",
  "Rhône-Alpes",
  "Région de Bruxelles-Capitale/Brussels Hoofdstedelijk Gewest",
  "Saarland",
  "Sachsen-Anhalt",
  "Salzburg",
  "Sardegna",
  "Schleswig-Holstein",
  "Schwaben",
  "Severovýchod",
  "Severozápad",
  "Sicilia",
  "Sjeverna Hrvatska",
  "Sjælland",
  "Småland med öarna",
  "Sostinės regionas",
  "Southern",
  "Steiermark",
  "Stockholm",
  "Stredné Slovensko",
  "Stuttgart",
  "Střední Morava",
  "Střední Čechy",
  "Sud - Muntenia",
  "Sud-Est",
  "Sud-Vest Oltenia",
  "Syddanmark",
  "Sydsverige",
  "Thüringen",
  "Tirol",
  "Toscana",
  "Trier",
  "Tübingen",
  "Umbria",
  "Unterfranken",
  "Utrecht",
  "Valle d_Aosta/Vallée d_Aoste",
  "Veneto",
  "Vest",
  "Vidurio ir vakarų Lietuvos regionas",
  "Vorarlberg",
  "Vzhodna Slovenija",
  "Västsverige",
  "Východné Slovensko",
  "Warmińsko-mazurskie",
  "Warszawski stołeczny",
  "Weser-Ems",
  "Wielkopolskie",
  "Wien",
  "Zachodniopomorskie",
  "Zahodna Slovenija",
  "Zeeland",
  "Zuid-Holland",
  "Západné Slovensko",
  "Área Metropolitana de Lisboa",
  "Åland",
  "Észak-Alföld",
  "Észak-Magyarország",
  "Île-de-France",
  "Östra Mellansverige",
  "Övre Norrland",
  "Łódzkie",
  "Śląskie",
  "Świętokrzyskie",
  "Ήπειρος",
  "Ανατολική Μακεδονία, Θράκη",
  "Αττική",
  "Βόρειο Αιγαίο",
  "Δυτική Ελλάδα",
  "Δυτική Μακεδονία",
  "Θεσσαλία",
  "Ιόνια Νησιά",
  "Κεντρική Μακεδονία",
  "Κρήτη",
  "Κύπρος",
  "Νότιο Αιγαίο",
  "Πελοπόννησος",
  "Στερεά Ελλάδα",
  "Северен централен",
  "Северозападен",
  "Североизточен",
  "Югозападен",
  "Югоизточен",
  "Южен централен"
]
const years = [2018, 2019, 2020];
const pollutants = ["PM2.5", "PM10", "O3", "NO2"];

cities.forEach((city) => {
  city_file = city.replace("/", "-");
  // try creating a folder with the city name
  try {
    fs.mkdirSync(`./${city_file}`);
  } catch (err) {
    // if the folder already exists, do nothing
    if (err.code !== "EEXIST") throw err;
  }

  years.forEach((year) => {
    pollutants.forEach((pollutant) => {
      let filePath = `./${city_file}/${city_file}_${year}_${pollutant}.csv.zip`;

      let city_url_encoded = encodeURIComponent(city);
      let pollutant_url_encoded = encodeURIComponent(pollutant);
      let year_url_encoded = encodeURIComponent(year);

      fetch(
        "https://discomap.eea.europa.eu/App/AQViewer/download?fqn=Airquality_Dissem.hra.nuts3_sel&f=csv",
        {
          headers: {
            accept:
              "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            pragma: "no-cache",
            "sec-ch-ua":
              '"Opera";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            cookie:
              "dtCookie=v_4_srv_-2D80_sn_S0HL1JVA638BSCE96JNJHHJQ3SNCGIB8; rxVisitor=16854764743222NGHMUD4Q3L2E9SVLOAD3R9LG94G5KLI; rxvt=1686593316372|1686591499930; dtLatC=1; dtSa=-; dtPC=-80$591499903_933h-vRIEGIQMKGTKKBUICMHBNUUHACHDOPSUR-0e0",
            Referer:
              "https://discomap.eea.europa.eu/App/AQViewer/index.html?fqn=Airquality_Dissem.hra.nuts3_sel&EUCountries=Yes&UrbanisationDegree=All%20Areas%20(incl.unclassified)&Year=2020&ScenarioDescription=WHO_2021_AQG_Scen_Base&AirPollutant=PM2.5",
            "Referrer-Policy": "strict-origin-when-cross-origin",
          },
          body:
            "request=%7B%22Page%22%3A0%2C%22SortBy%22%3A%22UrbanisationDegree%22%2C%22SortAscending%22%3Atrue%2C%22RequestFilter%22%3A%7B%22EUCountries%22%3A%7B%22FieldName%22%3A%22EUCountries%22%2C%22Values%22%3A%5B%22Yes%22%5D%7D%2C%22UrbanisationDegree%22%3A%7B%22FieldName%22%3A%22UrbanisationDegree%22%2C%22Values%22%3A%5B%22All+Areas+%28incl.unclassified%29%22%5D%7D%2C%22Year%22%3A%7B%22FieldName%22%3A%22Year%22%2C%22Values%22%3A%5B%22" +
            year_url_encoded +
            "%22%5D%7D%2C%22ScenarioDescription%22%3A%7B%22FieldName%22%3A%22ScenarioDescription%22%2C%22Values%22%3A%5B%22WHO_2021_AQG_Scen_Base%22%5D%7D%2C%22AirPollutant%22%3A%7B%22FieldName%22%3A%22AirPollutant%22%2C%22Values%22%3A%5B%22" +
            pollutant_url_encoded +
            "%22%5D%7D%2C%22NUTS2_Name%22%3A%7B%22FieldName%22%3A%22NUTS2_Name%22%2C%22Values%22%3A%5B%22" +
            city_url_encoded +
            "%22%5D%7D%7D%7D",
          method: "POST",
        }
      )
        .then((response) => {
          if (!response.ok) {
            // write the error into the file "./city/log.txt"
            fs.writeFileSync(
              `./${city_file}/log.txt`,
              `Error: ${response.status} ${response.statusText}`
            );
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.arrayBuffer();
        })
        .then((buffer) => {
          fs.writeFileSync(filePath, Buffer.from(buffer));
          fs.writeFileSync(
            `./${city_file}/log.txt`,
            `File downloaded and saved successfully!`
          );
          console.log("File downloaded and saved successfully!");
        })
        .catch((error) => {
          fs.writeFileSync(`./${city_file}/log.txt`, `Error: ${error.message}`);

          console.error("Error:", error.message);
        });
    });
  });
});

cities = []
for(let j = 0; j < countries.length; j++) {
  country = countries[j]
  document.getElementById(id="cmbCountry").value = country;
  // set a timer for 1 second to wait for the cities to load
  setTimeout(function () {}, 1000);
  cities_temp = document.getElementById(id="cmbCityName")
  for (i = 0; i < cities_temp.length; i++) {
    cities.push(cities_temp[i].value)
  }
};