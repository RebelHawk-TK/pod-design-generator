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
]

LANDMARKS_BY_KEY = {lm["key"]: lm for lm in LANDMARKS}
