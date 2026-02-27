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
]

LANDMARKS_BY_KEY = {lm["key"]: lm for lm in LANDMARKS}
