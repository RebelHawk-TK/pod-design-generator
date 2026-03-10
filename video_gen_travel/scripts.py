"""50 educational voiceover scripts for travel/history videos.

Each landmark has two variants:
  - "a": Origin story / construction history
  - "b": Fun facts / modern significance

Scripts are 50-60 words, educational tone, no product mentions.
"""

from __future__ import annotations

TRAVEL_SCRIPTS: dict[str, dict[str, str]] = {
    "eiffel_tower": {
        "a": (
            "Built in 1889 for the Paris World's Fair, the Eiffel Tower was meant "
            "to stand for just twenty years. Gustave Eiffel's iron lattice design "
            "was called an eyesore by artists and intellectuals. Yet it survived "
            "demolition, became a radio tower, and ultimately the most visited "
            "paid monument on Earth."
        ),
        "b": (
            "Every seven years, sixty tonnes of paint are applied to the Eiffel "
            "Tower entirely by hand. The tower grows up to six inches taller in "
            "summer heat as the iron expands. At night, its twenty thousand light "
            "bulbs create the famous sparkling display, which is actually "
            "copyrighted under French law."
        ),
    },
    "taj_mahal": {
        "a": (
            "Emperor Shah Jahan commissioned the Taj Mahal in 1632 as a tomb for "
            "his beloved wife Mumtaz Mahal, who died during childbirth. Over twenty "
            "thousand artisans worked for twenty-two years, using white marble from "
            "Rajasthan and precious stones from across Asia to create this monument "
            "to eternal love."
        ),
        "b": (
            "The Taj Mahal's white marble changes color throughout the day — pink "
            "at dawn, brilliant white at noon, and golden under moonlight. The "
            "minarets tilt slightly outward so they would fall away from the tomb "
            "in an earthquake. A legend claims Shah Jahan planned an identical "
            "black marble twin across the river."
        ),
    },
    "colosseum": {
        "a": (
            "Construction of Rome's Colosseum began in 72 AD under Emperor "
            "Vespasian and finished eight years later under his son Titus. The "
            "inaugural games lasted one hundred days and reportedly saw thousands "
            "of gladiators and wild animals. Its ingenious design could seat fifty "
            "thousand spectators and be emptied in minutes."
        ),
        "b": (
            "The Colosseum had a retractable canvas awning called the velarium, "
            "operated by a thousand sailors. Beneath the arena floor lay a network "
            "of tunnels, cages, and elevators that lifted animals dramatically into "
            "view. Over the centuries, nearly two-thirds of the original stone was "
            "stripped away and reused in other Roman buildings."
        ),
    },
    "great_wall": {
        "a": (
            "The Great Wall of China was not built all at once but over two "
            "thousand years, beginning in the seventh century BC. Multiple "
            "dynasties extended and connected separate walls. The Ming Dynasty "
            "rebuilt most of what we see today, using brick and stone instead of "
            "packed earth. It stretches over thirteen thousand miles."
        ),
        "b": (
            "Despite popular belief, the Great Wall cannot be seen from space with "
            "the naked eye. The mortar between its bricks contains sticky rice, "
            "which made it incredibly strong. Watchtowers along the wall used smoke "
            "signals by day and fire by night to communicate across hundreds of "
            "miles in just hours."
        ),
    },
    "notre_dame": {
        "a": (
            "Construction of Notre-Dame de Paris began in 1163 and took nearly two "
            "centuries to complete. Medieval craftsmen used innovative flying "
            "buttresses to support its towering walls and massive rose windows. "
            "The cathedral has witnessed coronations, revolutions, and Napoleon's "
            "self-crowning as Emperor of France."
        ),
        "b": (
            "Notre-Dame's famous gargoyles actually serve as rain gutters, "
            "channeling water away from the stone walls. The cathedral's great "
            "bell, Emmanuel, weighs over thirteen tonnes and has rung for every "
            "major event in French history. After the devastating 2019 fire, an "
            "international effort restored the spire and roof in just five years."
        ),
    },
    "neuschwanstein": {
        "a": (
            "King Ludwig the Second of Bavaria began building Neuschwanstein Castle "
            "in 1869 as a personal retreat, inspired by the operas of Richard "
            "Wagner. He spent lavishly on theatrical interiors and never intended "
            "it as a seat of power. Ludwig was declared insane before it was "
            "finished and died mysteriously days later."
        ),
        "b": (
            "Neuschwanstein means New Swan Stone, named after a Wagner opera "
            "character. Walt Disney visited in 1935 and used it as direct "
            "inspiration for Sleeping Beauty's Castle. Despite being Ludwig's "
            "private fantasy, the castle opened to the public just seven weeks "
            "after his death and now welcomes over one point four million visitors "
            "each year."
        ),
    },
    "mount_fuji": {
        "a": (
            "Mount Fuji last erupted in 1707, blanketing Tokyo in volcanic ash. "
            "The nearly perfect symmetrical cone was formed by layers of lava and "
            "debris over hundreds of thousands of years. For centuries, women were "
            "forbidden from climbing it. Today it is Japan's highest peak at "
            "over twelve thousand feet."
        ),
        "b": (
            "Mount Fuji is considered sacred in both Shinto and Buddhist traditions. "
            "Its iconic shape has inspired countless artists, most famously "
            "Hokusai's Great Wave woodblock print. Around three hundred thousand "
            "people climb it each summer during the official season. The mountain "
            "has its own post office at the summit where climbers can mail postcards."
        ),
    },
    "golden_gate": {
        "a": (
            "The Golden Gate Bridge opened in 1937 after four years of construction "
            "that many engineers said was impossible. Chief engineer Joseph Strauss "
            "pioneered safety nets that saved nineteen workers' lives during "
            "construction. The bridge's main span stretches over four thousand feet "
            "across one of the world's most treacherous straits."
        ),
        "b": (
            "The Golden Gate Bridge's signature International Orange color was "
            "originally meant as a temporary primer. The Navy wanted it painted "
            "black and yellow for visibility. Strong winds can cause the bridge "
            "to sway up to twenty-seven feet sideways. A dedicated team of painters "
            "works year-round — they never actually finish before starting over."
        ),
    },
    "sydney_opera": {
        "a": (
            "Danish architect Jorn Utzon won a 1957 design competition for the "
            "Sydney Opera House, beating over two hundred entries. Construction "
            "took sixteen years instead of four, and costs ballooned from seven "
            "million to one hundred two million dollars. Utzon resigned in "
            "frustration and never saw the finished building in person."
        ),
        "b": (
            "The Sydney Opera House roof is covered with over one million Swedish "
            "tiles that are self-cleaning in the rain. Its sails were originally "
            "impossible to build until engineers realized they could all be cut "
            "from sections of a single sphere. The building hosts over fifteen "
            "hundred performances every year across its multiple venues."
        ),
    },
    "santorini": {
        "a": (
            "Santorini's dramatic crescent shape was created by one of history's "
            "largest volcanic eruptions around 1600 BC. The Minoan eruption "
            "destroyed the island's center, possibly inspiring the legend of "
            "Atlantis. Ancient ruins at Akrotiri, preserved under volcanic ash, "
            "reveal a sophisticated Bronze Age civilization with running water."
        ),
        "b": (
            "Santorini's iconic white-washed buildings with blue domes were "
            "originally a practical choice — white lime paint was cheap and "
            "reflected the intense Mediterranean sun. The island produces unique "
            "wines from vines trained into basket shapes to resist fierce winds. "
            "Its sunsets over the caldera are considered among the most beautiful "
            "in the world."
        ),
    },
    "angkor_wat": {
        "a": (
            "King Suryavarman the Second built Angkor Wat in the early twelfth "
            "century as a Hindu temple dedicated to Vishnu. Over three hundred "
            "thousand workers and six thousand elephants helped construct it. The "
            "temple complex covers more area than Vatican City and gradually "
            "converted to Buddhism as Khmer culture evolved."
        ),
        "b": (
            "Angkor Wat is oriented to the west, unusual for Hindu temples, "
            "possibly symbolizing the setting sun and the afterlife. Its walls "
            "contain nearly two thousand carved apsara dancers, each with a unique "
            "expression and hairstyle. The moat surrounding the temple is not just "
            "decorative — it stabilizes the sandy soil beneath the massive stone "
            "structure."
        ),
    },
    "machu_picchu": {
        "a": (
            "Built around 1450 by the Inca emperor Pachacuti, Machu Picchu sits "
            "nearly eight thousand feet above sea level in the Andes. The city was "
            "abandoned during the Spanish conquest and remained unknown to the "
            "outside world for centuries. American historian Hiram Bingham "
            "rediscovered it in 1911, guided by a local farmer."
        ),
        "b": (
            "Machu Picchu's stones were cut so precisely that no mortar was needed "
            "— you cannot fit a knife blade between them. This technique actually "
            "makes the structures earthquake-resistant. The Incas built over seven "
            "hundred terraces for farming and water management. Only about thirty "
            "percent of the construction is visible — the rest is underground "
            "foundations."
        ),
    },
    "sagrada_familia": {
        "a": (
            "Antoni Gaudi took over the Sagrada Familia project in 1883 and "
            "dedicated his final forty-three years entirely to it. He knew he "
            "would not live to see it finished. Funded only by donations and "
            "entrance fees, the basilica has been under construction for over one "
            "hundred forty years and is expected to be completed by 2026."
        ),
        "b": (
            "Gaudi designed the Sagrada Familia's columns to branch like trees, "
            "creating a forest of light inside. Each of the eighteen planned towers "
            "represents a different biblical figure. Modern architects use "
            "three-dimensional printing and computer modeling to realize Gaudi's "
            "original plaster models. When complete, the tallest tower will make "
            "it Europe's tallest church."
        ),
    },
    "parthenon": {
        "a": (
            "The Parthenon was built between 447 and 432 BC under the Athenian "
            "leader Pericles to honor the goddess Athena. Architects Iktinos and "
            "Kallikrates designed it with subtle curves — no straight lines exist "
            "in the entire structure. Inside stood a massive gold and ivory statue "
            "of Athena that was later lost to history."
        ),
        "b": (
            "The Parthenon has served as a Greek temple, a Christian church, a "
            "mosque, and an ammunition dump. In 1687, a Venetian cannonball struck "
            "the stored gunpowder, blowing off the roof. Lord Elgin controversially "
            "removed half the surviving sculptures to London in 1801. Greece has "
            "been requesting their return for over two hundred years."
        ),
    },
    "stonehenge": {
        "a": (
            "Stonehenge was built in several stages over fifteen hundred years, "
            "beginning around 3000 BC. The massive sarsen stones, each weighing "
            "up to twenty-five tonnes, were transported from Marlborough Downs "
            "twenty-five miles away. The smaller bluestones came from Wales, over "
            "one hundred fifty miles distant, though how remains debated."
        ),
        "b": (
            "Stonehenge aligns precisely with the sunrise on the summer solstice "
            "and sunset on the winter solstice. Recent DNA analysis suggests its "
            "builders came from Anatolia via the Mediterranean. A highway tunnel "
            "is currently being built nearby to remove traffic from the ancient "
            "landscape. Each year, thousands gather at the stones to celebrate "
            "the solstice at dawn."
        ),
    },
    "moai": {
        "a": (
            "The Moai statues of Easter Island were carved by the Rapa Nui people "
            "between 1250 and 1500 AD from compressed volcanic ash. Nearly nine "
            "hundred statues were carved, with the largest standing thirty-three "
            "feet tall. They represented ancestral chiefs and were believed to "
            "channel spiritual power to protect the living."
        ),
        "b": (
            "Contrary to popular belief, the Moai were not just heads — most have "
            "full bodies buried up to their shoulders by centuries of soil movement. "
            "Researchers proved the statues were walked to their platforms by "
            "rocking them side to side with ropes. Each statue's eyes were made of "
            "white coral and red stone, now mostly lost to time."
        ),
    },
    "pyramids_giza": {
        "a": (
            "The Great Pyramid of Giza was built around 2560 BC as a tomb for "
            "Pharaoh Khufu. Over two million limestone blocks, each weighing "
            "about two and a half tonnes, were precisely stacked over twenty years. "
            "It remained the world's tallest structure for nearly four thousand "
            "years until Lincoln Cathedral surpassed it in 1311."
        ),
        "b": (
            "The Great Pyramid was originally covered in polished white limestone "
            "casing stones that made it gleam in the sun. The base is level to "
            "within less than one inch across thirteen acres. Inside, the "
            "temperature remains a constant sixty-eight degrees Fahrenheit. The "
            "three pyramids of Giza are aligned with the stars of Orion's Belt, "
            "though scholars debate whether this was intentional."
        ),
    },
    "petra": {
        "a": (
            "Petra was carved from rose-red sandstone cliffs by the Nabataean "
            "people over two thousand years ago. This trading hub controlled vital "
            "spice and silk routes connecting Arabia, Egypt, and the Mediterranean. "
            "Earthquakes and shifting trade routes led to its abandonment. Swiss "
            "explorer Johann Burckhardt rediscovered it in 1812."
        ),
        "b": (
            "Only fifteen percent of Petra has been explored by archaeologists. "
            "The famous Treasury facade stands over one hundred thirty feet tall "
            "and was likely a royal tomb, not a treasury. The Nabataeans engineered "
            "an elaborate water system with dams, cisterns, and ceramic pipes that "
            "supplied water to over thirty thousand residents in the middle of "
            "the desert."
        ),
    },
    "st_basils": {
        "a": (
            "Ivan the Terrible ordered Saint Basil's Cathedral built in 1555 to "
            "celebrate Russia's conquest of Kazan. Legend says Ivan blinded the "
            "architects so they could never create anything more beautiful. The "
            "cathedral's nine chapels were originally white with golden domes. "
            "The famous colorful onion domes were added in the seventeenth century."
        ),
        "b": (
            "Each of Saint Basil's nine domes is unique in shape, size, and color, "
            "and no two are alike. The cathedral survived Napoleon's order to "
            "destroy it and Stalin's plans to demolish it for wider military "
            "parades. An architect who refused to tear it down was reportedly sent "
            "to a labor camp. Today it stands as Russia's most recognizable "
            "landmark."
        ),
    },
    "chichen_itza": {
        "a": (
            "Chichen Itza was one of the largest Maya cities, thriving from around "
            "600 to 1200 AD in Mexico's Yucatan Peninsula. The iconic pyramid of "
            "Kukulcan stands seventy-nine feet tall with three hundred sixty-five "
            "steps — one for each day of the year. The city blended Maya and "
            "Toltec architectural styles in a unique cultural fusion."
        ),
        "b": (
            "During the spring and autumn equinoxes, sunlight creates a shadow "
            "pattern on Kukulcan's staircase that resembles a serpent descending "
            "the pyramid. Clap your hands at the base and the echo sounds like "
            "the call of the sacred quetzal bird. A cenote near the pyramid "
            "contained jade, gold, and other offerings to the rain god Chaac."
        ),
    },
    "christ_redeemer": {
        "a": (
            "Christ the Redeemer was built between 1922 and 1931 atop Corcovado "
            "Mountain overlooking Rio de Janeiro. Brazilian engineer Heitor da "
            "Silva Costa designed it, while French sculptor Paul Landowski created "
            "the hands and head. The statue stands ninety-eight feet tall with arms "
            "stretching ninety-two feet wide, made of reinforced concrete and "
            "soapstone."
        ),
        "b": (
            "Christ the Redeemer is struck by lightning several times each year, "
            "and in 2014 a bolt chipped off the tip of one thumb. The statue's "
            "soapstone exterior was chosen because it resists cracking in extreme "
            "temperatures. A small chapel inside the base hosts weddings and "
            "baptisms. In 2007 it was named one of the New Seven Wonders of "
            "the World."
        ),
    },
    "hagia_sophia": {
        "a": (
            "Emperor Justinian built the Hagia Sophia in just five years, "
            "completing it in 537 AD. Ten thousand workers constructed its "
            "revolutionary dome, which seemed to float on a ring of windows. For "
            "nearly a thousand years it was the world's largest cathedral. After "
            "the Ottoman conquest in 1453, it became a mosque with added minarets."
        ),
        "b": (
            "The Hagia Sophia's massive dome is over one hundred feet across and "
            "was an engineering marvel that influenced architecture for centuries. "
            "During restoration, workers discovered hidden Byzantine mosaics "
            "beneath layers of Ottoman plaster. The building has been a cathedral, "
            "a mosque, a museum, and in 2020 was reconverted to a mosque. It "
            "remains one of Istanbul's most visited sites."
        ),
    },
    "tower_of_pisa": {
        "a": (
            "Construction of the Tower of Pisa began in 1173 and took nearly two "
            "hundred years to complete. The tower started leaning during "
            "construction due to soft ground on one side. Builders tried to "
            "compensate by making upper floors slightly taller on the leaning side, "
            "giving the tower a subtle banana curve that most visitors never "
            "notice."
        ),
        "b": (
            "The Tower of Pisa leans at about four degrees — engineers stabilized "
            "it in the 1990s by removing soil from the high side. Galileo "
            "reportedly dropped two cannon balls from the tower to prove objects "
            "fall at the same speed regardless of weight. The tower has eight "
            "stories, two hundred ninety-four steps, and seven bells — one for "
            "each note of the musical scale."
        ),
    },
    "big_ben": {
        "a": (
            "The Elizabeth Tower, commonly called Big Ben, was completed in 1859 "
            "as part of the new Palace of Westminster after a fire destroyed the "
            "original. Big Ben actually refers to the great bell inside, which "
            "weighs over thirteen tonnes. The clock's accuracy is maintained by "
            "stacking old pennies on the pendulum mechanism."
        ),
        "b": (
            "Big Ben's clock faces are twenty-three feet in diameter, and the "
            "minute hands are over fourteen feet long. During World War Two, the "
            "tower's lights were blacked out but the bells continued to chime, "
            "broadcast by the BBC as a symbol of resilience. The tower leans "
            "slightly northwest due to underground railway construction and is "
            "sometimes called London's Leaning Tower."
        ),
    },
    "statue_of_liberty": {
        "a": (
            "France gifted the Statue of Liberty to the United States in 1886 to "
            "celebrate the centennial of American independence. Sculptor Frederic "
            "Auguste Bartholdi designed the exterior while Gustave Eiffel — yes, "
            "that Eiffel — engineered the internal iron framework. The statue "
            "arrived in three hundred fifty pieces packed in two hundred fourteen "
            "crates."
        ),
        "b": (
            "The Statue of Liberty's copper skin is only about two pennies thick, "
            "and her green color comes from natural oxidation over decades. Her "
            "crown has seven rays representing the seven continents and oceans. "
            "The broken chain at her feet symbolizes freedom from oppression. "
            "Over four million people visit Liberty Island each year, but only "
            "a few hundred can climb to the crown daily."
        ),
    },
    # ----- Phase 2 Landmarks -----
    "amsterdam_canals": {
        "a": (
            "Amsterdam's canal ring was dug in the early seventeenth century during "
            "the Dutch Golden Age, when the city was the richest in the world. "
            "Engineers laid out three concentric canals totaling over sixty miles, "
            "lined with thousands of narrow merchant houses built on wooden piles "
            "driven deep into the marshy ground."
        ),
        "b": (
            "Amsterdam has more than twelve hundred bridges, more than Venice and "
            "Paris combined. Many of the canal houses lean forward intentionally so "
            "furniture could be hoisted through upper windows without hitting the "
            "facade. Around two thousand five hundred houseboats line the canals, "
            "some converted into floating hotels and even a cat sanctuary."
        ),
    },
    "bagan_temples": {
        "a": (
            "Between the ninth and thirteenth centuries, the kings of Bagan built "
            "over ten thousand Buddhist temples across a forty-square-mile plain "
            "in central Myanmar. At its peak, Bagan rivaled Angkor Wat in scale "
            "and grandeur. A devastating earthquake in 1975 damaged many temples, "
            "though over two thousand still stand today."
        ),
        "b": (
            "Many of Bagan's temples contain murals that are nearly a thousand "
            "years old, depicting scenes from Buddhist scripture and daily life. "
            "Hot air balloon rides at sunrise over the temple plain have become one "
            "of Asia's most iconic travel experiences. Local craftspeople still "
            "produce lacquerware using techniques passed down for generations."
        ),
    },
    "bruges_medieval": {
        "a": (
            "Bruges was one of medieval Europe's wealthiest cities, a trading hub "
            "linking the North Sea to inland markets. Its canal network earned it "
            "the nickname Venice of the North. When the river Zwin silted up in "
            "the fifteenth century, trade shifted to Antwerp, and Bruges was "
            "frozen in time, preserving its medieval architecture almost perfectly."
        ),
        "b": (
            "Bruges's Belfry tower contains forty-seven bells that still play "
            "carillon concerts several times a week. The city is home to what many "
            "consider the world's finest chocolate shops, producing over fifty "
            "thousand tonnes of chocolate each year. A half-mile beer pipeline "
            "was built underground in 2016 to carry fresh beer from the brewery "
            "to the bottling plant."
        ),
    },
    "charles_bridge": {
        "a": (
            "King Charles the Fourth laid the first stone of Prague's Charles "
            "Bridge in 1357 at exactly five thirty-one in the morning, a time "
            "chosen by court astrologers. The gothic bridge took over fifty years "
            "to complete, spanning the Vltava River with sixteen arches. Legend "
            "says eggs were mixed into the mortar to strengthen it."
        ),
        "b": (
            "Thirty baroque statues line the Charles Bridge, added between 1683 "
            "and 1714. Touching the plaque beneath the statue of Saint John of "
            "Nepomuk is said to bring good luck and guarantee a return to Prague. "
            "The bridge was the only crossing over the Vltava for over four "
            "hundred years and today draws over thirty thousand visitors daily."
        ),
    },
    "chefchaouen": {
        "a": (
            "Chefchaouen was founded in 1471 as a fortress to fight Portuguese "
            "invasions in northern Morocco. Jewish refugees fleeing Spain in the "
            "fifteenth century are believed to have introduced the tradition of "
            "painting buildings blue, symbolizing the sky and heaven. The medina's "
            "winding streets have remained largely unchanged for centuries."
        ),
        "b": (
            "The blue paint used in Chefchaouen is said to repel mosquitoes, "
            "though locals debate whether this is fact or folklore. The town "
            "remained virtually unknown to outsiders until the 1920s when Spanish "
            "troops arrived. Today every shade of blue covers the walls, from "
            "powder to cobalt, making it one of the most photographed towns on "
            "Earth."
        ),
    },
    "edinburgh_old_town": {
        "a": (
            "Edinburgh's Old Town grew along a ridge descending from the castle "
            "to the Palace of Holyroodhouse, forming what is known as the Royal "
            "Mile. As space ran out, residents built upward — some tenements "
            "reached fourteen stories, making them Europe's first skyscrapers. "
            "The narrow closes and wynds between buildings hide centuries of "
            "history."
        ),
        "b": (
            "Beneath Edinburgh's streets lies an entire hidden city of underground "
            "vaults, sealed since the eighteenth century. The city inspired Robert "
            "Louis Stevenson's Doctor Jekyll and Mister Hyde. Edinburgh hosts the "
            "world's largest annual arts festival, the Fringe, which takes over "
            "the Old Town every August with over three thousand shows."
        ),
    },
    "fushimi_inari": {
        "a": (
            "Fushimi Inari Shrine was founded in 711 AD on the slopes of Mount "
            "Inari in southern Kyoto. It is dedicated to Inari, the Shinto god "
            "of rice, prosperity, and foxes. Over the centuries, thousands of "
            "vermilion torii gates were donated by individuals and businesses "
            "seeking good fortune, creating a tunnel of color up the mountainside."
        ),
        "b": (
            "The shrine's hiking trail through over ten thousand torii gates "
            "stretches about two and a half miles up Mount Inari and takes roughly "
            "two hours to complete. Stone fox statues guard the shrine because "
            "foxes are considered Inari's messengers. The gates are inscribed with "
            "donor names and dates, with the oldest gates dating back centuries."
        ),
    },
    "giants_causeway": {
        "a": (
            "The Giant's Causeway was formed sixty million years ago when volcanic "
            "eruptions forced molten basalt through chalk beds. As the lava cooled "
            "rapidly, it contracted and cracked into roughly forty thousand "
            "interlocking hexagonal columns. Irish legend attributes the formation "
            "to the giant Finn MacCool, who built it as a pathway to Scotland "
            "to challenge a rival."
        ),
        "b": (
            "Most of the Giant's Causeway columns are hexagonal, but some have "
            "four, five, seven, or eight sides. The tallest columns reach about "
            "thirty-nine feet high. In 1986 it became Northern Ireland's first "
            "UNESCO World Heritage Site. The same geological formation can be "
            "found across the sea at Fingal's Cave in Scotland, supporting the "
            "legend of a bridge between lands."
        ),
    },
    "guanajuato": {
        "a": (
            "Guanajuato was founded as a silver mining town in the sixteenth "
            "century and became one of the wealthiest cities in colonial Mexico. "
            "The silver from its mines funded ornate baroque churches and grand "
            "plazas. Its colorful houses climb steep hillsides, connected by "
            "narrow alleyways and underground tunnels that were once riverbeds."
        ),
        "b": (
            "Guanajuato's underground road network was created by diverting the "
            "river that frequently flooded the city. The famous Callejon del Beso, "
            "or Alley of the Kiss, is so narrow that lovers can lean from opposing "
            "balconies and kiss. The city hosts the Festival Cervantino, Latin "
            "America's largest performing arts festival, each October."
        ),
    },
    "hallgrimskirkja": {
        "a": (
            "Hallgrimskirkja was designed by architect Gudjon Samuelsson in 1937, "
            "inspired by the basalt lava columns found throughout Iceland's "
            "landscape. Construction took an extraordinary forty-one years, from "
            "1945 to 1986. At nearly two hundred forty feet tall, it is the "
            "largest church in Iceland and visible from almost anywhere in "
            "Reykjavik."
        ),
        "b": (
            "The church is named after the seventeenth-century Icelandic poet and "
            "clergyman Hallgrimur Petursson, who wrote Iceland's most beloved "
            "hymns. Its tower observation deck offers panoramic views of the "
            "colorful tin rooftops of Reykjavik. In front stands a statue of "
            "Leif Erikson, a gift from the United States in 1930, honoring the "
            "Viking explorer who reached North America five centuries before "
            "Columbus."
        ),
    },
    "hapenny_bridge": {
        "a": (
            "The Ha'penny Bridge was built in 1816 as Dublin's first pedestrian "
            "bridge, replacing a dangerous ferry service across the River Liffey. "
            "It was named for the half-penny toll charged to cross. Cast iron "
            "was imported from Shropshire, England, and the elegant arch design "
            "by John Windsor became an instant Dublin landmark."
        ),
        "b": (
            "The half-penny toll was collected for over a century until 1919 "
            "when Dublin Corporation purchased the bridge and made it free. The "
            "bridge's original oil lamps were replaced by three ornate cast iron "
            "lamps that still stand today. Over thirty thousand pedestrians cross "
            "it daily, making it one of Dublin's most photographed structures "
            "and a symbol of the city."
        ),
    },
    "havana_vieja": {
        "a": (
            "Old Havana was founded by the Spanish in 1519 as a key port for "
            "treasure fleets sailing between the Americas and Spain. Its strategic "
            "location led to the construction of massive fortresses, plazas, and "
            "baroque churches. After the 1959 revolution, many buildings were "
            "preserved in a time capsule of colonial and art deco architecture."
        ),
        "b": (
            "Old Havana's streets are a living museum of vintage American cars "
            "from the 1950s, kept running with ingenious repairs and Soviet-era "
            "parts. The neighborhood's famous Bodeguita del Medio bar claims to "
            "be the birthplace of the mojito. Since 1982, UNESCO has funded the "
            "restoration of hundreds of crumbling buildings, blending preservation "
            "with the daily life of over a hundred thousand residents."
        ),
    },
    "hawa_mahal": {
        "a": (
            "Maharaja Sawai Pratap Singh built the Hawa Mahal in 1799 as an "
            "extension of the Jaipur City Palace. Its nine hundred fifty-three "
            "small windows, called jharokhas, were designed so royal women could "
            "observe street festivals without being seen. The building's pink "
            "sandstone honeycomb facade is just one room deep in most places."
        ),
        "b": (
            "The Hawa Mahal, meaning Palace of Winds, was built without any "
            "foundation — it is the world's tallest building without one, standing "
            "five stories and fifty feet high. Its curved architecture and the "
            "Venturi effect through hundreds of windows create a natural air "
            "conditioning system. The facade is best viewed in the early morning "
            "when the rising sun bathes the pink sandstone in golden light."
        ),
    },
    "hoi_an": {
        "a": (
            "Hoi An was a major Southeast Asian trading port from the fifteenth "
            "to nineteenth centuries, attracting Chinese, Japanese, and European "
            "merchants. The Japanese Covered Bridge, built in the 1590s, still "
            "stands as a symbol of the town. When the Thu Bon River silted up, "
            "trade moved to nearby Da Nang, leaving Hoi An's ancient streets "
            "remarkably intact."
        ),
        "b": (
            "Each month on the full moon, Hoi An turns off its electric lights "
            "and the ancient town glows with hundreds of silk lanterns and candles "
            "floating on the river. The town is famous for its tailors, who can "
            "produce custom clothing in under twenty-four hours. Hoi An's cuisine, "
            "including cao lau noodles and white rose dumplings, is found nowhere "
            "else in Vietnam."
        ),
    },
    "milford_sound": {
        "a": (
            "Milford Sound was carved by glaciers over millions of years, creating "
            "a fjord flanked by sheer cliffs rising over three thousand feet "
            "straight from the water. The Maori knew it as Piopiotahi, named after "
            "the now-extinct piopio bird. Rudyard Kipling called it the eighth "
            "wonder of the world when he visited in the early twentieth century."
        ),
        "b": (
            "Milford Sound receives over twenty feet of rain annually, making it "
            "one of the wettest places on Earth. After heavy rain, dozens of "
            "temporary waterfalls cascade down the cliff faces. Bottlenose dolphins "
            "and fur seals are regular visitors, and rare black coral grows in its "
            "deep waters. A permanent layer of fresh rainwater on the surface "
            "creates unusual underwater visibility conditions."
        ),
    },
    "mont_saint_michel": {
        "a": (
            "In 708 AD, the Archangel Michael reportedly appeared to the Bishop "
            "of Avranches, commanding him to build a church on this tidal island "
            "in Normandy. Over centuries, a Benedictine abbey and a fortified "
            "village grew on the granite outcrop. The abbey withstood English "
            "sieges during the Hundred Years War and later served as a prison "
            "during the French Revolution."
        ),
        "b": (
            "The tides around Mont Saint-Michel are among Europe's most dramatic, "
            "with water levels rising up to forty-six feet. Before the modern "
            "causeway, pilgrims risked deadly quicksand to reach the island. The "
            "abbey's cloister appears to float above the sea, supported by "
            "columns arranged in a double row. Only about thirty permanent "
            "residents live on the island, but over three million tourists visit "
            "each year."
        ),
    },
    "moraine_lake": {
        "a": (
            "Moraine Lake sits at over six thousand feet in the Valley of the Ten "
            "Peaks in Banff National Park, fed by glacial meltwater. Its vivid "
            "turquoise color comes from rock flour — fine glacial sediment that "
            "refracts light. The lake was featured on the Canadian twenty-dollar "
            "bill from 1969 to 1979, making it one of Canada's most recognized "
            "landscapes."
        ),
        "b": (
            "Moraine Lake is only accessible from late May to early October "
            "because the road is buried under avalanche debris the rest of the "
            "year. Despite its name, the lake was likely formed by a rockslide "
            "rather than a glacial moraine. The famous view from the Rock Pile "
            "trail became so popular that Parks Canada now requires shuttle "
            "reservations during peak season."
        ),
    },
    "nyhavn": {
        "a": (
            "King Christian the Fifth ordered Nyhavn dug in 1671 as a commercial "
            "port connecting Copenhagen's inner city to the sea. Sailors, traders, "
            "and dockworkers filled its taverns and boarding houses. The brightly "
            "painted townhouses that line the canal today date from the seventeenth "
            "and eighteenth centuries, originally home to merchants and sea "
            "captains."
        ),
        "b": (
            "Hans Christian Andersen lived at three different addresses in Nyhavn "
            "over the course of his life and wrote some of his most famous fairy "
            "tales there. The oldest house, number nine, dates from 1681. Once a "
            "rough sailors' quarter, Nyhavn transformed in the 1970s into "
            "Copenhagen's most charming waterfront, now lined with restaurants and "
            "jazz clubs where vintage wooden ships bob in the canal."
        ),
    },
    "plitvice_lakes": {
        "a": (
            "Plitvice Lakes formed over thousands of years as water dissolved "
            "limestone and deposited travertine barriers, creating sixteen terraced "
            "lakes connected by over ninety waterfalls. The park covers nearly "
            "three hundred square kilometers of dense forest in central Croatia. "
            "It was among the first natural sites added to the UNESCO World "
            "Heritage List in 1979."
        ),
        "b": (
            "The lakes of Plitvice change color throughout the year, shifting "
            "between azure, green, blue, and grey depending on mineral content "
            "and sunlight angle. Bears, wolves, and over a hundred sixty bird "
            "species inhabit the surrounding forests. Wooden boardwalks wind "
            "through the park, letting visitors walk just inches above the crystal "
            "clear water. Swimming is not permitted to protect the fragile "
            "travertine formations."
        ),
    },
    "ponte_vecchio": {
        "a": (
            "The Ponte Vecchio was first built as a simple wooden crossing over "
            "the Arno River in Roman times. The current stone bridge dates from "
            "1345, rebuilt after a devastating flood. Originally home to butchers "
            "and tanners, the Medici rulers relocated goldsmiths and jewelers there "
            "in 1593 to improve the smell near the Vasari Corridor above."
        ),
        "b": (
            "The Ponte Vecchio is the only bridge in Florence that survived World "
            "War Two, reportedly spared on Hitler's direct orders because of its "
            "beauty. The Vasari Corridor, a secret elevated passageway built in "
            "1565, runs above the shops connecting the Uffizi Gallery to the Pitti "
            "Palace. The bridge's goldsmith shops still operate today, making it "
            "one of the oldest commercial streets in the world."
        ),
    },
    "rialto_bridge": {
        "a": (
            "The Rialto Bridge has spanned Venice's Grand Canal since a wooden "
            "version was first built in 1181. After that bridge collapsed under "
            "the weight of a wedding crowd, Antonio da Ponte designed the current "
            "stone arch, completed in 1591. Michelangelo and Palladio both "
            "submitted competing designs that were rejected."
        ),
        "b": (
            "The Rialto Bridge rests on over twelve thousand wooden piles driven "
            "into the canal bed, supporting a single marble arch spanning nearly "
            "ninety feet. Its central portico houses shops that have operated "
            "continuously for over four centuries. The bridge was the only way to "
            "cross the Grand Canal on foot for nearly three hundred years, making "
            "the surrounding Rialto market the commercial heart of Venice."
        ),
    },
    "rijksmuseum": {
        "a": (
            "The Rijksmuseum was founded in 1800 to house the Dutch Republic's "
            "art collection. Architect Pierre Cuypers designed the current "
            "building, which opened in 1885 as a cathedral-like blend of Gothic "
            "and Renaissance styles. It is home to Rembrandt's Night Watch and "
            "Vermeer's Milkmaid, among over eight thousand displayed objects from "
            "eight hundred years of Dutch history."
        ),
        "b": (
            "The Rijksmuseum underwent a ten-year, three hundred seventy-five "
            "million euro renovation that restored it to Cuypers's original "
            "vision. The museum's bicycle passageway, running straight through "
            "the building, is used by thousands of Amsterdam cyclists daily. "
            "Its research library is the largest art history library in the "
            "Netherlands, containing over four hundred fifty thousand volumes."
        ),
    },
    "temple_bar": {
        "a": (
            "Temple Bar takes its name from the Temple family who owned land "
            "along the River Liffey in the seventeenth century. The cobblestoned "
            "quarter nearly disappeared in the 1980s when plans called for a new "
            "bus terminal. Artists and musicians moved into the abandoned buildings "
            "at low rents, transforming it into Dublin's cultural and "
            "entertainment district."
        ),
        "b": (
            "Temple Bar is home to some of Dublin's oldest pubs, including the "
            "Temple Bar Pub itself, which dates back to 1840. The area hosts "
            "an outdoor food market every Saturday and a book market at the "
            "cobbled Meeting House Square. Street performers, live music, and "
            "gallery exhibitions fill the narrow lanes, making it the beating "
            "heart of Dublin's creative scene."
        ),
    },
    "twelve_apostles": {
        "a": (
            "The Twelve Apostles are limestone sea stacks along Australia's Great "
            "Ocean Road, formed over twenty million years of erosion by the "
            "Southern Ocean's powerful waves and winds. The cliffs originally "
            "extended further out to sea, but constant erosion carved caves, then "
            "arches, and finally the freestanding pillars we see today. Despite "
            "the name, there were only ever nine visible stacks."
        ),
        "b": (
            "One of the Twelve Apostles collapsed into the sea in 2005, reducing "
            "the number to eight. The stacks continue to erode at a rate of about "
            "one inch per year. The coastline was originally called the Sow and "
            "Piglets before being renamed for tourism appeal. Helicopter tours "
            "reveal the stacks' dramatic scale, with the tallest standing nearly "
            "one hundred fifty feet above the waves."
        ),
    },
    "zanzibar_stone_town": {
        "a": (
            "Zanzibar Stone Town was the heart of the East African spice and slave "
            "trade for centuries, ruled by Omani sultans from the seventeenth "
            "century onward. Its winding streets blend African, Arab, Indian, and "
            "European architectural influences. The famous carved wooden doors, "
            "some over centuries old, display the wealth and status of the families "
            "who lived behind them."
        ),
        "b": (
            "Stone Town has over five hundred intricately carved doorways, each "
            "telling a story through its design — Indian doors feature lotus "
            "patterns while Arab doors show Quranic inscriptions. Freddie Mercury "
            "of the band Queen was born here in 1946. The Darajani Market fills "
            "the streets with the scent of cloves, vanilla, and cinnamon, "
            "reminders of Zanzibar's history as the Spice Island."
        ),
    },
}
