"""Landmark data for blog post generation.

Each landmark dict contains metadata used to generate SEO-optimized
blog posts about landmark art prints.
"""

LANDMARKS = [
    {
        "key": "eiffel_tower",
        "name": "Eiffel Tower",
        "location": "Paris",
        "country": "France",
        "year": "1889",
        "description": (
            "The Eiffel Tower was built as the entrance arch for the 1889 World's Fair "
            "and has since become the most iconic symbol of Paris and France. Standing at "
            "330 meters tall, it was the world's tallest man-made structure for 41 years."
        ),
        "fun_facts": [
            "The tower was originally intended to be dismantled after 20 years but was saved because of its usefulness as a radio transmission tower.",
            "It takes 60 tons of paint to repaint the Eiffel Tower, which is done every 7 years.",
            "Gustave Eiffel had a private apartment at the top of the tower where he entertained guests like Thomas Edison.",
        ],
        "collection_handle": "eiffel-tower-art",
    },
    {
        "key": "taj_mahal",
        "name": "Taj Mahal",
        "location": "Agra",
        "country": "India",
        "year": "1653",
        "description": (
            "The Taj Mahal is a white marble mausoleum commissioned by Mughal Emperor Shah Jahan "
            "in memory of his beloved wife Mumtaz Mahal. Widely regarded as one of the most "
            "beautiful buildings ever created, it is a UNESCO World Heritage Site and one of the New Seven Wonders of the World."
        ),
        "fun_facts": [
            "Over 20,000 artisans worked for 22 years to complete the Taj Mahal.",
            "The four minarets surrounding the tomb are slightly tilted outward so they would fall away from the main structure in an earthquake.",
            "The marble changes color throughout the day — pinkish in the morning, white during the day, and golden under moonlight.",
        ],
        "collection_handle": "taj-mahal-art",
    },
    {
        "key": "colosseum",
        "name": "Colosseum",
        "location": "Rome",
        "country": "Italy",
        "year": "80",
        "description": (
            "The Colosseum is an ancient amphitheater in the heart of Rome that could hold "
            "between 50,000 and 80,000 spectators. Built under the Flavian dynasty, it hosted "
            "gladiatorial contests, public spectacles, and dramas for nearly four centuries."
        ),
        "fun_facts": [
            "The Colosseum had a retractable awning system called the velarium, operated by a team of sailors, to shade spectators from the sun.",
            "It is estimated that over 400,000 people and one million wild animals died in the Colosseum over its active years.",
            "The arena floor could be flooded to stage mock naval battles called naumachiae.",
        ],
        "collection_handle": "colosseum-art",
    },
    {
        "key": "great_wall",
        "name": "Great Wall of China",
        "location": "Northern China",
        "country": "China",
        "year": "700 BC",
        "description": (
            "The Great Wall of China is a series of fortifications stretching over 13,000 miles "
            "across northern China, built over centuries to protect against invasions from the north. "
            "It is the longest structure ever built by humans and a powerful symbol of Chinese civilization."
        ),
        "fun_facts": [
            "Contrary to popular myth, the Great Wall is not visible from space with the naked eye.",
            "Sticky rice was used as mortar in some sections, making it incredibly strong and durable.",
            "The wall was built by soldiers, peasants, and prisoners over a span of more than 2,000 years.",
        ],
        "collection_handle": "great-wall-art",
    },
    {
        "key": "notre_dame",
        "name": "Notre-Dame Cathedral",
        "location": "Paris",
        "country": "France",
        "year": "1345",
        "description": (
            "Notre-Dame de Paris is a medieval Catholic cathedral renowned for its French Gothic "
            "architecture, including its flying buttresses, rose windows, and gargoyles. Construction "
            "began in 1163 and took nearly 200 years to complete."
        ),
        "fun_facts": [
            "Victor Hugo's 1831 novel 'The Hunchback of Notre-Dame' helped spark a major restoration campaign that saved the deteriorating cathedral.",
            "The cathedral's three famous rose windows date from the 13th century and contain over 1,000 square meters of stained glass.",
            "After the devastating 2019 fire, over one billion euros were pledged for its restoration within just two days.",
        ],
        "collection_handle": "notre-dame-art",
    },
    {
        "key": "neuschwanstein",
        "name": "Neuschwanstein Castle",
        "location": "Schwangau, Bavaria",
        "country": "Germany",
        "year": "1886",
        "description": (
            "Neuschwanstein Castle is a 19th-century Romanesque Revival palace commissioned by "
            "King Ludwig II of Bavaria as a personal retreat. Its fairy-tale appearance has made "
            "it one of the most photographed buildings in Europe and a global icon of romantic architecture."
        ),
        "fun_facts": [
            "Walt Disney used Neuschwanstein as the primary inspiration for Sleeping Beauty Castle in Disneyland.",
            "King Ludwig II lived in the castle for only 172 days before his mysterious death in 1886.",
            "The castle receives over 1.4 million visitors per year, with up to 6,000 per day in summer.",
        ],
        "collection_handle": "neuschwanstein-art",
    },
    {
        "key": "mount_fuji",
        "name": "Mount Fuji",
        "location": "Honshu Island",
        "country": "Japan",
        "year": "100,000 BC",
        "description": (
            "Mount Fuji is Japan's tallest peak at 3,776 meters and an active stratovolcano that "
            "last erupted in 1707. Revered as a sacred mountain for centuries, it has been a subject "
            "of countless works of Japanese art, most famously Hokusai's 'Thirty-six Views of Mount Fuji.'"
        ),
        "fun_facts": [
            "Mount Fuji's nearly perfect symmetrical cone is actually formed by three overlapping volcanoes stacked on top of each other.",
            "The official climbing season is only two months long, from July to September, yet over 300,000 people summit each year.",
            "The mountain is considered one of Japan's three sacred mountains alongside Mount Tate and Mount Haku.",
        ],
        "collection_handle": "mount-fuji-art",
    },
    {
        "key": "golden_gate",
        "name": "Golden Gate Bridge",
        "location": "San Francisco",
        "country": "United States",
        "year": "1937",
        "description": (
            "The Golden Gate Bridge is a suspension bridge spanning the Golden Gate strait, the "
            "one-mile-wide channel between San Francisco Bay and the Pacific Ocean. Its striking "
            "International Orange color and Art Deco design have made it one of the most recognizable "
            "bridges in the world."
        ),
        "fun_facts": [
            "The bridge's famous 'International Orange' color was originally just the primer — the architect liked it so much he made it permanent.",
            "The bridge sways up to 27 feet sideways in high winds, a flexibility that is intentional and essential to its structural integrity.",
            "When the bridge opened to pedestrians in 1937, approximately 200,000 people walked across it on the first day.",
        ],
        "collection_handle": "golden-gate-art",
    },
    {
        "key": "sydney_opera",
        "name": "Sydney Opera House",
        "location": "Sydney",
        "country": "Australia",
        "year": "1973",
        "description": (
            "The Sydney Opera House is a multi-venue performing arts center with a distinctive "
            "sail-shaped roof designed by Danish architect Jorn Utzon. It is one of the most "
            "famous and distinctive buildings of the 20th century and a UNESCO World Heritage Site."
        ),
        "fun_facts": [
            "The project was originally estimated at $7 million but ended up costing $102 million and took 16 years to build.",
            "The roof is covered with over one million tiles that were manufactured in Sweden and are self-cleaning.",
            "Architect Jorn Utzon never saw the finished building in person — he left the project in 1966 due to disputes and never returned to Sydney.",
        ],
        "collection_handle": "sydney-opera-art",
    },
    {
        "key": "santorini",
        "name": "Santorini",
        "location": "Cyclades Islands",
        "country": "Greece",
        "year": "3000 BC",
        "description": (
            "Santorini is a volcanic island in the Aegean Sea famous for its dramatic caldera views, "
            "whitewashed buildings with blue domes, and spectacular sunsets. The island was shaped "
            "by one of the largest volcanic eruptions in recorded history around 1600 BC."
        ),
        "fun_facts": [
            "The massive Minoan eruption of Santorini around 1600 BC may have inspired Plato's legend of Atlantis.",
            "The island's iconic blue-domed churches were originally painted blue because it was the cheapest pigment available to fishermen.",
            "Santorini has no natural fresh water supply — the island relies on desalination plants and imported water.",
        ],
        "collection_handle": "santorini-art",
    },
    {
        "key": "angkor_wat",
        "name": "Angkor Wat",
        "location": "Siem Reap",
        "country": "Cambodia",
        "year": "1150",
        "description": (
            "Angkor Wat is the largest religious monument in the world, originally built as a "
            "Hindu temple dedicated to Vishnu before gradually transforming into a Buddhist site. "
            "Its intricate bas-reliefs and towering spires represent the pinnacle of classical Khmer architecture."
        ),
        "fun_facts": [
            "Angkor Wat is oriented to the west, unlike most Hindu temples, which may indicate it was built as a funerary temple.",
            "The temple complex covers over 400 acres — larger than Vatican City.",
            "It appears on the Cambodian national flag, making Cambodia the only country with a building on its flag.",
        ],
        "collection_handle": "angkor-wat-art",
    },
    {
        "key": "machu_picchu",
        "name": "Machu Picchu",
        "location": "Cusco Region",
        "country": "Peru",
        "year": "1450",
        "description": (
            "Machu Picchu is a 15th-century Inca citadel perched high in the Andes Mountains "
            "at nearly 2,500 meters above sea level. Abandoned during the Spanish Conquest and "
            "unknown to the outside world until 1911, it remains one of the most extraordinary "
            "archaeological sites on Earth."
        ),
        "fun_facts": [
            "The stones of Machu Picchu were cut so precisely that no mortar was used, yet a knife blade cannot fit between them.",
            "The site was never discovered by Spanish conquistadors, which is why it remains so remarkably well-preserved.",
            "Machu Picchu was built on two fault lines, and earthquakes actually cause the stones to bounce and resettle into place.",
        ],
        "collection_handle": "machu-picchu-art",
    },
    {
        "key": "sagrada_familia",
        "name": "Sagrada Familia",
        "location": "Barcelona",
        "country": "Spain",
        "year": "2026",
        "description": (
            "The Sagrada Familia is a monumental basilica designed by Antoni Gaudi that has been "
            "under construction since 1882. Its organic, nature-inspired forms and towering spires "
            "blend Gothic and Art Nouveau styles in a way that is utterly unique in world architecture."
        ),
        "fun_facts": [
            "When completed, the tallest tower will reach 172.5 meters, making it the tallest church in the world.",
            "Gaudi knew he would not live to see its completion and said, 'My client is not in a hurry' — referring to God.",
            "Modern technology including 3D printing and computer-aided design has dramatically accelerated construction in recent years.",
        ],
        "collection_handle": "sagrada-familia-art",
    },
    {
        "key": "parthenon",
        "name": "Parthenon",
        "location": "Athens",
        "country": "Greece",
        "year": "432 BC",
        "description": (
            "The Parthenon is a former temple on the Athenian Acropolis dedicated to the goddess "
            "Athena, built at the height of the Athenian Empire. It is considered the finest example "
            "of Doric architecture and has influenced Western building design for over two millennia."
        ),
        "fun_facts": [
            "The Parthenon's columns are not perfectly straight — they curve slightly inward to create the optical illusion of perfect symmetry.",
            "In the 17th century, the Parthenon was being used as a gunpowder magazine by the Ottomans when a Venetian cannonball caused a massive explosion that destroyed much of the structure.",
            "The original building housed a 12-meter-tall gold and ivory statue of Athena that has been lost to history.",
        ],
        "collection_handle": "parthenon-art",
    },
    {
        "key": "stonehenge",
        "name": "Stonehenge",
        "location": "Wiltshire",
        "country": "England",
        "year": "2500 BC",
        "description": (
            "Stonehenge is a prehistoric stone circle on Salisbury Plain whose purpose and construction "
            "methods remain one of archaeology's greatest mysteries. The monument was built in stages "
            "over roughly 1,500 years and aligns precisely with the sunrise on the summer solstice."
        ),
        "fun_facts": [
            "The largest stones weigh about 25 tons and were transported from 25 miles away, while the smaller bluestones came from Wales, over 150 miles distant.",
            "Stonehenge was used as a burial ground for over 500 years, with cremated remains of up to 240 people discovered at the site.",
            "Charles Darwin was one of the first to study how earthworms were slowly burying the stones by bringing soil to the surface.",
        ],
        "collection_handle": "stonehenge-art",
    },
    {
        "key": "moai",
        "name": "Moai Statues",
        "location": "Easter Island",
        "country": "Chile",
        "year": "1250",
        "description": (
            "The Moai are nearly 1,000 monolithic stone statues carved by the Rapa Nui people "
            "on Easter Island between the 13th and 16th centuries. These enormous figures, with "
            "their oversized heads and solemn expressions, were created to honor ancestral chiefs and deified leaders."
        ),
        "fun_facts": [
            "The average Moai stands about 4 meters tall and weighs 12.5 tons, but the largest ever erected was nearly 10 meters and weighed 82 tons.",
            "Researchers demonstrated that the statues were likely 'walked' to their locations by rocking them side to side using ropes.",
            "Almost all Moai face inland rather than out to sea, watching over the villages they were meant to protect.",
        ],
        "collection_handle": "moai-art",
    },
    {
        "key": "pyramids_giza",
        "name": "Pyramids of Giza",
        "location": "Giza",
        "country": "Egypt",
        "year": "2560 BC",
        "description": (
            "The Pyramids of Giza are the oldest of the Seven Wonders of the Ancient World and "
            "the only one still largely intact. Built as tombs for the pharaohs Khufu, Khafre, "
            "and Menkaure, the Great Pyramid stood as the tallest man-made structure for over 3,800 years."
        ),
        "fun_facts": [
            "The Great Pyramid contains an estimated 2.3 million stone blocks, each weighing an average of 2.5 tons.",
            "The four sides of the Great Pyramid are aligned almost perfectly with the four cardinal directions, with less than 0.05 degrees of error.",
            "The pyramids were originally encased in polished white limestone that gleamed brilliantly in the Egyptian sun.",
        ],
        "collection_handle": "pyramids-of-giza-art",
    },
    {
        "key": "petra",
        "name": "Petra",
        "location": "Ma'an Governorate",
        "country": "Jordan",
        "year": "312 BC",
        "description": (
            "Petra is an ancient city carved directly into rose-red sandstone cliffs by the "
            "Nabataean people, who made it their capital and a vital crossroads for the incense "
            "trade. Often called the 'Rose City,' it was lost to the Western world for centuries "
            "until its rediscovery in 1812."
        ),
        "fun_facts": [
            "Only about 15% of Petra has been excavated — the vast majority of the city remains underground and unexplored.",
            "The Nabataeans engineered a sophisticated water conduit system that allowed the desert city to support a population of 30,000.",
            "Petra's Treasury facade was featured as the hiding place of the Holy Grail in 'Indiana Jones and the Last Crusade.'",
        ],
        "collection_handle": "petra-art",
    },
    {
        "key": "st_basils",
        "name": "St. Basil's Cathedral",
        "location": "Moscow",
        "country": "Russia",
        "year": "1561",
        "description": (
            "St. Basil's Cathedral stands at one end of Red Square in Moscow with its iconic "
            "cluster of colorful onion domes. Built by order of Ivan the Terrible to commemorate "
            "the capture of Kazan, it is one of the most recognizable symbols of Russia."
        ),
        "fun_facts": [
            "Legend holds that Ivan the Terrible had the architects blinded after completion so they could never build anything to rival it.",
            "The cathedral is actually nine separate chapels built on a single foundation, each topped with its own unique dome.",
            "Stalin reportedly ordered the cathedral demolished to make room for military parades, but architect Pyotr Baranovsky refused and was imprisoned — the cathedral survived.",
        ],
        "collection_handle": "st-basils-art",
    },
    {
        "key": "chichen_itza",
        "name": "Chichen Itza",
        "location": "Yucatan",
        "country": "Mexico",
        "year": "600",
        "description": (
            "Chichen Itza was one of the largest and most important cities of the Maya civilization, "
            "known for its remarkable pyramid El Castillo and advanced astronomical knowledge. "
            "The site blends Maya and Toltec architectural styles and is one of the New Seven Wonders of the World."
        ),
        "fun_facts": [
            "During the spring and autumn equinoxes, a shadow pattern on El Castillo creates the illusion of a serpent slithering down the pyramid's staircase.",
            "El Castillo has 365 steps — one for each day of the solar year — demonstrating the Maya's extraordinary astronomical precision.",
            "If you clap your hands at the base of El Castillo, the echo that returns sounds remarkably like the chirp of a quetzal bird, sacred to the Maya.",
        ],
        "collection_handle": "chichen-itza-art",
    },
    {
        "key": "christ_redeemer",
        "name": "Christ the Redeemer",
        "location": "Rio de Janeiro",
        "country": "Brazil",
        "year": "1931",
        "description": (
            "Christ the Redeemer is a 30-meter Art Deco statue of Jesus Christ atop Mount "
            "Corcovado overlooking Rio de Janeiro. One of the New Seven Wonders of the World, "
            "it has become an enduring symbol of both Rio and Brazil."
        ),
        "fun_facts": [
            "The statue was designed by French sculptor Paul Landowski and built by Brazilian engineer Heitor da Silva Costa using reinforced concrete and soapstone.",
            "Lightning strikes the statue an average of three to six times per year, and a 2014 storm chipped the tip of the right thumb.",
            "The outstretched arms span 28 meters wide, and the statue weighs approximately 635 metric tons.",
        ],
        "collection_handle": "christ-the-redeemer-art",
    },
    {
        "key": "hagia_sophia",
        "name": "Hagia Sophia",
        "location": "Istanbul",
        "country": "Turkey",
        "year": "537",
        "description": (
            "Hagia Sophia was built as a Byzantine cathedral and served as the world's largest "
            "cathedral for nearly a thousand years before being converted into a mosque after the "
            "Ottoman conquest in 1453. Its massive dome was an engineering marvel that influenced "
            "religious architecture for centuries."
        ),
        "fun_facts": [
            "The main dome is 31 meters in diameter and appears to float above the building, supported by hidden pendentives that distribute its weight.",
            "Emperor Justinian reportedly exclaimed 'Solomon, I have surpassed thee!' upon seeing the completed building.",
            "The building has served as a cathedral, mosque, museum, and mosque again over its 1,500-year history.",
        ],
        "collection_handle": "hagia-sophia-art",
    },
    {
        "key": "tower_of_pisa",
        "name": "Leaning Tower of Pisa",
        "location": "Pisa",
        "country": "Italy",
        "year": "1372",
        "description": (
            "The Leaning Tower of Pisa is a freestanding bell tower famous for its unintended "
            "tilt, which began during construction due to soft ground on one side. The tower took "
            "nearly 200 years to build and leans at about 3.97 degrees from vertical."
        ),
        "fun_facts": [
            "The tower began leaning during construction in 1173, and builders tried to compensate by making upper floors slightly taller on one side.",
            "Galileo Galilei reportedly dropped two cannonballs of different masses from the tower to demonstrate that objects fall at the same rate regardless of weight.",
            "A massive stabilization project completed in 2001 reduced the lean and ensured the tower will remain stable for at least another 200 years.",
        ],
        "collection_handle": "tower-of-pisa-art",
    },
    {
        "key": "big_ben",
        "name": "Big Ben",
        "location": "London",
        "country": "England",
        "year": "1859",
        "description": (
            "Big Ben is the nickname for the Great Bell inside the Elizabeth Tower at the north end "
            "of the Palace of Westminster in London. The tower and its clock have become one of the "
            "most prominent symbols of London and the United Kingdom."
        ),
        "fun_facts": [
            "Big Ben technically refers only to the 13.5-ton bell inside the tower, not the tower itself, which was renamed Elizabeth Tower in 2012.",
            "The clock is regulated by adding or removing old penny coins on the pendulum mechanism to adjust its speed.",
            "The tower leans about 0.26 degrees to the northwest due to ground conditions, earning it the occasional nickname 'the Leaning Tower of London.'",
        ],
        "collection_handle": "big-ben-art",
    },
    {
        "key": "statue_of_liberty",
        "name": "Statue of Liberty",
        "location": "New York City",
        "country": "United States",
        "year": "1886",
        "description": (
            "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in "
            "New York Harbor, a gift from France to the United States. Standing 93 meters from "
            "ground to torch tip, Lady Liberty has welcomed millions of immigrants arriving by sea "
            "and remains an enduring symbol of freedom and democracy."
        ),
        "fun_facts": [
            "The statue's copper skin is only 2.4 millimeters thick — about the thickness of two pennies stacked together.",
            "Gustave Eiffel, who later built the Eiffel Tower, designed the statue's internal iron framework.",
            "The statue's full name is 'Liberty Enlightening the World,' and the broken chains at her feet symbolize freedom from oppression.",
        ],
        "collection_handle": "statue-of-liberty-art",
    },
    # ----- Phase 2 Landmarks -----
    {
        "key": "amsterdam_canals",
        "name": "Amsterdam Canal Ring",
        "location": "Amsterdam",
        "country": "Netherlands",
        "year": "1613",
        "description": (
            "The Amsterdam Canal Ring is a network of concentric waterways built during the Dutch "
            "Golden Age that defines the city's iconic crescent shape. This UNESCO World Heritage "
            "Site features over 100 kilometers of canals, 1,500 bridges, and thousands of narrow "
            "merchant houses lining the water's edge."
        ),
        "fun_facts": [
            "The three main canals — Herengracht, Keizersgracht, and Prinsengracht — were dug simultaneously in the early 17th century as part of one of the most ambitious urban planning projects in history.",
            "Amsterdam has more bridges than Venice, with approximately 1,753 spanning its canals compared to Venice's roughly 400.",
            "The canal houses lean forward intentionally — their tilted facades made it easier to hoist furniture and goods up to the upper floors using the beam hooks that still protrude from many rooftops.",
        ],
        "collection_handle": "amsterdam-canal-ring-art",
    },
    {
        "key": "bagan_temples",
        "name": "Bagan Temple Plain",
        "location": "Mandalay Region",
        "country": "Myanmar",
        "year": "1057",
        "description": (
            "The Bagan Temple Plain is an ancient archaeological zone containing over 2,000 Buddhist "
            "temples, pagodas, and monasteries spread across a vast plain along the Irrawaddy River. "
            "Built between the 9th and 13th centuries during the Pagan Kingdom, it is one of the "
            "densest concentrations of sacred architecture in the world."
        ),
        "fun_facts": [
            "At its peak in the 13th century, Bagan had over 10,000 Buddhist temples — the remaining 2,200 are survivors of centuries of earthquakes and weathering.",
            "Many temples contain original frescoes and murals that are over 800 years old, depicting scenes from Buddhist cosmology and daily life.",
            "Hot air balloon rides over Bagan at sunrise have become one of Southeast Asia's most iconic travel experiences.",
        ],
        "collection_handle": "bagan-temple-plain-art",
    },
    {
        "key": "bruges_medieval",
        "name": "Bruges Medieval Center",
        "location": "Bruges",
        "country": "Belgium",
        "year": "1100",
        "description": (
            "The medieval center of Bruges is one of Europe's best-preserved Gothic cities, with "
            "winding cobblestone streets, picturesque canals, and stunning Flemish architecture. "
            "Once one of the wealthiest trading cities in the world, its historic core is a UNESCO "
            "World Heritage Site often called the Venice of the North."
        ),
        "fun_facts": [
            "Bruges was the commercial capital of northern Europe in the 13th century, and the world's first stock exchange was established here in 1309.",
            "The Belfry tower in the Market Square stands 83 meters tall and houses a carillon of 47 bells that still plays melodies throughout the day.",
            "The city's canals were originally built for trade but fell into disuse — their preservation for beauty rather than commerce helped Bruges avoid the industrial modernization that altered many European cities.",
        ],
        "collection_handle": "bruges-medieval-center-art",
    },
    {
        "key": "charles_bridge",
        "name": "Charles Bridge",
        "location": "Prague",
        "country": "Czech Republic",
        "year": "1402",
        "description": (
            "Charles Bridge is a medieval stone arch bridge crossing the Vltava River in Prague, "
            "lined with 30 baroque statues of saints. Commissioned by Emperor Charles IV in 1357 "
            "and completed in the early 15th century, it served as the only crossing between Old "
            "Town and Prague Castle for over 400 years."
        ),
        "fun_facts": [
            "Legend says Charles IV laid the foundation stone on July 9, 1357 at 5:31 AM because the date forms a palindrome (1-3-5-7-9-7-5-3-1), which was considered auspicious.",
            "Egg yolks were mixed into the mortar to strengthen the bridge — though modern analysis suggests this may be more legend than fact.",
            "Touching the bronze plaque depicting the martyrdom of St. John of Nepomuk on the bridge is said to bring good luck and ensure your return to Prague.",
        ],
        "collection_handle": "charles-bridge-art",
    },
    {
        "key": "chefchaouen",
        "name": "Chefchaouen",
        "location": "Rif Mountains",
        "country": "Morocco",
        "year": "1471",
        "description": (
            "Chefchaouen is a small mountain city in northern Morocco famous for its striking "
            "blue-washed buildings that cascade down the hillside. Founded in 1471 as a fortress "
            "against Portuguese invasions, its blue-painted medina has made it one of the most "
            "photographed cities in Africa."
        ),
        "fun_facts": [
            "The tradition of painting buildings blue is often attributed to Jewish refugees who settled here in the 1930s, as blue symbolizes the sky and heaven in Jewish tradition.",
            "Chefchaouen was virtually isolated from the outside world until 1920, when Spanish troops occupied the city and found its inhabitants had never seen a foreigner.",
            "The city sits at an elevation of 564 meters in the Rif Mountains and is surrounded by two peaks whose shape resembles goat horns — 'chaouen' means horns in the local Berber language.",
        ],
        "collection_handle": "chefchaouen-art",
    },
    {
        "key": "edinburgh_old_town",
        "name": "Edinburgh Old Town",
        "location": "Edinburgh",
        "country": "Scotland",
        "year": "1100",
        "description": (
            "Edinburgh's Old Town stretches along a dramatic rocky ridge from Edinburgh Castle down "
            "to the Palace of Holyroodhouse, forming the famous Royal Mile. Its medieval street plan "
            "and towering tenement buildings, some reaching eleven stories, preserve a unique "
            "atmosphere of Scotland's storied past."
        ),
        "fun_facts": [
            "Edinburgh's Old Town is built on layers of itself — underground vaults and passageways from earlier centuries lie beneath the modern streets, some now open as tourist attractions.",
            "The Royal Mile is actually 1.12 miles long, running from Edinburgh Castle to the Scottish Parliament at Holyroodhouse.",
            "J.K. Rowling wrote much of the early Harry Potter books in Edinburgh cafes, and many Old Town landmarks are said to have inspired locations in the series.",
        ],
        "collection_handle": "edinburgh-old-town-art",
    },
    {
        "key": "fushimi_inari",
        "name": "Fushimi Inari Shrine",
        "location": "Kyoto",
        "country": "Japan",
        "year": "711",
        "description": (
            "Fushimi Inari Shrine is the head shrine of Inari, the Shinto god of rice and prosperity, "
            "famous for its thousands of vermilion torii gates that wind through the forested slopes "
            "of Mount Inari. The trail of gates stretches over 4 kilometers and creates one of the "
            "most mesmerizing sacred walkways on Earth."
        ),
        "fun_facts": [
            "There are approximately 10,000 torii gates along the trails, each donated by individuals or businesses as offerings for prosperity and good fortune.",
            "The shrine's fox statues are messengers of Inari — foxes are believed to be Inari's supernatural servants and often hold a key, jewel, or sheaf of rice in their mouths.",
            "Fushimi Inari is the most popular tourist destination in all of Japan according to TripAdvisor, and the full hike to the summit takes about 2-3 hours.",
        ],
        "collection_handle": "fushimi-inari-shrine-art",
    },
    {
        "key": "giants_causeway",
        "name": "Giant's Causeway",
        "location": "County Antrim",
        "country": "Northern Ireland",
        "year": "60 million years ago",
        "description": (
            "The Giant's Causeway is a natural formation of about 40,000 interlocking basalt columns "
            "created by an ancient volcanic eruption. Most columns are hexagonal and fit together "
            "like stepping stones leading into the sea, creating a landscape so perfectly geometric "
            "it seems almost artificial."
        ),
        "fun_facts": [
            "Irish legend says the causeway was built by the giant Finn McCool so he could walk to Scotland to fight his rival Benandonner — and identical columns exist on the Scottish island of Staffa.",
            "The tallest columns are about 12 meters high, and the solidified lava in the cliffs is up to 28 meters thick in places.",
            "While most columns are hexagonal, some have four, five, seven, or eight sides — the hexagonal shape forms naturally because it is the most efficient way for cooling lava to crack.",
        ],
        "collection_handle": "giants-causeway-art",
    },
    {
        "key": "guanajuato",
        "name": "Guanajuato",
        "location": "Guanajuato State",
        "country": "Mexico",
        "year": "1554",
        "description": (
            "Guanajuato is a colorful colonial city nestled in a narrow valley in central Mexico, "
            "famous for its brightly painted houses stacked up steep hillsides and its underground "
            "street network of former river tunnels. Founded as a silver mining town, its extraordinary "
            "wealth produced stunning baroque architecture now recognized as a UNESCO World Heritage Site."
        ),
        "fun_facts": [
            "The city's underground road network was created by diverting the Guanajuato River through tunnels after devastating floods — cars now drive through these beautifully lit former river channels.",
            "Guanajuato produced nearly a third of the world's silver supply during the colonial era, making it one of the richest cities in the Americas.",
            "The Callejon del Beso (Alley of the Kiss) is so narrow that lovers on opposing balconies can lean across and kiss — legend says couples who kiss on the third step will have seven years of happiness.",
        ],
        "collection_handle": "guanajuato-art",
    },
    {
        "key": "hallgrimskirkja",
        "name": "Hallgrimskirkja",
        "location": "Reykjavik",
        "country": "Iceland",
        "year": "1986",
        "description": (
            "Hallgrimskirkja is a Lutheran church and Reykjavik's most prominent landmark, designed "
            "to resemble the basalt lava flows of Iceland's volcanic landscape. At 74.5 meters tall, "
            "it is the largest church in Iceland and took 41 years to build, from 1945 to 1986."
        ),
        "fun_facts": [
            "The church's distinctive shape was inspired by the columnar basalt formations found at places like Svartifoss waterfall in Vatnajokull National Park.",
            "A 15-meter statue of Leif Eriksson stands in front of the church — it was a gift from the United States in 1930, predating the church itself by 15 years.",
            "The church houses a massive 5,275-pipe organ that weighs 25 tons and stands 15 meters tall, and its observation tower offers panoramic views of the entire city.",
        ],
        "collection_handle": "hallgrimskirkja-art",
    },
    {
        "key": "hapenny_bridge",
        "name": "Ha'penny Bridge",
        "location": "Dublin",
        "country": "Ireland",
        "year": "1816",
        "description": (
            "The Ha'penny Bridge is a pedestrian bridge spanning the River Liffey in Dublin, "
            "named after the half-penny toll once charged to cross it. Built in 1816, this elegant "
            "cast-iron bridge is one of Dublin's most iconic landmarks and the oldest pedestrian "
            "bridge in the city."
        ),
        "fun_facts": [
            "The bridge was officially named the Liffey Bridge but earned its nickname from the half-penny toll charged until 1919 — people grumbled about the fee but used it anyway.",
            "Before the bridge was built, the crossing was operated by William Walsh's ferry service, and the bridge was constructed as a condition of his ferry license expiring.",
            "The bridge was nearly demolished in 1913 to make way for a wider crossing, but public outcry saved it — it was fully restored in 2001 and painted its distinctive white color.",
        ],
        "collection_handle": "hapenny-bridge-art",
    },
    {
        "key": "havana_vieja",
        "name": "Old Havana",
        "location": "Havana",
        "country": "Cuba",
        "year": "1519",
        "description": (
            "Old Havana is the historic heart of Cuba's capital, a vibrant district of baroque and "
            "neoclassical architecture, crumbling pastel facades, and classic American cars frozen "
            "in time. Founded by the Spanish in 1519, its well-preserved colonial core is a UNESCO "
            "World Heritage Site and one of the Caribbean's most atmospheric neighborhoods."
        ),
        "fun_facts": [
            "Old Havana's streets are filled with pre-1960 American cars because the US trade embargo froze car imports — Cubans have kept these vintage vehicles running for over 60 years with improvised parts.",
            "The city was once the staging point for Spanish treasure fleets carrying gold and silver from the Americas back to Spain, making it one of the most heavily fortified cities in the New World.",
            "Ernest Hemingway lived near Havana for over 20 years, and his favorite bar El Floridita in Old Havana still has a bronze statue of him sitting at his usual spot.",
        ],
        "collection_handle": "old-havana-art",
    },
    {
        "key": "hawa_mahal",
        "name": "Hawa Mahal",
        "location": "Jaipur",
        "country": "India",
        "year": "1799",
        "description": (
            "Hawa Mahal, or the Palace of Winds, is a stunning pink sandstone facade with 953 small "
            "windows designed to allow royal women to observe street life without being seen. Built "
            "by Maharaja Sawai Pratap Singh in 1799, its honeycomb-like exterior is the most "
            "recognizable landmark of Jaipur, the Pink City."
        ),
        "fun_facts": [
            "The palace is only one room deep in most places — it is essentially an elaborate facade, more like a decorative screen than a full building.",
            "The 953 jharokha windows create a constant breeze through the structure, functioning as an ancient air conditioning system that gives the palace its name.",
            "Hawa Mahal was inspired by the crown of the Hindu god Krishna, and its pyramidal shape resembles a royal tiara when viewed from the street.",
        ],
        "collection_handle": "hawa-mahal-art",
    },
    {
        "key": "hoi_an",
        "name": "Hoi An Ancient Town",
        "location": "Quang Nam Province",
        "country": "Vietnam",
        "year": "1500",
        "description": (
            "Hoi An is a beautifully preserved Southeast Asian trading port dating from the 15th to "
            "19th centuries, where Chinese, Japanese, and European influences blend in a unique "
            "architectural tapestry. Its lantern-lit streets, ancient merchant houses, and covered "
            "bridges make it one of Vietnam's most enchanting destinations."
        ),
        "fun_facts": [
            "Every month on the 14th day of the lunar calendar, Hoi An holds its famous Lantern Festival — electric lights are turned off and the entire ancient town is illuminated by thousands of colorful silk lanterns and candles.",
            "The Japanese Covered Bridge was built in the 1590s by Japanese traders and features a small temple inside dedicated to the weather god.",
            "Hoi An is famous for its lightning-fast tailors who can create custom-made clothing overnight, attracting visitors from around the world.",
        ],
        "collection_handle": "hoi-an-ancient-town-art",
    },
    {
        "key": "milford_sound",
        "name": "Milford Sound",
        "location": "Fiordland, South Island",
        "country": "New Zealand",
        "year": "12,000 BC",
        "description": (
            "Milford Sound is a dramatic fiord in southwestern New Zealand carved by glaciers over "
            "thousands of years, surrounded by sheer rock faces rising over 1,200 meters from the dark "
            "waters below. Rudyard Kipling called it the 'eighth wonder of the world,' and its "
            "untouched wilderness remains one of Earth's most spectacular natural landscapes."
        ),
        "fun_facts": [
            "Milford Sound receives about 7 meters of rainfall per year, making it one of the wettest places on Earth — the rain creates dozens of temporary waterfalls cascading down the cliff faces.",
            "Despite its name, Milford Sound is technically a fiord (carved by glaciers) rather than a sound (carved by rivers).",
            "The fiord is home to a permanent population of bottlenose dolphins, fur seals, and Fiordland crested penguins, one of the world's rarest penguin species.",
        ],
        "collection_handle": "milford-sound-art",
    },
    {
        "key": "mont_saint_michel",
        "name": "Mont Saint-Michel",
        "location": "Normandy",
        "country": "France",
        "year": "708",
        "description": (
            "Mont Saint-Michel is a tidal island topped by a medieval abbey that rises dramatically "
            "from the flat surrounding bay in Normandy. First established as a monastery in 708 AD, "
            "this gravity-defying marvel of medieval architecture appears to float above the water "
            "at high tide and has drawn pilgrims for over a thousand years."
        ),
        "fun_facts": [
            "The tides around Mont Saint-Michel are among the strongest in Europe, with water levels rising up to 14 meters — at high tide the island is completely surrounded, and at low tide you can walk across the sand.",
            "During the Hundred Years' War, Mont Saint-Michel was the only place in Normandy that never fell to the English, despite repeated sieges.",
            "The abbey's spire is topped by a gilded statue of the Archangel Michael slaying a dragon, which stands 170 meters above sea level.",
        ],
        "collection_handle": "mont-saint-michel-art",
    },
    {
        "key": "moraine_lake",
        "name": "Moraine Lake",
        "location": "Banff National Park",
        "country": "Canada",
        "year": "10,000 BC",
        "description": (
            "Moraine Lake is a glacially fed lake in the Valley of the Ten Peaks in Banff National "
            "Park, famous for its impossibly vivid turquoise color. Surrounded by towering Rocky "
            "Mountain peaks, its stunning beauty once graced the Canadian twenty-dollar bill and "
            "remains one of the most photographed landscapes in North America."
        ),
        "fun_facts": [
            "The lake's intense turquoise color comes from glacial rock flour — fine particles of rock ground by glaciers that refract light and create the striking blue-green hue.",
            "The view from the Rock Pile at the lake's edge appeared on the back of the Canadian twenty-dollar bill from 1969 to 1979.",
            "Moraine Lake sits at an elevation of 1,884 meters and is frozen over for most of the year — the road to the lake is typically only open from late May to early October.",
        ],
        "collection_handle": "moraine-lake-art",
    },
    {
        "key": "nyhavn",
        "name": "Nyhavn",
        "location": "Copenhagen",
        "country": "Denmark",
        "year": "1673",
        "description": (
            "Nyhavn is a colorful 17th-century waterfront canal district in Copenhagen lined with "
            "brightly painted townhouses, historic wooden ships, and bustling restaurants. Originally "
            "a busy commercial port, it has become Copenhagen's most iconic postcard image and a "
            "beloved gathering place for locals and visitors alike."
        ),
        "fun_facts": [
            "Hans Christian Andersen lived at three different addresses in Nyhavn — numbers 18, 20, and 67 — and wrote some of his most famous fairy tales there.",
            "The colorful buildings were originally painted in bright hues so sailors returning from sea could easily spot Nyhavn from a distance.",
            "Nyhavn literally means 'New Harbor' — it was dug by Swedish prisoners of war between 1670 and 1673 to connect the King's New Square to the harbor.",
        ],
        "collection_handle": "nyhavn-art",
    },
    {
        "key": "plitvice_lakes",
        "name": "Plitvice Lakes",
        "location": "Lika-Senj County",
        "country": "Croatia",
        "year": "Ancient",
        "description": (
            "Plitvice Lakes National Park is a cascading series of 16 terraced lakes connected by "
            "waterfalls and set within a dense primeval forest in central Croatia. The lakes shift "
            "in color from azure to green to grey depending on mineral content and sunlight, "
            "creating one of Europe's most otherworldly natural landscapes."
        ),
        "fun_facts": [
            "The travertine barriers that create the terraced lakes grow at a rate of about 1 centimeter per year through the deposition of calcium carbonate from the water.",
            "Swimming in the lakes has been banned since 2006 to protect the delicate ecosystem, though the crystal-clear water makes it extremely tempting.",
            "The park is home to European brown bears, wolves, and lynx — it is one of the last places in Europe where all three large predators coexist.",
        ],
        "collection_handle": "plitvice-lakes-art",
    },
    {
        "key": "ponte_vecchio",
        "name": "Ponte Vecchio",
        "location": "Florence",
        "country": "Italy",
        "year": "1345",
        "description": (
            "Ponte Vecchio is a medieval stone bridge over the Arno River in Florence, famous for "
            "the shops built along its entire length. Originally home to butchers and tanners, "
            "it has housed jewelers and goldsmiths since the 16th century and is the only bridge "
            "in Florence to survive World War II intact."
        ),
        "fun_facts": [
            "In 1593, Grand Duke Ferdinand I banned butchers from the bridge due to the smell and replaced them with goldsmiths and jewelers, who remain to this day.",
            "The Vasari Corridor, a secret elevated passageway, runs above the shops on the bridge connecting the Palazzo Vecchio to the Pitti Palace, allowing the Medici family to cross without mingling with commoners.",
            "During the German retreat in 1944, Hitler specifically ordered that Ponte Vecchio be spared from destruction, though all other bridges in Florence were blown up.",
        ],
        "collection_handle": "ponte-vecchio-art",
    },
    {
        "key": "rialto_bridge",
        "name": "Rialto Bridge",
        "location": "Venice",
        "country": "Italy",
        "year": "1591",
        "description": (
            "The Rialto Bridge is the oldest and most famous of the four bridges spanning Venice's "
            "Grand Canal, an elegant stone arch supporting rows of shops on either side. Designed "
            "by Antonio da Ponte, it replaced a series of wooden bridges and has served as the "
            "commercial heart of Venice for over four centuries."
        ),
        "fun_facts": [
            "Michelangelo and Andrea Palladio both submitted designs for the bridge, but the commission went to the lesser-known Antonio da Ponte, whose surname fittingly means 'bridge.'",
            "The single stone arch spans 28.8 meters and was considered a remarkable engineering feat — many critics predicted it would collapse, but it has stood for over 430 years.",
            "The bridge was the only way to cross the Grand Canal on foot for nearly 300 years, until the Ponte dell'Accademia was built in 1854.",
        ],
        "collection_handle": "rialto-bridge-art",
    },
    {
        "key": "rijksmuseum",
        "name": "Rijksmuseum",
        "location": "Amsterdam",
        "country": "Netherlands",
        "year": "1885",
        "description": (
            "The Rijksmuseum is the Netherlands' national museum dedicated to Dutch art and history, "
            "housed in a grand Gothic and Renaissance revival building designed by Pierre Cuypers. "
            "Home to masterpieces by Rembrandt, Vermeer, and other Dutch Golden Age painters, it is "
            "the most visited museum in the Netherlands."
        ),
        "fun_facts": [
            "Rembrandt's 'The Night Watch' has its own dedicated gallery and is the museum's most famous work — at 3.6 by 4.4 meters, it was actually trimmed to fit a previous location.",
            "A public road and bicycle path runs directly through the building's arched passageway, making it the only major museum in the world you can cycle through.",
            "The museum underwent a massive ten-year renovation completed in 2013 at a cost of 375 million euros, restoring the building to Cuypers' original vision.",
        ],
        "collection_handle": "rijksmuseum-art",
    },
    {
        "key": "temple_bar",
        "name": "Temple Bar District",
        "location": "Dublin",
        "country": "Ireland",
        "year": "1600",
        "description": (
            "Temple Bar is Dublin's cultural quarter, a lively cobblestoned neighborhood on the south "
            "bank of the River Liffey packed with pubs, galleries, street performers, and colorful "
            "storefronts. Named after Sir William Temple who owned land here in the 1600s, it is "
            "the social heart of Dublin and Ireland's most famous nightlife district."
        ),
        "fun_facts": [
            "Temple Bar was nearly demolished in the 1980s to make way for a bus depot — the cheap rents during the planning period attracted artists and musicians who gave it the bohemian character it has today.",
            "The area has nothing to do with drinking establishments — 'bar' comes from a riverside walkway, and 'Temple' from the Temple family who lived nearby.",
            "Temple Bar hosts Dublin's oldest outdoor food market every Saturday and a book market every weekend at Temple Bar Square.",
        ],
        "collection_handle": "temple-bar-district-art",
    },
    {
        "key": "twelve_apostles",
        "name": "Twelve Apostles",
        "location": "Great Ocean Road, Victoria",
        "country": "Australia",
        "year": "20 million years ago",
        "description": (
            "The Twelve Apostles are a collection of limestone sea stacks rising dramatically from "
            "the Southern Ocean along Victoria's Great Ocean Road. Formed by millions of years of "
            "erosion by wind and waves, these towering pillars stand up to 45 meters tall and are "
            "one of Australia's most visited natural landmarks."
        ),
        "fun_facts": [
            "Despite the name, there were never actually twelve stacks — when they were named in the 1960s there were nine, and as of 2024 only seven remain after ongoing erosion caused collapses.",
            "The stacks were originally called 'The Sow and Piglets' until the name was changed to the more tourist-friendly 'Twelve Apostles' in 1922.",
            "The limestone cliffs erode at a rate of about 2 centimeters per year, and new stacks are constantly being formed as headlands are gradually worn away.",
        ],
        "collection_handle": "twelve-apostles-art",
    },
    {
        "key": "zanzibar_stone_town",
        "name": "Zanzibar Stone Town",
        "location": "Zanzibar Island",
        "country": "Tanzania",
        "year": "1800s",
        "description": (
            "Stone Town is the historic heart of Zanzibar City, a labyrinth of narrow alleys, "
            "ornately carved wooden doors, and coral stone buildings reflecting centuries of "
            "African, Arab, Indian, and European influence. Once the center of the East African "
            "spice and slave trades, this UNESCO World Heritage Site is one of the most culturally "
            "rich urban areas in Africa."
        ),
        "fun_facts": [
            "Stone Town has over 500 intricately carved wooden doors, many featuring brass studs originally designed to protect against elephant attacks in India — the tradition was carried over by Indian traders.",
            "Freddie Mercury, the legendary Queen frontman, was born in Stone Town in 1946 as Farrokh Bulsara — his childhood home is now a small museum.",
            "Zanzibar was once the world's largest producer of cloves, and the spice trade that made the island wealthy still perfumes the air throughout Stone Town's markets.",
        ],
        "collection_handle": "zanzibar-stone-town-art",
    },
    # ----- Phase 3 Landmarks -----
    {
        "key": "pyramids_giza",
        "name": "Pyramids of Giza",
        "location": "Giza",
        "country": "Egypt",
        "year": "2560 BC",
        "description": (
            "The Pyramids of Giza are a complex of three ancient Egyptian pyramids on the Giza "
            "plateau outside Cairo, built as monumental tombs for the pharaohs Khufu, Khafre, and "
            "Menkaure. The Great Pyramid of Khufu, the oldest and largest, is the only surviving "
            "wonder of the original Seven Wonders of the Ancient World."
        ),
        "fun_facts": [
            "The Great Pyramid stood as the tallest man-made structure in the world for over 3,800 years, from its completion around 2560 BC until the Lincoln Cathedral spire surpassed it around 1311 AD.",
            "An estimated 2.3 million limestone blocks, each weighing an average of 2.5 tons, were used to build the Great Pyramid — and they fit together so precisely that a sheet of paper cannot be inserted between them.",
            "The Great Pyramid was originally covered in smooth white Tura limestone casing stones that made it gleam in the sun; most were stripped away over the centuries for use in other buildings.",
        ],
        "collection_handle": "pyramids-giza-art",
    },
    {
        "key": "table_mountain",
        "name": "Table Mountain",
        "location": "Cape Town",
        "country": "South Africa",
        "year": "600 million years ago",
        "description": (
            "Table Mountain is a flat-topped mountain overlooking Cape Town, one of the oldest "
            "mountains on Earth with rocks dating back approximately 600 million years. Its "
            "distinctive flat summit stretches roughly 3 kilometers from side to side and is "
            "a UNESCO World Heritage Site and one of the New7Wonders of Nature."
        ),
        "fun_facts": [
            "Table Mountain is home to over 1,470 plant species, more than the entire United Kingdom, and many are found nowhere else on Earth.",
            "The famous 'tablecloth' cloud that drapes over the mountain's summit is formed when moist air from the southeast is pushed up and over the flat top, condensing as it rises.",
            "The first known ascent of Table Mountain was recorded in 1503 by Portuguese sailor Antonio de Saldanha, making it one of the earliest recorded mountain climbs.",
        ],
        "collection_handle": "table-mountain-art",
    },
    {
        "key": "victoria_falls",
        "name": "Victoria Falls",
        "location": "Livingstone",
        "country": "Zambia/Zimbabwe",
        "year": "Ancient",
        "description": (
            "Victoria Falls is the world's largest sheet of falling water, spanning 1,708 meters "
            "wide and plunging 108 meters into the Batoka Gorge on the border of Zambia and "
            "Zimbabwe. Known locally as Mosi-oa-Tunya, meaning 'The Smoke That Thunders,' its "
            "spray can be seen from over 50 kilometers away."
        ),
        "fun_facts": [
            "Scottish explorer David Livingstone became the first European to see the falls in 1855 and named them after Queen Victoria, though the indigenous Kololo people had long called them Mosi-oa-Tunya.",
            "During peak flood season, over 500 million liters of water plunge over the edge every minute, creating a spray column that rises over 400 meters into the air.",
            "Devil's Pool, a natural rock pool at the very edge of the falls on the Zambian side, allows swimmers to wade to the precipice during low-water season without being swept over.",
        ],
        "collection_handle": "victoria-falls-art",
    },
    {
        "key": "djemaa_el_fna",
        "name": "Djemaa el-Fna",
        "location": "Marrakech",
        "country": "Morocco",
        "year": "1050",
        "description": (
            "Djemaa el-Fna is a vast open square and marketplace in the heart of Marrakech's "
            "medina, a swirling spectacle of storytellers, musicians, snake charmers, acrobats, "
            "and food stalls that has served as the city's main gathering place for nearly a "
            "thousand years. UNESCO recognized it as a Masterpiece of the Oral and Intangible "
            "Heritage of Humanity in 2001."
        ),
        "fun_facts": [
            "The square's name likely translates to 'Assembly of the Dead,' possibly referring to its historical use as a place where the heads of executed criminals were displayed.",
            "Every evening the square transforms completely as over 100 food stalls are assembled from scratch, creating one of the largest open-air restaurants in the world.",
            "UNESCO's recognition of Djemaa el-Fna in 2001 was groundbreaking — it was one of the first places honored specifically for its living cultural traditions rather than physical structures.",
        ],
        "collection_handle": "djemaa-el-fna-art",
    },
    {
        "key": "lalibela_churches",
        "name": "Rock-Hewn Churches of Lalibela",
        "location": "Lalibela",
        "country": "Ethiopia",
        "year": "1200",
        "description": (
            "The Rock-Hewn Churches of Lalibela are eleven medieval monolithic churches carved "
            "directly out of solid volcanic rock in the highlands of northern Ethiopia. Commissioned "
            "by King Lalibela in the 12th and 13th centuries as a 'New Jerusalem,' they remain active "
            "places of worship and one of the most extraordinary architectural achievements in human history."
        ),
        "fun_facts": [
            "Each church was carved from the top down out of a single block of rock, meaning the builders had to envision the entire structure before making a single cut — one mistake could ruin years of work.",
            "The most famous church, Bete Giyorgis (Church of St. George), is carved in the shape of a cross and sits 12 meters below ground level in its own excavated courtyard.",
            "An elaborate system of drainage ditches, tunnels, and ceremonial passages connects the churches underground, all carved from the same living rock.",
        ],
        "collection_handle": "lalibela-churches-art",
    },
    {
        "key": "serengeti",
        "name": "Serengeti",
        "location": "Mara and Simiyu Regions",
        "country": "Tanzania",
        "year": "Ancient",
        "description": (
            "The Serengeti is a vast ecosystem spanning roughly 30,000 square kilometers of "
            "grassland plains and savanna in northern Tanzania, home to the largest terrestrial "
            "mammal migration on Earth. Each year, over 1.5 million wildebeest and hundreds of "
            "thousands of zebras and gazelles undertake a circular migration following the rains."
        ),
        "fun_facts": [
            "The Great Migration involves roughly 1.5 million wildebeest, 500,000 zebras, and 300,000 gazelles traveling in a continuous loop of about 800 kilometers throughout the year.",
            "The name 'Serengeti' comes from the Maasai word 'siringet,' meaning 'endless plains' — and the flat grasslands stretch to the horizon in every direction.",
            "The Serengeti has one of the highest concentrations of large predators in Africa, with approximately 3,000 lions, 1,000 leopards, and 8,000 hyenas.",
        ],
        "collection_handle": "serengeti-art",
    },
    {
        "key": "borobudur",
        "name": "Borobudur Temple",
        "location": "Central Java",
        "country": "Indonesia",
        "year": "825",
        "description": (
            "Borobudur is the world's largest Buddhist temple, a massive 9th-century monument "
            "in Central Java built in the shape of a giant mandala when viewed from above. "
            "Constructed with approximately 2 million blocks of volcanic stone, it features "
            "2,672 relief panels and 504 Buddha statues arranged across nine stacked platforms."
        ),
        "fun_facts": [
            "Borobudur was abandoned in the 14th century after the decline of Hindu-Buddhist kingdoms in Java and the spread of Islam, and lay hidden under volcanic ash and jungle growth for centuries until its rediscovery by the British in 1814.",
            "The temple's 2,672 carved relief panels, if laid end to end, would stretch nearly 6 kilometers, making it the largest and most complete ensemble of Buddhist reliefs in the world.",
            "The entire structure is designed as a Buddhist cosmological map — pilgrims walk through three levels representing the world of desire, the world of forms, and the world of formlessness on their path to enlightenment.",
        ],
        "collection_handle": "borobudur-art",
    },
    {
        "key": "terracotta_warriors",
        "name": "Terracotta Warriors",
        "location": "Xi'an",
        "country": "China",
        "year": "210 BC",
        "description": (
            "The Terracotta Warriors are a collection of over 8,000 life-sized clay soldiers, "
            "horses, and chariots buried with China's first emperor, Qin Shi Huang, to protect "
            "him in the afterlife. Discovered by farmers digging a well in 1974, the army had "
            "lain hidden underground for over two thousand years near the city of Xi'an."
        ),
        "fun_facts": [
            "No two terracotta warriors are alike — each of the estimated 8,000 figures has a unique face, hairstyle, and expression, believed to have been modeled after real soldiers in the emperor's army.",
            "The warriors were originally painted in vivid colors including red, blue, green, and purple, but the pigments oxidize and fade within minutes of being exposed to air during excavation.",
            "The farmer who discovered the warriors in 1974, Yang Zhifa, was reportedly paid about 10 yuan (roughly $1.50) for the initial find; the site is now one of China's most visited attractions.",
        ],
        "collection_handle": "terracotta-warriors-art",
    },
    {
        "key": "golden_temple_amritsar",
        "name": "Golden Temple",
        "location": "Amritsar",
        "country": "India",
        "year": "1604",
        "description": (
            "The Golden Temple, or Sri Harmandir Sahib, is the holiest shrine in Sikhism, a "
            "stunning gilded temple set in the middle of a sacred pool in Amritsar, Punjab. "
            "Founded in 1604 by the fifth Sikh Guru, Guru Arjan, its gold-plated upper floors "
            "and marble lower walls shimmer in reflection on the surrounding water."
        ),
        "fun_facts": [
            "The Golden Temple's community kitchen, called the Langar, serves free meals to over 100,000 people every day regardless of religion, caste, or background, making it the largest free kitchen in the world.",
            "The temple has four entrances, one on each side, symbolizing the openness of Sikhism to all people from all directions and all walks of life.",
            "The temple's upper floors are covered with approximately 750 kilograms of pure gold, which was applied during the reign of Maharaja Ranjit Singh in the early 19th century.",
        ],
        "collection_handle": "golden-temple-amritsar-art",
    },
    {
        "key": "petronas_towers",
        "name": "Petronas Towers",
        "location": "Kuala Lumpur",
        "country": "Malaysia",
        "year": "1998",
        "description": (
            "The Petronas Towers are twin supertall skyscrapers in Kuala Lumpur that held the "
            "record as the world's tallest buildings from 1998 to 2004. Standing 451.9 meters "
            "tall with 88 floors each, they remain the tallest twin towers in the world and are "
            "connected by a sky bridge at the 41st and 42nd floors."
        ),
        "fun_facts": [
            "The towers' floor plan is based on an eight-pointed star, a motif found throughout Islamic art and architecture, reflecting Malaysia's Muslim heritage.",
            "Each tower was built by a different construction company — one South Korean and one Japanese — creating an unusual competition where both teams raced to complete their tower first.",
            "The sky bridge connecting the two towers at 170 meters above ground is not fixed to both towers — it rests on spherical bearings that allow it to slide in and out as the towers sway independently in the wind.",
        ],
        "collection_handle": "petronas-towers-art",
    },
    {
        "key": "halong_bay",
        "name": "Ha Long Bay",
        "location": "Quang Ninh Province",
        "country": "Vietnam",
        "year": "Ancient",
        "description": (
            "Ha Long Bay is a UNESCO World Heritage Site in northeastern Vietnam featuring nearly "
            "2,000 limestone karst islands and islets rising dramatically from emerald waters. "
            "The name translates to 'Descending Dragon Bay,' and its otherworldly seascape of "
            "towering pillars, hidden caves, and floating fishing villages is one of Southeast "
            "Asia's most iconic landscapes."
        ),
        "fun_facts": [
            "According to Vietnamese legend, the islands were created when a family of dragons sent by the gods spat out jewels and jade to form a barrier against coastal invaders.",
            "Ha Long Bay contains several large caves, including Sung Sot (Surprise) Cave, which has two enormous chambers and can accommodate thousands of visitors at once.",
            "Hundreds of people still live on the bay in floating fishing villages, some of which have existed for generations, though the Vietnamese government has been relocating residents to the mainland.",
        ],
        "collection_handle": "halong-bay-art",
    },
    {
        "key": "sigiriya",
        "name": "Sigiriya",
        "location": "Central Province",
        "country": "Sri Lanka",
        "year": "477",
        "description": (
            "Sigiriya is a massive column of rock nearly 200 meters tall topped with the ruins "
            "of an ancient palace and fortress in central Sri Lanka. Built by King Kashyapa I in "
            "the 5th century AD, this UNESCO World Heritage Site features elaborate frescoes, "
            "a mirror wall, and a monumental lion gate carved into the rock face."
        ),
        "fun_facts": [
            "The entrance to the palace was carved in the shape of an enormous lion — visitors walked through the lion's open mouth to reach the stairway, though only the giant paws survive today.",
            "Sigiriya's famous frescoes depict celestial maidens and are painted in a sheltered pocket of the rock face; originally there may have been as many as 500, but only 22 survive.",
            "The mirror wall was originally polished so highly that the king could see his reflection as he walked past; centuries of visitors have scratched graffiti into it, some dating back to the 8th century.",
        ],
        "collection_handle": "sigiriya-art",
    },
    {
        "key": "potala_palace",
        "name": "Potala Palace",
        "location": "Lhasa",
        "country": "Tibet/China",
        "year": "1649",
        "description": (
            "The Potala Palace is a towering fortress-like structure perched atop Marpo Ri hill "
            "in Lhasa, Tibet, at an altitude of 3,700 meters. Originally built in the 7th century "
            "and massively expanded by the fifth Dalai Lama in the 17th century, it served as the "
            "winter residence of the Dalai Lamas and the seat of Tibetan government for centuries."
        ),
        "fun_facts": [
            "The palace contains over 1,000 rooms, 10,000 shrines, and approximately 200,000 statues spread across its 13 stories, making it one of the largest ancient palaces in the world.",
            "The White Palace served as the living quarters and administrative offices, while the Red Palace at the center contains chapels, libraries, and the gilded funeral stupas of eight Dalai Lamas.",
            "The foundations of the palace include copper poured into the bedrock to help protect it from earthquakes — a remarkably advanced engineering technique for the 17th century.",
        ],
        "collection_handle": "potala-palace-art",
    },
    {
        "key": "meiji_shrine",
        "name": "Meiji Shrine",
        "location": "Tokyo",
        "country": "Japan",
        "year": "1920",
        "description": (
            "Meiji Shrine is a Shinto shrine in Tokyo dedicated to the deified spirits of Emperor "
            "Meiji and Empress Shoken, set within a 70-hectare forest of 120,000 trees in the heart "
            "of the city. Completed in 1920, it is one of Japan's most visited shrines, attracting "
            "over 3 million worshippers during the first three days of each new year."
        ),
        "fun_facts": [
            "The shrine's surrounding forest was artificially created by planting 120,000 trees donated from all over Japan, and was designed to become a self-sustaining old-growth forest — which it now is, over a century later.",
            "The massive torii gate at the shrine's entrance is 12 meters tall and made from 1,500-year-old Japanese cypress trees from a forest in Taiwan.",
            "The original shrine was destroyed by Allied air raids in 1945 during World War II and was rebuilt in 1958 using funds raised through a public fundraising campaign.",
        ],
        "collection_handle": "meiji-shrine-art",
    },
    {
        "key": "gyeongbokgung",
        "name": "Gyeongbokgung Palace",
        "location": "Seoul",
        "country": "South Korea",
        "year": "1395",
        "description": (
            "Gyeongbokgung is the largest and most iconic of Seoul's Five Grand Palaces, built "
            "in 1395 as the main royal palace of the Joseon dynasty. Its name means 'Palace Greatly "
            "Blessed by Heaven,' and its sprawling complex of halls, pavilions, and gardens served "
            "as the political center of Korea for five centuries."
        ),
        "fun_facts": [
            "The palace was almost entirely destroyed during the Japanese invasions of 1592 and lay in ruins for nearly 300 years before being rebuilt in 1867 by the regent Heungseon Daewongun.",
            "The Gyeonghoeru Pavilion, a grand banquet hall set on 48 stone pillars over an artificial lake, is one of the most photographed structures in South Korea.",
            "Visitors can rent traditional Korean hanbok clothing near the palace and receive free admission when wearing it, making it one of the most popular cultural experiences in Seoul.",
        ],
        "collection_handle": "gyeongbokgung-art",
    },
    {
        "key": "zhangjiajie",
        "name": "Zhangjiajie",
        "location": "Hunan Province",
        "country": "China",
        "year": "Ancient",
        "description": (
            "Zhangjiajie National Forest Park is famous for its towering sandstone pillar formations, "
            "some rising over 200 meters above the subtropical forest floor. These dramatic quartzite "
            "sandstone columns, formed by millions of years of erosion, inspired the floating "
            "mountains in the film Avatar and are part of the Wulingyuan Scenic Area UNESCO World "
            "Heritage Site."
        ),
        "fun_facts": [
            "The tallest pillar, the Southern Sky Column standing at 1,080 meters, was officially renamed 'Avatar Hallelujah Mountain' in 2010 after inspiring the floating mountains in James Cameron's film.",
            "The park's glass-bottomed Zhangjiajie Grand Canyon Bridge spans 430 meters at a height of 300 meters above the canyon floor, making it one of the highest and longest glass bridges in the world.",
            "The pillar formations were created over 300 million years as physical and chemical erosion widened cracks in the sandstone, eventually isolating individual columns from the plateau above.",
        ],
        "collection_handle": "zhangjiajie-art",
    },
    {
        "key": "acropolis_athens",
        "name": "Acropolis of Athens",
        "location": "Athens",
        "country": "Greece",
        "year": "447 BC",
        "description": (
            "The Acropolis of Athens is an ancient citadel perched on a rocky outcrop above the "
            "city, crowned by the Parthenon and several other temples from the 5th century BC. "
            "Built during the Golden Age of Athens under the leadership of Pericles, it represents "
            "the pinnacle of classical Greek architecture and the birthplace of Western civilization."
        ),
        "fun_facts": [
            "The Parthenon's columns appear perfectly straight but are actually slightly curved — this optical illusion, called entasis, was deliberately designed to make the building appear more symmetrical to the human eye.",
            "Lord Elgin controversially removed about half of the Parthenon's surviving sculptures in the early 1800s and sold them to the British Museum, where they remain a subject of heated repatriation debate.",
            "The Parthenon has served as a Greek temple, a Christian church, an Ottoman mosque, and an ammunition depot — it was largely intact until 1687, when a Venetian bombardment ignited Ottoman gunpowder stored inside.",
        ],
        "collection_handle": "acropolis-athens-art",
    },
    {
        "key": "blue_mosque",
        "name": "Blue Mosque",
        "location": "Istanbul",
        "country": "Turkey",
        "year": "1616",
        "description": (
            "The Blue Mosque, officially the Sultan Ahmed Mosque, is an Ottoman-era imperial mosque "
            "in Istanbul renowned for its six minarets and interior adorned with over 20,000 "
            "handmade Iznik ceramic tiles in blue floral patterns. Built between 1609 and 1616 for "
            "Sultan Ahmed I, it remains an active mosque and one of Istanbul's most visited landmarks."
        ),
        "fun_facts": [
            "The mosque has six minarets, which caused controversy at the time because only the mosque in Mecca had six — Sultan Ahmed resolved this by funding the construction of a seventh minaret at Mecca.",
            "The interior is decorated with more than 20,000 handmade Iznik tiles featuring tulips, carnations, and roses in over 50 different patterns, all in the blue tones that give the mosque its popular name.",
            "The mosque was built directly opposite Hagia Sophia as a deliberate architectural challenge, and the two face each other across a garden in one of the world's most famous religious skylines.",
        ],
        "collection_handle": "blue-mosque-art",
    },
    {
        "key": "duomo_florence",
        "name": "Florence Cathedral",
        "location": "Florence",
        "country": "Italy",
        "year": "1436",
        "description": (
            "The Florence Cathedral, or Cattedrale di Santa Maria del Fiore, is crowned by "
            "Filippo Brunelleschi's iconic dome, the largest masonry dome ever constructed. "
            "Begun in 1296 in the Gothic style and structurally completed in 1436, its "
            "terracotta-tiled dome dominates the Florence skyline and remains an engineering "
            "marvel of the Renaissance."
        ),
        "fun_facts": [
            "Brunelleschi's dome was built without a temporary wooden support frame, which was considered impossible at the time — he invented a herringbone brick pattern and custom hoisting machines to accomplish the feat.",
            "The dome is actually two shells, one nested inside the other, with a staircase of 463 steps between them leading to the lantern at the top.",
            "The cathedral's facade was not completed until 1887, over 400 years after the rest of the building, when a neo-Gothic marble facade was finally added in white, green, and pink Tuscan marble.",
        ],
        "collection_handle": "duomo-florence-art",
    },
    {
        "key": "tower_of_london",
        "name": "Tower of London",
        "location": "London",
        "country": "England",
        "year": "1066",
        "description": (
            "The Tower of London is a historic castle and fortress on the north bank of the "
            "Thames, founded by William the Conqueror in 1066. Over its nearly 1,000-year "
            "history, it has served as a royal palace, prison, armory, treasury, and menagerie, "
            "and today houses the Crown Jewels of England."
        ),
        "fun_facts": [
            "At least six ravens are kept at the Tower at all times because of a legend that if the ravens ever leave, the kingdom will fall — the Ravenmaster clips one wing of each bird to prevent them from flying away.",
            "The Tower housed a royal menagerie for over 600 years beginning in the 13th century, including lions, an elephant, and a polar bear that was allowed to fish in the Thames on a long leash.",
            "Anne Boleyn, Catherine Howard, Lady Jane Grey, and Sir Walter Raleigh are among the famous prisoners who were held or executed at the Tower.",
        ],
        "collection_handle": "tower-of-london-art",
    },
    {
        "key": "santorini",
        "name": "Santorini",
        "location": "Cyclades",
        "country": "Greece",
        "year": "3000 BC",
        "description": (
            "Santorini is a crescent-shaped volcanic island in the Aegean Sea, famous for its "
            "dramatic caldera views, white-washed buildings with blue-domed churches, and "
            "spectacular sunsets. The island was shaped by one of the largest volcanic eruptions "
            "in recorded history around 1600 BC, which may have contributed to the decline of "
            "the Minoan civilization."
        ),
        "fun_facts": [
            "The Minoan eruption of Thera around 1600 BC was one of the most powerful volcanic events in human history, ejecting about 60 cubic kilometers of material and potentially inspiring the legend of Atlantis.",
            "Santorini's iconic blue-domed churches were originally painted blue because the pigment was the cheapest available — the color has since become the island's defining aesthetic.",
            "The island's unique volcanic soil produces distinctive wines, especially Assyrtiko, and the vines are trained into basket shapes called kouloura to protect them from the island's fierce winds.",
        ],
        "collection_handle": "santorini-art",
    },
    {
        "key": "dubrovnik_walls",
        "name": "Dubrovnik Old Town",
        "location": "Dubrovnik",
        "country": "Croatia",
        "year": "1272",
        "description": (
            "Dubrovnik's Old Town is a remarkably preserved medieval walled city on the Adriatic "
            "coast, encircled by massive stone walls up to 25 meters high and 6 meters thick. "
            "Known as the 'Pearl of the Adriatic,' it served as the capital of the Republic of "
            "Ragusa, a maritime trading power that rivaled Venice for centuries."
        ),
        "fun_facts": [
            "Dubrovnik established one of the world's first quarantine systems in 1377, requiring arriving ships to isolate for 30 days on a nearby island before entering the city — the word 'quarantine' derives from a similar Italian practice.",
            "The city walls run almost 2 kilometers around the entire Old Town and have never been breached by a hostile army throughout their history.",
            "Dubrovnik gained worldwide fame as the filming location for King's Landing in the HBO series Game of Thrones, leading to a massive surge in tourism.",
        ],
        "collection_handle": "dubrovnik-walls-art",
    },
    {
        "key": "rothenburg",
        "name": "Rothenburg ob der Tauber",
        "location": "Bavaria",
        "country": "Germany",
        "year": "1170",
        "description": (
            "Rothenburg ob der Tauber is a medieval walled town in Bavaria that has preserved "
            "its half-timbered houses, cobblestone streets, and complete town wall since the "
            "Middle Ages. Often called the best-preserved medieval town in Germany, it looks "
            "virtually unchanged since the 17th century and epitomizes the fairy-tale German village."
        ),
        "fun_facts": [
            "The town was saved during the Thirty Years' War by a legendary drinking feat — in 1631, the mayor supposedly drank a 3.25-liter tankard of wine in one draught, persuading the conquering general to spare the town.",
            "Rothenburg is home to the Kathe Wohlfahrt Christmas store, which is open year-round and is one of the world's largest permanent Christmas decoration shops.",
            "Much of the Old Town was damaged by Allied bombing in 1945, but it was meticulously restored to its original medieval appearance using surviving records and photographs, partly funded by donations from the United States.",
        ],
        "collection_handle": "rothenburg-art",
    },
    {
        "key": "seville_alcazar",
        "name": "Royal Alcazar of Seville",
        "location": "Seville",
        "country": "Spain",
        "year": "913",
        "description": (
            "The Royal Alcazar of Seville is a stunning palace complex originally built as a "
            "Moorish fort in the 10th century and expanded over successive centuries by both "
            "Muslim and Christian rulers. Its blend of Mudejar, Gothic, Renaissance, and Baroque "
            "architecture makes it one of the most beautiful palaces in Europe and the oldest "
            "royal palace still in active use."
        ),
        "fun_facts": [
            "The Alcazar is the oldest royal palace still in use in Europe — the Spanish royal family continues to use the upper floors as their official Seville residence when visiting the city.",
            "King Pedro I of Castile employed Moorish craftsmen from Granada to build the Palace of King Don Pedro in 1364, creating a masterpiece of Mudejar architecture that rivals the Alhambra.",
            "The Alcazar's lush gardens and ornate rooms were used as filming locations for the Water Gardens of Dorne in Game of Thrones.",
        ],
        "collection_handle": "seville-alcazar-art",
    },
    {
        "key": "matterhorn",
        "name": "Matterhorn",
        "location": "Zermatt",
        "country": "Switzerland",
        "year": "Ancient",
        "description": (
            "The Matterhorn is one of the most recognizable mountains in the world, a nearly "
            "symmetrical pyramidal peak rising 4,478 meters on the border of Switzerland and "
            "Italy. Its distinctive shape and near-vertical faces have made it an enduring symbol "
            "of the Alps and one of the deadliest peaks in mountaineering history."
        ),
        "fun_facts": [
            "The first successful ascent was made on July 14, 1865, by Edward Whymper's team, but four of the seven climbers died during the descent when a rope broke — the tragedy made headlines worldwide.",
            "The Toblerone chocolate bar's logo features the Matterhorn, and the mountain's shape has become one of the most commercially used mountain images in the world.",
            "The Matterhorn is actually slowly moving — geological studies show the entire peak sways back and forth roughly once every two seconds due to seismic energy from the ocean and human activity.",
        ],
        "collection_handle": "matterhorn-art",
    },
    {
        "key": "amalfi_coast",
        "name": "Amalfi Coast",
        "location": "Campania",
        "country": "Italy",
        "year": "Ancient",
        "description": (
            "The Amalfi Coast is a 50-kilometer stretch of dramatic coastline along the "
            "Sorrentine Peninsula in southern Italy, with colorful villages clinging to steep "
            "cliffs above the Tyrrhenian Sea. A UNESCO World Heritage Site, its terraced "
            "lemon groves, pastel-painted towns, and winding coastal roads make it one of "
            "the most beautiful coastlines in the Mediterranean."
        ),
        "fun_facts": [
            "The town of Amalfi was once a powerful maritime republic rivaling Venice, Genoa, and Pisa, and its maritime code, the Tabula Amalphitana, governed Mediterranean sea trade for centuries.",
            "Limoncello, the famous Italian lemon liqueur, originated on the Amalfi Coast, where the local Sfusato Amalfitano lemons grow to the size of grapefruits on the steep terraced hillsides.",
            "The main coastal road, SS163, was built by the Bourbon dynasty in the mid-19th century and features over 1,000 dramatic curves with sheer drops to the sea.",
        ],
        "collection_handle": "amalfi-coast-art",
    },
    {
        "key": "trolltunga",
        "name": "Trolltunga",
        "location": "Hordaland",
        "country": "Norway",
        "year": "10,000 years ago",
        "description": (
            "Trolltunga, or 'Troll's Tongue,' is a dramatic piece of rock jutting horizontally "
            "out of a mountain about 700 meters above Lake Ringedalsvatnet in western Norway. "
            "Formed during the last ice age when glacial water froze inside the mountain and "
            "broke away the surrounding rock, it has become one of Norway's most spectacular "
            "and photographed natural landmarks."
        ),
        "fun_facts": [
            "The rock formation extends about 10 meters horizontally from the cliff face and sits roughly 700 meters above the lake below, making it one of the most dramatic cliff viewpoints in the world.",
            "The hike to Trolltunga is approximately 27 kilometers round trip and takes 10 to 12 hours, with an elevation gain of about 800 meters — it is not a casual stroll.",
            "Despite its dramatic appearance and extreme drop, the rock itself is geologically stable and is not in danger of breaking off anytime soon according to Norwegian geological surveys.",
        ],
        "collection_handle": "trolltunga-art",
    },
    {
        "key": "meteora",
        "name": "Meteora",
        "location": "Thessaly",
        "country": "Greece",
        "year": "1300s",
        "description": (
            "Meteora is a rock formation in central Greece where six Eastern Orthodox monasteries "
            "perch atop towering natural sandstone pillars reaching up to 400 meters high. The "
            "monasteries were built between the 14th and 16th centuries by monks seeking spiritual "
            "isolation, and the name Meteora means 'suspended in the air.'"
        ),
        "fun_facts": [
            "The original monks reached the tops of the pillars using removable ladders and later hauled themselves up in large nets suspended from ropes — visitors asked how often the ropes were replaced, and the monks reportedly answered 'when the Lord lets them break.'",
            "Of the 24 monasteries originally built, only six remain active today, inhabited by small communities of monks and nuns.",
            "The sandstone pillars were formed over 60 million years ago when the area was an ancient seabed — tectonic activity pushed the rock upward, and erosion carved the dramatic columns.",
        ],
        "collection_handle": "meteora-art",
    },
    {
        "key": "niagara_falls",
        "name": "Niagara Falls",
        "location": "Ontario/New York",
        "country": "Canada/USA",
        "year": "12,000 years ago",
        "description": (
            "Niagara Falls is a group of three waterfalls straddling the border between Ontario, "
            "Canada, and New York, USA, collectively forming the highest flow rate of any waterfall "
            "in North America. The Horseshoe Falls, the largest of the three, plunges 51 meters "
            "and carries about 90 percent of the water flow."
        ),
        "fun_facts": [
            "Niagara Falls has been slowly eroding and moving upstream — since its formation after the last ice age, the falls have retreated about 11 kilometers from their original position near present-day Queenston.",
            "In 1969, the U.S. Army Corps of Engineers completely diverted the water flow from the American Falls for several months to study the rock face, revealing tons of rock at the base.",
            "Nikola Tesla helped design the first major hydroelectric power plant at Niagara Falls in 1895, which transmitted alternating current electricity to Buffalo, 26 miles away, proving the viability of AC power distribution.",
        ],
        "collection_handle": "niagara-falls-art",
    },
    {
        "key": "chichen_itza",
        "name": "Chichen Itza",
        "location": "Yucatan",
        "country": "Mexico",
        "year": "600 AD",
        "description": (
            "Chichen Itza is a large pre-Columbian archaeological site built by the Maya "
            "civilization on the Yucatan Peninsula, dominated by the iconic step pyramid known "
            "as El Castillo or the Temple of Kukulcan. One of the New Seven Wonders of the World, "
            "it was one of the largest Maya cities and a major focal point of political and "
            "economic activity in the region."
        ),
        "fun_facts": [
            "During the spring and autumn equinoxes, the late afternoon sun casts a series of triangular shadows on the northern stairway of El Castillo that create the illusion of a feathered serpent descending the pyramid.",
            "If you clap your hands at the base of El Castillo, the echo returned sounds remarkably like the call of the quetzal bird, which was sacred to the Maya — though whether this was intentional remains debated.",
            "The Sacred Cenote, a natural sinkhole at the site, was a place of pilgrimage where the Maya deposited offerings including gold, jade, pottery, and human sacrifices to the rain god Chaac.",
        ],
        "collection_handle": "chichen-itza-art",
    },
    {
        "key": "iguazu_falls",
        "name": "Iguazu Falls",
        "location": "Misiones",
        "country": "Argentina/Brazil",
        "year": "Ancient",
        "description": (
            "Iguazu Falls is a vast system of 275 individual waterfalls spanning nearly 3 "
            "kilometers along the border of Argentina and Brazil, surrounded by lush subtropical "
            "rainforest. The largest drop, called the Devil's Throat, is a U-shaped cascade 82 "
            "meters high and 150 meters wide, producing a permanent cloud of mist and rainbows."
        ),
        "fun_facts": [
            "Upon seeing Iguazu Falls, Eleanor Roosevelt reportedly exclaimed 'Poor Niagara!' — Iguazu is about four times wider and carries far more water than its North American counterpart.",
            "The falls are shared between Argentina and Brazil, with Argentina having about 80 percent of the falls and offering close-up walkway views, while Brazil's side provides the sweeping panoramic vista.",
            "The surrounding national parks on both sides protect one of the largest remaining tracts of Atlantic Forest and are home to jaguars, giant anteaters, and over 400 species of birds.",
        ],
        "collection_handle": "iguazu-falls-art",
    },
    {
        "key": "easter_island",
        "name": "Easter Island",
        "location": "Polynesia",
        "country": "Chile",
        "year": "1250",
        "description": (
            "Easter Island, or Rapa Nui, is one of the most remote inhabited islands on Earth, "
            "famous for its 887 monumental stone statues called moai carved by the Rapa Nui "
            "people between the 13th and 16th centuries. These massive figures, some weighing "
            "over 80 tons, stand on stone platforms along the coastline gazing inland to watch "
            "over the villages."
        ),
        "fun_facts": [
            "The moai were carved from compressed volcanic ash at the Rano Raraku quarry, where nearly 400 unfinished statues remain in various stages of completion — the largest unfinished moai would have stood 21 meters tall.",
            "Recent research suggests the moai were 'walked' to their platforms by rocking them side to side using ropes, which aligns with the Rapa Nui oral tradition that the statues 'walked' to their destinations.",
            "Easter Island is one of the most isolated inhabited places on Earth — the nearest inhabited land is Pitcairn Island, over 2,000 kilometers away, with a population of about 50 people.",
        ],
        "collection_handle": "easter-island-art",
    },
    {
        "key": "tikal",
        "name": "Tikal",
        "location": "Peten",
        "country": "Guatemala",
        "year": "400 BC",
        "description": (
            "Tikal is one of the largest and most important archaeological sites of the ancient "
            "Maya civilization, deep within the rainforests of northern Guatemala. At its peak "
            "around 700 AD, Tikal was home to an estimated 100,000 people and featured towering "
            "temple-pyramids rising above the jungle canopy, the tallest reaching 70 meters."
        ),
        "fun_facts": [
            "Temple IV, the tallest structure at Tikal at 70 meters, offers a view above the rainforest canopy that was used as the Rebel base on Yavin 4 in the original Star Wars film.",
            "Tikal was mysteriously abandoned around 900 AD, likely due to a combination of drought, warfare, and environmental degradation, and was swallowed by the jungle for nearly a thousand years.",
            "The site contains over 3,000 structures spread across 16 square kilometers, and archaeologists estimate that only a fraction of the ancient city has been excavated.",
        ],
        "collection_handle": "tikal-art",
    },
    {
        "key": "antelope_canyon",
        "name": "Antelope Canyon",
        "location": "Arizona",
        "country": "USA",
        "year": "Ancient",
        "description": (
            "Antelope Canyon is a slot canyon on Navajo land near Page, Arizona, carved over "
            "millions of years by flash floods and wind erosion into smooth, flowing sandstone "
            "walls. Its narrow passageways, sculpted curves, and beams of light filtering down "
            "from above create one of the most surreal and photographed landscapes in the "
            "American Southwest."
        ),
        "fun_facts": [
            "The canyon is divided into two sections — Upper Antelope Canyon, called Tse bighanilini ('the place where water runs through rocks') by the Navajo, and Lower Antelope Canyon, called Hasdestwazi ('spiral rock arches').",
            "The famous light beams that illuminate the canyon floor in Upper Antelope Canyon only occur between late March and early October when the sun is high enough to penetrate the narrow opening above.",
            "Antelope Canyon can only be visited with a licensed Navajo guide because it sits on Navajo Nation land and is prone to dangerous flash floods, even during clear weather.",
        ],
        "collection_handle": "antelope-canyon-art",
    },
    {
        "key": "monument_valley",
        "name": "Monument Valley",
        "location": "Utah/Arizona",
        "country": "USA",
        "year": "Ancient",
        "description": (
            "Monument Valley is a Navajo Tribal Park on the Utah-Arizona border, defined by "
            "massive sandstone buttes rising 300 meters from the red desert floor. Its iconic "
            "landscape of towering mesas and vast open desert has appeared in countless Western "
            "films and is one of the most recognizable landscapes in the American West."
        ),
        "fun_facts": [
            "Director John Ford used Monument Valley as a filming location in at least nine of his Western films starting with Stagecoach in 1939, establishing it as the quintessential image of the American frontier.",
            "The formations are the remnants of sandstone layers deposited over 250 million years ago — the surrounding softer rock eroded away, leaving the harder buttes and mesas standing.",
            "Monument Valley is not a national park but a Navajo Tribal Park managed by the Navajo Nation, and a 17-mile unpaved loop road allows visitors to drive through the valley floor.",
        ],
        "collection_handle": "monument-valley-art",
    },
    {
        "key": "yellowstone",
        "name": "Yellowstone National Park",
        "location": "Wyoming",
        "country": "USA",
        "year": "1872",
        "description": (
            "Yellowstone was the world's first national park, established in 1872, spanning "
            "nearly 9,000 square kilometers across Wyoming, Montana, and Idaho. It sits atop "
            "one of the world's largest active volcanic systems and contains over half of the "
            "world's active geysers, including the famous Old Faithful."
        ),
        "fun_facts": [
            "Old Faithful erupts approximately every 90 minutes, shooting up to 56,000 liters of boiling water as high as 56 meters — and it has been reliably performing for at least 200 years.",
            "The Yellowstone supervolcano's magma chamber is estimated to contain enough magma to fill the Grand Canyon more than 11 times, though a catastrophic eruption is not expected anytime soon.",
            "Grand Prismatic Spring is the largest hot spring in the United States at 110 meters across, and its vivid rainbow colors are produced by heat-loving microorganisms called thermophiles that thrive at different temperatures.",
        ],
        "collection_handle": "yellowstone-art",
    },
    {
        "key": "sugarloaf_rio",
        "name": "Sugarloaf Mountain",
        "location": "Rio de Janeiro",
        "country": "Brazil",
        "year": "Ancient",
        "description": (
            "Sugarloaf Mountain is a 396-meter peak at the mouth of Guanabara Bay in Rio de "
            "Janeiro, offering panoramic views of the city, Copacabana Beach, and Christ the "
            "Redeemer. A glass-walled cable car has carried visitors to the summit since 1912, "
            "making it one of the first urban cable car systems in the world."
        ),
        "fun_facts": [
            "The original cable car system was inaugurated in 1912, making it the third cable car in the world, and has since carried over 40 million passengers to the summit.",
            "Sugarloaf is a massive monolith of granite and quartz, formed over 600 million years ago, and its name likely comes from its resemblance to the conical clay molds used to refine sugar in colonial times.",
            "The peak has been a site of daring feats — in 1977, stuntman Roger Moore (as James Bond) famously fought atop the cable car in the film Moonraker, though the actual stunt was performed by Richard Kiel.",
        ],
        "collection_handle": "sugarloaf-rio-art",
    },
    {
        "key": "lake_louise",
        "name": "Lake Louise",
        "location": "Alberta",
        "country": "Canada",
        "year": "10,000 years ago",
        "description": (
            "Lake Louise is a glacially fed lake in Banff National Park known for its stunning "
            "turquoise color and the backdrop of Victoria Glacier. Named after Princess Louise "
            "Caroline Alberta, the daughter of Queen Victoria, it has attracted visitors since "
            "the Canadian Pacific Railway built the first Chateau Lake Louise in 1890."
        ),
        "fun_facts": [
            "The lake's remarkable turquoise color is caused by glacial rock flour — fine sediment ground by the Victoria Glacier that remains suspended in the water and refracts sunlight.",
            "The original Chateau Lake Louise was built in 1890 as a modest log cabin by the Canadian Pacific Railway to attract tourists to the rail line; it has since grown into one of the world's most famous lakeside hotels.",
            "Lake Louise sits at an elevation of 1,750 meters and is frozen over from November to June — in winter, the frozen lake surface is used for ice skating and ice sculpture festivals.",
        ],
        "collection_handle": "lake-louise-art",
    },
    {
        "key": "uluru",
        "name": "Uluru",
        "location": "Northern Territory",
        "country": "Australia",
        "year": "550 million years ago",
        "description": (
            "Uluru, also known as Ayers Rock, is a massive sandstone monolith in the heart of "
            "Australia's Red Centre, sacred to the Anangu Aboriginal people for tens of thousands "
            "of years. Standing 348 meters above the surrounding plain with a circumference of "
            "9.4 kilometers, it dramatically changes color throughout the day from ochre to fiery "
            "red at sunset."
        ),
        "fun_facts": [
            "Uluru extends an estimated 2.5 kilometers below the ground surface — what is visible above ground is just the tip of an enormous underground rock formation.",
            "Climbing Uluru was permanently banned in October 2019 at the request of the Anangu people, for whom the rock is deeply sacred and the climb follows a path of spiritual significance.",
            "Uluru appears to change color because the iron minerals in the sandstone oxidize and reflect light differently at various times of day — it glows brightest red at sunrise and sunset.",
        ],
        "collection_handle": "uluru-art",
    },
    {
        "key": "tongariro",
        "name": "Tongariro National Park",
        "location": "North Island",
        "country": "New Zealand",
        "year": "Ancient",
        "description": (
            "Tongariro National Park is New Zealand's oldest national park and a dual UNESCO "
            "World Heritage Site, home to three active volcanoes: Tongariro, Ngauruhoe, and "
            "Ruapehu. The Tongariro Alpine Crossing, a 19.4-kilometer day hike through volcanic "
            "landscapes, emerald lakes, and steaming vents, is considered one of the world's "
            "greatest single-day treks."
        ),
        "fun_facts": [
            "Mount Ngauruhoe served as the filming location for Mount Doom in Peter Jackson's Lord of the Rings trilogy, and its near-perfect volcanic cone is remarkably similar to Tolkien's description.",
            "Tongariro was the fourth national park established in the world, gifted to the New Zealand government in 1887 by the Maori chief Te Heuheu Tukino IV to protect it from European settlement.",
            "The Emerald Lakes on the Tongariro Crossing get their vivid green color from dissolved minerals leached from the surrounding volcanic rock, and the water is highly acidic.",
        ],
        "collection_handle": "tongariro-art",
    },
    {
        "key": "great_barrier_reef",
        "name": "Great Barrier Reef",
        "location": "Queensland",
        "country": "Australia",
        "year": "Ancient",
        "description": (
            "The Great Barrier Reef is the world's largest coral reef system, stretching over "
            "2,300 kilometers along the northeast coast of Australia. Composed of nearly 3,000 "
            "individual reef systems and hundreds of islands, it is the largest living structure "
            "on Earth and is visible from outer space."
        ),
        "fun_facts": [
            "The reef is home to over 1,500 species of fish, 400 types of coral, 4,000 species of mollusk, and 240 species of birds, making it one of the most biodiverse ecosystems on the planet.",
            "While the reef system is ancient, the current living reef structure is relatively young — most of the present reef grew on top of older platforms after the last ice age, beginning about 8,000 years ago.",
            "The reef generates approximately $6.4 billion annually for the Australian economy through tourism, fishing, and related industries, supporting about 64,000 jobs.",
        ],
        "collection_handle": "great-barrier-reef-art",
    },
    {
        "key": "bora_bora",
        "name": "Bora Bora",
        "location": "Leeward Islands",
        "country": "French Polynesia",
        "year": "4 million years ago",
        "description": (
            "Bora Bora is a volcanic island in French Polynesia surrounded by a turquoise "
            "lagoon and a barrier reef, dominated by the dramatic peak of Mount Otemanu rising "
            "727 meters above the water. Often called the most beautiful island in the world, "
            "its overwater bungalows, coral gardens, and crystal-clear lagoon make it the "
            "ultimate tropical paradise destination."
        ),
        "fun_facts": [
            "Bora Bora was a major U.S. military supply base during World War II — up to 6,000 American soldiers were stationed there, and remnants of guns and bunkers can still be found on the island.",
            "The original Polynesian name is Pora Pora, meaning 'first born,' and it was one of the last islands to be settled by Polynesian voyagers navigating by stars across the Pacific.",
            "Bora Bora's overwater bungalows were invented here in the 1960s — three American hotel developers who couldn't find enough beachfront land built stilted huts over the lagoon, creating a concept that spread worldwide.",
        ],
        "collection_handle": "bora-bora-art",
    },
    {
        "key": "burj_khalifa",
        "name": "Burj Khalifa",
        "location": "Dubai",
        "country": "UAE",
        "year": "2010",
        "description": (
            "The Burj Khalifa is the world's tallest building, soaring 828 meters with 163 "
            "floors above the Dubai skyline. Completed in 2010, its Y-shaped floor plan was "
            "inspired by the Hymenocallis flower, and it holds multiple world records including "
            "tallest structure, highest occupied floor, and highest outdoor observation deck."
        ),
        "fun_facts": [
            "The building is so tall that temperatures at the top can be up to 6 degrees Celsius cooler than at ground level, and residents on upper floors see the sunset about two minutes later than people at the base.",
            "The Burj Khalifa uses a buttressed core structural system that had never been used at such a height — the building tapers as it rises, reducing wind forces, and setbacks at different levels break up vortex shedding.",
            "The tower was originally called Burj Dubai but was renamed Burj Khalifa at its inauguration in honor of UAE President Sheikh Khalifa bin Zayed Al Nahyan, whose government provided financial support during the 2009 financial crisis.",
        ],
        "collection_handle": "burj-khalifa-art",
    },
    {
        "key": "wadi_rum",
        "name": "Wadi Rum",
        "location": "Aqaba Governorate",
        "country": "Jordan",
        "year": "Ancient",
        "description": (
            "Wadi Rum is a vast desert valley in southern Jordan characterized by towering "
            "sandstone and granite rock formations, natural arches, and ancient petroglyphs. "
            "Known as the Valley of the Moon for its otherworldly landscape, it was the base "
            "of operations for T.E. Lawrence during the Arab Revolt and is a UNESCO World "
            "Heritage Site."
        ),
        "fun_facts": [
            "T.E. Lawrence (Lawrence of Arabia) described Wadi Rum as 'vast, echoing, and God-like' in his memoir Seven Pillars of Wisdom, and the 1962 film Lawrence of Arabia was partly filmed here.",
            "Wadi Rum has been used as a stand-in for Mars in multiple films including The Martian (2015) and has served as an alien landscape in Rogue One, Dune, and other science fiction productions.",
            "The desert contains rock carvings and inscriptions dating back over 12,000 years, left by the Nabataeans, Thamudic tribes, and other ancient peoples who traversed the region.",
        ],
        "collection_handle": "wadi-rum-art",
    },
    {
        "key": "sheikh_zayed_mosque",
        "name": "Sheikh Zayed Grand Mosque",
        "location": "Abu Dhabi",
        "country": "UAE",
        "year": "2007",
        "description": (
            "The Sheikh Zayed Grand Mosque is one of the world's largest mosques, featuring "
            "82 domes, over 1,000 columns, and the capacity to hold over 40,000 worshippers. "
            "Completed in 2007 and named after the UAE's founding father, Sheikh Zayed bin "
            "Sultan Al Nahyan, its gleaming white marble exterior and lavish interior make it "
            "one of the most visually stunning religious buildings in the modern world."
        ),
        "fun_facts": [
            "The mosque's main prayer hall contains the world's largest hand-knotted carpet, measuring 5,627 square meters and weighing 35 tons — it was made by 1,200 artisans over two years.",
            "Seven Swarovski crystal chandeliers hang inside the mosque, the largest of which weighs approximately 12 tons and is 10 meters in diameter, making it one of the largest chandeliers in the world.",
            "The exterior features over 1,000 columns inlaid with semi-precious stones including lapis lazuli, red agate, amethyst, and mother of pearl in floral designs inspired by Mughal architecture.",
        ],
        "collection_handle": "sheikh-zayed-mosque-art",
    },
    {
        "key": "cappadocia",
        "name": "Cappadocia",
        "location": "Nevsehir Province",
        "country": "Turkey",
        "year": "Ancient",
        "description": (
            "Cappadocia is a historical region in central Turkey famous for its surreal landscape "
            "of fairy chimneys, cone-shaped rock formations, and vast underground cities carved "
            "into soft volcanic tuff. Early Christians carved churches, monasteries, and entire "
            "cities into the rock, and today it is best known for the hundreds of hot air balloons "
            "that float above its valleys at dawn."
        ),
        "fun_facts": [
            "Derinkuyu, one of the region's underground cities, extends 60 meters below the surface with 18 levels and could shelter approximately 20,000 people along with their livestock and food stores.",
            "The fairy chimneys were formed when soft volcanic tuff deposited by ancient eruptions was eroded away, leaving harder basalt caps balanced on pillars of softer rock.",
            "Over 100 hot air balloons launch at sunrise on clear mornings during the flying season, creating one of the most photographed spectacles in the world.",
        ],
        "collection_handle": "cappadocia-art",
    },
    {
        "key": "northern_lights_iceland",
        "name": "Northern Lights",
        "location": "Iceland",
        "country": "Iceland",
        "year": "Ancient",
        "description": (
            "The Northern Lights, or Aurora Borealis, are a natural light display visible across "
            "Iceland's dark winter skies from September to April. Caused by charged particles "
            "from the sun colliding with gases in Earth's atmosphere, the aurora paints the sky "
            "in shimmering curtains of green, purple, pink, and blue, and Iceland's location "
            "near the Arctic Circle makes it one of the best places on Earth to witness them."
        ),
        "fun_facts": [
            "In Norse mythology, the Northern Lights were believed to be the reflections of the Valkyries' armor as they led fallen warriors to Valhalla.",
            "The most common color of the aurora is green, produced when charged particles collide with oxygen molecules at altitudes of 100 to 300 kilometers, while red auroras occur at higher altitudes and are much rarer.",
            "Reykjavik turns off its street lights on especially active aurora nights to give residents and visitors a better view — this coordinated dimming is announced in advance by the city.",
        ],
        "collection_handle": "northern-lights-iceland-art",
    },
    {
        "key": "li_river_guilin",
        "name": "Li River",
        "location": "Guilin",
        "country": "China",
        "year": "Ancient",
        "description": (
            "The Li River winds 83 kilometers from Guilin to Yangshuo through a dreamlike "
            "landscape of karst limestone peaks, bamboo groves, and traditional fishing villages. "
            "The scenery along this stretch has inspired Chinese painters and poets for centuries "
            "and appears on the back of the 20-yuan banknote."
        ),
        "fun_facts": [
            "The famous scene depicted on the Chinese 20-yuan banknote shows the karst peaks near Xingping village along the Li River, making it one of the most widely reproduced landscapes in the world.",
            "Local fishermen still practice the ancient art of cormorant fishing, using trained birds that dive into the water to catch fish — a tradition dating back over 1,300 years.",
            "The karst peaks along the Li River were formed over 300 million years ago when the area was an ancient seabed — tectonic uplift and millions of years of erosion by water created the distinctive tower-like formations.",
        ],
        "collection_handle": "li-river-guilin-art",
    },
    {
        "key": "mysore_palace",
        "name": "Mysore Palace",
        "location": "Mysore",
        "country": "India",
        "year": "1912",
        "description": (
            "Mysore Palace, officially Amba Vilas Palace, is a historical palace in the city of "
            "Mysore that served as the seat of the Wadiyar dynasty, the rulers of the Kingdom of "
            "Mysore. The current structure was completed in 1912 in an Indo-Saracenic style "
            "blending Hindu, Muslim, Rajput, and Gothic elements, and it is the most visited "
            "monument in India after the Taj Mahal."
        ),
        "fun_facts": [
            "During the Dasara festival, the palace is illuminated with nearly 100,000 light bulbs, transforming it into a dazzling spectacle that draws hundreds of thousands of visitors over the ten-day celebration.",
            "The current palace is actually the fourth on the site — the previous wooden palace burned down in 1897 during a royal wedding, and the Wadiyar maharaja commissioned British architect Henry Irwin to design the replacement.",
            "The Durbar Hall inside features an ornate ceiling painted with scenes from the Dasara procession, stained glass from Glasgow, carved mahogany doors, and a solid silver entry door weighing over 750 kilograms.",
        ],
        "collection_handle": "mysore-palace-art",
    },
    {
        "key": "banaue_rice_terraces",
        "name": "Banaue Rice Terraces",
        "location": "Ifugao Province",
        "country": "Philippines",
        "year": "2,000 years ago",
        "description": (
            "The Banaue Rice Terraces are 2,000-year-old terraces carved into the mountains of "
            "Ifugao province in the northern Philippines by the ancestors of the indigenous Ifugao "
            "people. Often called the 'Eighth Wonder of the World,' these hand-carved steps climb "
            "to elevations of 1,500 meters and would stretch over 20,000 kilometers if laid end "
            "to end."
        ),
        "fun_facts": [
            "The terraces were carved by hand using primitive tools over 2,000 years ago and are fed by an ancient irrigation system that channels water from the rainforests above down through the terraces.",
            "If all the terrace walls were placed end to end, they would encircle approximately half of the globe — a staggering feat of engineering for a pre-industrial society.",
            "The Ifugao people maintain the terraces using traditional farming methods passed down through generations, but many young Ifugao are moving to cities, placing this UNESCO World Heritage Site at risk.",
        ],
        "collection_handle": "banaue-rice-terraces-art",
    },
]

LANDMARKS_BY_KEY = {lm["key"]: lm for lm in LANDMARKS}
