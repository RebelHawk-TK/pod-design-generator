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
    # ── Phase 3 landmarks ───────────────────────────────────────────────
    "table_mountain": {
        "a": (
            "Table Mountain is one of the oldest mountains on Earth, with rocks "
            "dating back over six hundred million years — predating even the "
            "dinosaurs. The Khoisan people called it Hoerikwaggo, meaning Sea "
            "Mountain. Its distinctive flat top was formed by millions of years "
            "of erosion on horizontal sandstone layers."
        ),
        "b": (
            "Table Mountain is home to over fifteen hundred species of flowering "
            "plants, more than the entire United Kingdom. Its famous tablecloth "
            "cloud forms when moisture-laden air rolls over the summit. The "
            "aerial cableway, opened in 1929, rotates three hundred sixty degrees "
            "during the ascent, carrying sixty-five passengers per trip to the "
            "top."
        ),
    },
    "victoria_falls": {
        "a": (
            "The Kololo people called it Mosi-oa-Tunya, the Smoke That Thunders. "
            "Scottish explorer David Livingstone became the first European to see "
            "the falls in 1855 and named them after Queen Victoria. The Zambezi "
            "River plunges over three hundred fifty feet into a narrow gorge "
            "along the border of Zambia and Zimbabwe."
        ),
        "b": (
            "Victoria Falls is the largest curtain of falling water on Earth, "
            "stretching over a mile wide. The spray from the falls can be seen "
            "from over thirty miles away and rises up to thirteen hundred feet "
            "in the air. A natural rock pool called Devil's Pool sits at the "
            "very edge of the falls, where swimmers can peer over the precipice "
            "during the dry season."
        ),
    },
    "djemaa_el_fna": {
        "a": (
            "Djemaa el-Fna has been Marrakech's main square since the city was "
            "founded by the Almoravid dynasty in 1070. Its name may translate as "
            "Assembly of the Dead, possibly referring to public executions held "
            "there centuries ago. For nearly a thousand years it has served as a "
            "gathering place for traders, storytellers, and performers."
        ),
        "b": (
            "UNESCO declared Djemaa el-Fna a Masterpiece of the Oral and "
            "Intangible Heritage of Humanity in 2001. Each evening the square "
            "transforms as over a hundred food stalls appear, serving traditional "
            "dishes to thousands. Snake charmers, henna artists, and halqa "
            "performers — traditional storytellers who gather crowds in circles — "
            "keep alive traditions passed down through generations."
        ),
    },
    "lalibela_churches": {
        "a": (
            "King Lalibela ordered eleven churches carved from solid rock in the "
            "twelfth and thirteenth centuries in the Ethiopian highlands. Rather "
            "than being built upward, each church was excavated downward, chiseled "
            "from a single block of volcanic tuff. Legend says angels helped "
            "complete the work at night while human laborers rested during the day."
        ),
        "b": (
            "The Church of Saint George, carved in the shape of a cross, is the "
            "most iconic of Lalibela's rock-hewn churches. An intricate network "
            "of tunnels and passageways connects all eleven churches. Ethiopian "
            "Orthodox priests still conduct services in these eight-hundred-year-old "
            "structures. Lalibela remains a major pilgrimage site, drawing tens "
            "of thousands of worshippers each Ethiopian Christmas."
        ),
    },
    "serengeti": {
        "a": (
            "The Serengeti takes its name from the Maasai word Siringet, meaning "
            "Endless Plains. The ecosystem has sustained wildlife for millions of "
            "years across over twelve thousand square miles of grassland. German "
            "explorers documented the area in the late nineteenth century, and the "
            "region became a protected game reserve in 1929 and a national park "
            "in 1951."
        ),
        "b": (
            "The Great Migration sees over one and a half million wildebeest and "
            "hundreds of thousands of zebras travel in a circular route through "
            "the Serengeti each year. The ecosystem supports the highest "
            "concentration of large predators in Africa, including over three "
            "thousand lions. The Serengeti's kopjes — ancient granite outcroppings — "
            "serve as lookout posts for cheetahs and shelter for leopards."
        ),
    },
    "borobudur": {
        "a": (
            "Borobudur was built in the ninth century during the Sailendra dynasty "
            "on the island of Java, using over two million blocks of volcanic "
            "stone. The temple was abandoned after the decline of Buddhist kingdoms "
            "in Java and lay hidden under volcanic ash and jungle for centuries. "
            "British lieutenant governor Thomas Stamford Raffles rediscovered it "
            "in 1814."
        ),
        "b": (
            "Borobudur is the world's largest Buddhist temple, featuring over "
            "twenty-seven hundred carved relief panels and five hundred four "
            "Buddha statues. Its nine platforms represent the Buddhist cosmological "
            "path from earthly desire to enlightenment. At dawn, the temple's "
            "bell-shaped stupas emerge from mist with volcanic peaks behind them, "
            "creating one of Southeast Asia's most iconic views."
        ),
    },
    "terracotta_warriors": {
        "a": (
            "Emperor Qin Shi Huang commissioned his funerary army around 210 BC "
            "to protect him in the afterlife. An estimated seven hundred thousand "
            "laborers worked for decades to create the figures. The warriors were "
            "discovered accidentally in 1974 by farmers digging a well near Xi'an. "
            "Archaeologists have so far unearthed over eight thousand soldiers, "
            "horses, and chariots."
        ),
        "b": (
            "No two terracotta warriors have the same face — each was individually "
            "sculpted with unique features, hairstyles, and expressions. The "
            "figures were originally painted in vivid colors that faded within "
            "minutes of exposure to air. The emperor's actual tomb remains "
            "unexcavated; ancient texts describe rivers of mercury inside, and "
            "modern soil testing has confirmed unusually high mercury levels."
        ),
    },
    "golden_temple_amritsar": {
        "a": (
            "The Golden Temple was founded in 1577 by Guru Ram Das, the fourth "
            "Sikh Guru, who excavated the sacred pool known as Amrit Sarovar, "
            "which gives Amritsar its name. Guru Arjan Dev completed the temple "
            "in 1604 and installed the Adi Granth, the Sikh holy scripture, "
            "inside. Maharaja Ranjit Singh covered the upper floors in gold "
            "leaf in the early nineteenth century."
        ),
        "b": (
            "The Golden Temple's community kitchen, called the Langar, feeds up "
            "to one hundred thousand visitors every day for free, regardless of "
            "faith, caste, or background. The temple has four entrances, one on "
            "each side, symbolizing openness to all people and directions. The "
            "Harmandir Sahib sits in the center of the sacred pool, reached by "
            "a causeway, reflecting beautifully on the water at night."
        ),
    },
    "petronas_towers": {
        "a": (
            "The Petronas Towers were designed by Argentine-American architect "
            "Cesar Pelli and completed in 1998 in Kuala Lumpur. At over fourteen "
            "hundred fifty feet tall, they held the record as the world's tallest "
            "buildings until 2004. The design incorporates Islamic geometric "
            "patterns, with floor plans based on eight-pointed stars reflecting "
            "Malaysia's Muslim heritage."
        ),
        "b": (
            "The Petronas Towers' sky bridge on the forty-first floor is the "
            "highest two-story bridge in the world, connecting the twin towers "
            "at five hundred seventy feet above street level. Each tower rests "
            "on foundations of concrete piles reaching over three hundred feet "
            "deep. The towers required over thirty-six thousand tonnes of steel "
            "and over one hundred sixty thousand cubic meters of concrete to build."
        ),
    },
    "halong_bay": {
        "a": (
            "Halong Bay in northern Vietnam contains nearly two thousand limestone "
            "islands and islets formed over five hundred million years. Vietnamese "
            "legend says a dragon descended from the mountains to defend the coast, "
            "and the islands are the jewels it spat into the sea. The bay has been "
            "inhabited since prehistoric times, with evidence of human settlement "
            "dating back twenty-five thousand years."
        ),
        "b": (
            "Halong Bay's karst islands contain hundreds of caves and grottoes, "
            "many still being discovered. Floating fishing villages have existed "
            "on the bay for generations, with families living entirely on the "
            "water. The bay was designated a UNESCO World Heritage Site in 1994. "
            "The name Ha Long translates to Descending Dragon, and the bay's "
            "emerald waters and towering pillars create one of Asia's most "
            "dramatic landscapes."
        ),
    },
    "sigiriya": {
        "a": (
            "King Kashyapa built a fortress and palace atop Sigiriya, a massive "
            "rock column rising over six hundred feet above the Sri Lankan jungle, "
            "in the fifth century AD. After seizing the throne from his father, "
            "he chose this remote location as his stronghold. After Kashyapa's "
            "defeat in battle, Buddhist monks used the site as a monastery until "
            "the fourteenth century."
        ),
        "b": (
            "Sigiriya's Mirror Wall was once polished so highly that the king "
            "could see his reflection as he walked past. Ancient graffiti on the "
            "wall, dating from the seventh century onward, includes poems and "
            "comments from visitors — among the oldest known examples of travel "
            "writing. Frescoes of celestial maidens, painted fifteen hundred "
            "years ago, still retain their vivid colors in a sheltered alcove."
        ),
    },
    "potala_palace": {
        "a": (
            "The Potala Palace was built in its current form by the fifth Dalai "
            "Lama beginning in 1645 on Marpo Ri hill in Lhasa, Tibet. The White "
            "Palace served as the seat of government, while the Red Palace housed "
            "chapels and the tombs of previous Dalai Lamas. Over seven thousand "
            "workers and fifteen hundred artisans labored on the construction for "
            "decades."
        ),
        "b": (
            "The Potala Palace contains over a thousand rooms, ten thousand "
            "shrines, and approximately two hundred thousand statues. At over "
            "twelve thousand feet above sea level, it was one of the highest "
            "palaces ever built. The tomb of the fifth Dalai Lama is covered "
            "in nearly four tonnes of gold. Since the fourteenth Dalai Lama's "
            "exile in 1959, the palace has served as a museum and UNESCO World "
            "Heritage Site."
        ),
    },
    "meiji_shrine": {
        "a": (
            "Meiji Shrine was built in 1920 to honor Emperor Meiji and Empress "
            "Shoken, who led Japan's transformation from feudal isolation to modern "
            "nation during the Meiji Restoration. The original buildings were "
            "destroyed during World War Two air raids and faithfully reconstructed "
            "in 1958. The shrine sits within a forest of over one hundred "
            "thousand trees donated from across Japan."
        ),
        "b": (
            "The forest surrounding Meiji Shrine was entirely man-made, planted "
            "by over one hundred thousand volunteers who donated trees from every "
            "prefecture in Japan. Today it has grown into a thriving ecosystem "
            "in the heart of Tokyo with over three thousand species of plants "
            "and animals. Over three million people visit the shrine during the "
            "first three days of each new year for hatsumode, the traditional "
            "first shrine visit."
        ),
    },
    "gyeongbokgung": {
        "a": (
            "Gyeongbokgung Palace was first built in 1395 as the main royal "
            "palace of the Joseon dynasty, which ruled Korea for over five "
            "centuries. The palace was destroyed during the Japanese invasions "
            "of the 1590s and lay in ruins for nearly three hundred years before "
            "being rebuilt in 1867 by the regent Heungseon Daewongun."
        ),
        "b": (
            "Gyeongbokgung's Gyeonghoeru Pavilion appears to float on a large "
            "artificial lake and was used for royal banquets and diplomatic "
            "receptions. The changing of the guard ceremony, performed daily, "
            "recreates Joseon-era military rituals with soldiers in period "
            "costumes. Visitors can rent traditional hanbok clothing and explore "
            "the palace grounds in historical dress, a practice that has become "
            "one of Seoul's most popular cultural experiences."
        ),
    },
    "zhangjiajie": {
        "a": (
            "Zhangjiajie's towering sandstone pillars formed over three hundred "
            "million years as water and wind eroded a vast plateau of quartz "
            "sandstone in China's Hunan province. The area became China's first "
            "national forest park in 1982. Over three thousand narrow pillars, "
            "some rising over six hundred feet, create an otherworldly landscape "
            "often shrouded in mist."
        ),
        "b": (
            "Zhangjiajie's pillars inspired the floating mountains in the film "
            "Avatar, and one pillar was officially renamed the Avatar Hallelujah "
            "Mountain in 2010. The park's glass-bottomed bridge, opened in 2016, "
            "spans over fourteen hundred feet across a canyon at a height of "
            "nearly a thousand feet. Rhesus macaques roam freely throughout the "
            "park, often approaching visitors on the hiking trails."
        ),
    },
    "acropolis_athens": {
        "a": (
            "The Acropolis of Athens has been a site of worship and fortification "
            "for over three thousand years. The Parthenon, its crowning structure, "
            "was built between 447 and 432 BC under the leadership of Pericles "
            "as a temple to the goddess Athena. The architects Iktinos and "
            "Kallikrates designed it with subtle optical refinements that make "
            "its columns appear perfectly straight."
        ),
        "b": (
            "The Parthenon's columns actually lean slightly inward and bulge "
            "in the middle, optical corrections that prevent the building from "
            "appearing to sag. The temple served as a church and then a mosque "
            "before a Venetian bombardment in 1687 detonated Ottoman ammunition "
            "stored inside, causing massive damage. The ongoing restoration has "
            "been underway since 1975, using original marble and ancient "
            "construction techniques."
        ),
    },
    "blue_mosque": {
        "a": (
            "Sultan Ahmed the First commissioned the Blue Mosque in 1609 to rival "
            "the nearby Hagia Sophia. Architect Sedefkar Mehmed Aga completed it "
            "in 1616, creating the only imperial mosque in Istanbul with six "
            "minarets. The interior is lined with over twenty thousand handmade "
            "Iznik ceramic tiles featuring blue floral patterns that give the "
            "mosque its popular name."
        ),
        "b": (
            "When the Blue Mosque was built with six minarets, it sparked "
            "controversy because only the mosque in Mecca had as many. Sultan "
            "Ahmed resolved this by funding a seventh minaret at Mecca. The "
            "mosque's two hundred sixty windows flood the interior with natural "
            "light, illuminating the blue tilework. It remains an active place "
            "of worship, closing to tourists five times daily for prayer."
        ),
    },
    "duomo_florence": {
        "a": (
            "Construction of Florence's Cathedral, the Duomo, began in 1296 "
            "under architect Arnolfo di Cambio. The massive dome remained an "
            "unsolved engineering challenge for over a century until Filippo "
            "Brunelleschi won a competition in 1418 with his revolutionary "
            "double-shell design. He completed the dome in 1436 without using "
            "any external scaffolding or temporary support."
        ),
        "b": (
            "Brunelleschi's dome remains the largest masonry dome ever "
            "constructed, spanning nearly one hundred fifty feet across. He "
            "invented new hoisting machines and a herringbone brick pattern to "
            "build it, keeping his methods secret from rivals. The cathedral's "
            "facade was not finished until 1887, nearly six centuries after "
            "construction began. Climbing the four hundred sixty-three steps "
            "to the lantern rewards visitors with panoramic views of Florence."
        ),
    },
    "tower_of_london": {
        "a": (
            "William the Conqueror began building the Tower of London in 1066 "
            "after his invasion of England. The White Tower, the central keep, "
            "was completed around 1078 using stone imported from Caen in "
            "Normandy. Over the centuries the fortress expanded into a complex "
            "of towers, walls, and moats that served as a royal palace, prison, "
            "armory, and treasury."
        ),
        "b": (
            "The Crown Jewels have been kept at the Tower of London since 1303. "
            "Legend says if the Tower's ravens ever leave, the kingdom will fall, "
            "so their wings are clipped and they are cared for by a dedicated "
            "Ravenmaster. The Tower has housed famous prisoners including Anne "
            "Boleyn and Sir Walter Raleigh. Thirty-eight Yeoman Warders, known "
            "as Beefeaters, still guard the fortress today."
        ),
    },
    "dubrovnik_walls": {
        "a": (
            "Dubrovnik's city walls were first constructed in the seventh century "
            "and expanded over the following thousand years. The walls stretch "
            "nearly two kilometers around the old city, reaching up to eighty "
            "feet high and twenty feet thick. The Republic of Ragusa, as "
            "Dubrovnik was known, maintained its independence for over four "
            "hundred years partly thanks to these fortifications."
        ),
        "b": (
            "Dubrovnik's walls withstood Ottoman sieges, a devastating earthquake "
            "in 1667, and shelling during the 1990s Croatian War of Independence. "
            "The walls feature sixteen towers and five bastions connected by a "
            "continuous walkway. The city served as a filming location for King's "
            "Landing in Game of Thrones, bringing a surge of visitors. The walk "
            "along the walls takes about ninety minutes and offers sweeping "
            "Adriatic views."
        ),
    },
    "rothenburg": {
        "a": (
            "Rothenburg ob der Tauber was a free imperial city of the Holy Roman "
            "Empire, reaching its peak prosperity in the fourteenth century. When "
            "the Thirty Years' War devastated the region in the seventeenth "
            "century, the town fell into economic decline, which ironically "
            "preserved its medieval character. Its half-timbered houses and "
            "cobblestone streets survived virtually unchanged for centuries."
        ),
        "b": (
            "Rothenburg's medieval town wall is one of the best preserved in "
            "Germany, and visitors can walk along most of its length. The town's "
            "night watchman tour, led by a guide in period costume, has operated "
            "for decades and recounts tales of medieval life. The Christmas "
            "Museum and the year-round Kathe Wohlfahrt Christmas shop attract "
            "visitors from around the world, making Rothenburg synonymous "
            "with German holiday traditions."
        ),
    },
    "seville_alcazar": {
        "a": (
            "The Royal Alcazar of Seville was originally built as a fort by the "
            "Moors in 913 AD. After the Christian reconquest in 1248, King "
            "Pedro the First commissioned Mudejar artisans to rebuild the palace "
            "in the fourteenth century, blending Islamic and Christian artistic "
            "traditions. It is the oldest royal palace still in use in Europe, "
            "serving the Spanish royal family today."
        ),
        "b": (
            "The Alcazar's Ambassador Hall features a magnificent half-orange "
            "dome of gilded and interlocking wood, built without a single nail. "
            "Its gardens span over seventeen acres, featuring fountains, pavilions, "
            "and orange groves. The palace doubled as the Water Gardens of Dorne "
            "in Game of Thrones. Charles the Fifth and Isabella of Portugal were "
            "married in the palace in 1526."
        ),
    },
    "matterhorn": {
        "a": (
            "The Matterhorn's distinctive pyramid shape formed over millions of "
            "years as glaciers carved its four steep faces. At over fourteen "
            "thousand seven hundred feet, it straddles the border between "
            "Switzerland and Italy. Edward Whymper led the first successful "
            "ascent on July 14, 1865, but four of his seven team members died "
            "during the descent in one of mountaineering's greatest tragedies."
        ),
        "b": (
            "The Matterhorn inspired the design of the Toblerone chocolate "
            "logo and the Disneyland roller coaster. Over three thousand climbers "
            "attempt the summit each year, but the mountain has claimed over "
            "five hundred lives since records began. The Gornergrat railway, "
            "opened in 1898, carries visitors to over ten thousand feet for "
            "panoramic views of the peak and surrounding glaciers."
        ),
    },
    "amalfi_coast": {
        "a": (
            "The Amalfi Coast was home to the powerful Maritime Republic of "
            "Amalfi, which rivaled Venice and Genoa as a Mediterranean trading "
            "power from the ninth to twelfth centuries. The republic created "
            "the Tabula Amalfitana, one of the earliest codes of maritime law. "
            "Terraced lemon groves and pastel-colored villages cling to cliffs "
            "that plunge over a thousand feet into the Tyrrhenian Sea."
        ),
        "b": (
            "The Amalfi Coast's famous limoncello liqueur is made from sfusato "
            "lemons, a variety grown only on these terraces. The narrow coastal "
            "road, built in the mid-nineteenth century, features over a thousand "
            "curves along just thirty miles. Ravello, perched high above the "
            "coast, has hosted a music festival since 1953 in gardens where "
            "Richard Wagner once found inspiration for his opera Parsifal."
        ),
    },
    "trolltunga": {
        "a": (
            "Trolltunga, meaning Troll's Tongue, is a horizontal rock formation "
            "jutting out over Lake Ringedalsvatnet in western Norway. The "
            "formation was carved during the last ice age roughly ten thousand "
            "years ago when glacial water froze inside rock crevices and broke "
            "away chunks, leaving the tongue-shaped ledge suspended about "
            "thirty-six hundred feet above sea level."
        ),
        "b": (
            "The hike to Trolltunga covers roughly seventeen miles round trip "
            "and takes ten to twelve hours. The rock juts out horizontally about "
            "one hundred feet over the lake below. Once a little-known local "
            "attraction, a viral photo in 2010 turned it into one of Norway's "
            "most popular hikes, drawing over one hundred thousand visitors "
            "annually. The hiking season runs from mid-June to mid-September."
        ),
    },
    "meteora": {
        "a": (
            "Meteora's sandstone pillars formed over sixty million years ago as "
            "an ancient sea receded and erosion sculpted the remaining rock into "
            "towering columns in central Greece. In the fourteenth century, monks "
            "seeking isolation built monasteries atop these natural towers, "
            "accessible only by rope ladders and pulley-drawn nets. At their peak, "
            "twenty-four monasteries stood on the pillars."
        ),
        "b": (
            "Six of Meteora's original twenty-four monasteries remain active "
            "today, perched on pillars reaching over a thousand feet high. The "
            "name Meteora means suspended in the air. Until the 1920s, the only "
            "way to reach most monasteries was by rope basket. Steps carved into "
            "the rock now provide access, though monks still use the original "
            "rope systems for hauling supplies."
        ),
    },
    "niagara_falls": {
        "a": (
            "Niagara Falls formed roughly twelve thousand years ago as glaciers "
            "retreated at the end of the last ice age, diverting water from the "
            "Great Lakes over the Niagara Escarpment. The falls have eroded "
            "seven miles upstream from their original position. In 1859, Charles "
            "Blondin crossed the gorge on a tightrope, performing stunts "
            "including carrying his manager on his back."
        ),
        "b": (
            "Over seven hundred fifty thousand gallons of water flow over Niagara "
            "Falls every second during peak daytime hours. At night, up to "
            "seventy-five percent of the water is diverted through tunnels to "
            "generate hydroelectric power. The falls freeze partially in extreme "
            "winters, creating spectacular ice formations. The Maid of the Mist "
            "boat tour has operated since 1846, bringing visitors face to face "
            "with the thundering cascade."
        ),
    },
    "iguazu_falls": {
        "a": (
            "Iguazu Falls stretches nearly two miles along the border of Argentina "
            "and Brazil, comprising over two hundred seventy individual waterfalls. "
            "The Guarani people called it the Great Water. Spanish conquistador "
            "Alvar Nunez Cabeza de Vaca was the first European to document the "
            "falls in 1541. The surrounding Atlantic Forest is one of the most "
            "biodiverse regions on the planet."
        ),
        "b": (
            "The Devil's Throat, a U-shaped chasm where fourteen falls converge, "
            "produces a permanent cloud of mist and a thunderous roar audible "
            "miles away. Iguazu is taller than Niagara and roughly twice as wide. "
            "Coatis, toucans, and hundreds of butterfly species inhabit the "
            "surrounding national parks. Eleanor Roosevelt reportedly exclaimed "
            "Poor Niagara upon seeing the falls for the first time."
        ),
    },
    "easter_island": {
        "a": (
            "The Rapa Nui people settled Easter Island around the twelfth century "
            "and carved nearly nine hundred moai statues from volcanic tuff at "
            "the Rano Raraku quarry. The largest completed moai stands over "
            "thirty feet tall and weighs over eighty tonnes. How they transported "
            "these massive figures miles across the island remains a subject "
            "of scholarly debate, with recent experiments suggesting they were "
            "rocked upright and walked."
        ),
        "b": (
            "Nearly four hundred moai remain at the Rano Raraku quarry in various "
            "stages of completion, as if the carvers suddenly stopped work. The "
            "statues originally wore red stone topknots called pukao and had "
            "coral and obsidian eyes. Easter Island is one of the most remote "
            "inhabited places on Earth, located over two thousand miles from the "
            "nearest populated land. The island's original name, Rapa Nui, means "
            "Great Rock."
        ),
    },
    "tikal": {
        "a": (
            "Tikal was one of the largest and most powerful cities of the ancient "
            "Maya civilization, flourishing from roughly 200 to 900 AD in what "
            "is now northern Guatemala. At its peak, the city may have housed "
            "over sixty thousand people. Temple I, known as the Temple of the "
            "Grand Jaguar, rises over one hundred fifty feet above the central "
            "plaza and was built around 734 AD as a funerary temple."
        ),
        "b": (
            "Tikal's temples rise above the jungle canopy, and howler monkeys, "
            "toucans, and spider monkeys inhabit the surrounding rainforest. The "
            "city contains over three thousand structures spread across six "
            "square miles, though much remains unexcavated beneath the jungle. "
            "The site served as a Rebel base in the original Star Wars film. "
            "Sound travels remarkably well across the central plaza — a handclap "
            "at one temple echoes clearly from another."
        ),
    },
    "antelope_canyon": {
        "a": (
            "Antelope Canyon was formed over millions of years as flash floods "
            "carved through Navajo sandstone in northern Arizona. The Navajo "
            "people call it Tse bighanilini, meaning the place where water runs "
            "through rocks. The narrow slot canyon features flowing walls sculpted "
            "by water and wind into undulating curves that glow in shades of "
            "orange, red, and purple."
        ),
        "b": (
            "Light beams that pierce through the narrow openings of Upper "
            "Antelope Canyon occur only from late March to early October when "
            "the sun is high enough. The canyon is located on Navajo Nation land "
            "and can only be visited with a Navajo guide. Flash floods remain "
            "a serious danger; a 1997 flood tragically killed eleven visitors. "
            "Photographers often wait hours for the perfect shaft of light."
        ),
    },
    "monument_valley": {
        "a": (
            "Monument Valley's sandstone buttes formed over millions of years as "
            "layers of sediment were deposited, then eroded by wind and water, "
            "leaving behind the towering formations. The valley lies within the "
            "Navajo Nation on the Arizona-Utah border. The Navajo have lived "
            "in the area for centuries, and it holds deep cultural and spiritual "
            "significance in their traditions."
        ),
        "b": (
            "Monument Valley's iconic silhouette has appeared in more films, "
            "television shows, and advertisements than perhaps any other American "
            "landscape. Director John Ford made it famous through classic westerns "
            "beginning with Stagecoach in 1939. The Mittens, two matching buttes "
            "with thin spires, are the valley's most recognizable formations. "
            "The valley floor sits at over five thousand feet elevation and "
            "receives less than ten inches of rain per year."
        ),
    },
    "yellowstone": {
        "a": (
            "Yellowstone became the world's first national park in 1872, "
            "protecting over two million acres in the Rocky Mountains. The park "
            "sits atop a massive volcanic hotspot that has produced three "
            "cataclysmic eruptions over the past two million years. The most "
            "recent super-eruption, about six hundred forty thousand years ago, "
            "created the park's vast caldera stretching over thirty miles wide."
        ),
        "b": (
            "Yellowstone contains over half of the world's active geysers, "
            "including Old Faithful, which erupts roughly every ninety minutes. "
            "The Grand Prismatic Spring, the largest hot spring in the United "
            "States, gets its rainbow colors from heat-loving bacteria. The park "
            "is home to grizzly bears, wolves, bison, and elk. Its underground "
            "magma chamber could fill the Grand Canyon over eleven times."
        ),
    },
    "sugarloaf_rio": {
        "a": (
            "Sugarloaf Mountain rises over thirteen hundred feet from the mouth "
            "of Guanabara Bay in Rio de Janeiro. The granite monolith formed "
            "over six hundred million years ago through the slow cooling of "
            "magma beneath the Earth's surface. The first recorded ascent was "
            "by British nanny Henrietta Carstairs in 1817, climbing with a "
            "ladder and iron stakes."
        ),
        "b": (
            "The cable car to Sugarloaf's summit has operated since 1912, making "
            "it one of the oldest aerial tramways in the world. The system was "
            "modernized in 1972, and the current cars carry sixty-five passengers "
            "each. Marmosets and numerous bird species inhabit the Atlantic Forest "
            "on the mountain's slopes. The panoramic views from the summit "
            "encompass Copacabana Beach, Christ the Redeemer, and the sprawling "
            "city below."
        ),
    },
    "lake_louise": {
        "a": (
            "Lake Louise was named in 1884 after Princess Louise Caroline Alberta, "
            "the fourth daughter of Queen Victoria. Tom Wilson, a Canadian Pacific "
            "Railway employee, was the first European to see the lake in 1882, "
            "guided there by a Stoney Nakoda man. The turquoise color comes from "
            "glacial rock flour suspended in meltwater from the Victoria Glacier "
            "at the lake's far end."
        ),
        "b": (
            "Lake Louise sits at over five thousand six hundred feet elevation in "
            "Banff National Park. The Fairmont Chateau Lake Louise, originally "
            "a small log cabin built in 1890, has grown into a grand lakeside "
            "hotel. In winter the lake freezes solid and hosts an ice sculpture "
            "festival and outdoor skating rink. The Lake Agnes Tea House above, "
            "accessible only by hiking trail, has served tea to hikers since 1905."
        ),
    },
    "uluru": {
        "a": (
            "Uluru is a sandstone monolith in Australia's Northern Territory, "
            "sacred to the Anangu Aboriginal people for tens of thousands of "
            "years. The rock formed around five hundred million years ago from "
            "sediment deposited by ancient rivers. What visitors see above ground "
            "is only about one third of the total rock formation, with most of "
            "it hidden below the surface."
        ),
        "b": (
            "Uluru stands over eleven hundred feet tall and has a circumference "
            "of nearly six miles. The rock appears to change color throughout "
            "the day, glowing deep red at sunrise and sunset. In October 2019, "
            "climbing Uluru was permanently banned to respect Anangu cultural "
            "traditions. Dozens of springs, waterholes, rock caves, and ancient "
            "paintings around its base hold deep spiritual significance."
        ),
    },
    "tongariro": {
        "a": (
            "Tongariro National Park in New Zealand was the country's first "
            "national park, gifted to the nation in 1887 by Maori chief Te "
            "Heuheu Tukino the Fourth to protect its sacred volcanic peaks. The "
            "park's three active volcanoes — Tongariro, Ngauruhoe, and Ruapehu — "
            "are central to Maori spiritual beliefs. Tongariro became a UNESCO "
            "dual World Heritage Site in 1990 for both natural and cultural "
            "significance."
        ),
        "b": (
            "The Tongariro Alpine Crossing is often called New Zealand's greatest "
            "day hike, covering twelve miles across volcanic terrain. The "
            "Emerald Lakes along the route get their vivid color from dissolved "
            "minerals. Mount Ngauruhoe served as the filming location for Mount "
            "Doom in the Lord of the Rings films. Mount Ruapehu's crater lake "
            "is heated by volcanic activity and can reach temperatures of over "
            "one hundred forty degrees Fahrenheit."
        ),
    },
    "great_barrier_reef": {
        "a": (
            "The Great Barrier Reef began forming around twenty thousand years "
            "ago as sea levels rose after the last ice age and coral colonized "
            "the shallow continental shelf off northeastern Australia. Stretching "
            "over fourteen hundred miles, it is the largest living structure on "
            "Earth, visible from space. Aboriginal and Torres Strait Islander "
            "peoples have lived along the reef for over sixty thousand years."
        ),
        "b": (
            "The Great Barrier Reef comprises nearly three thousand individual "
            "reef systems and over nine hundred islands. It supports over fifteen "
            "hundred species of fish and over four hundred types of coral. The "
            "reef generates billions of dollars annually for Australia's economy "
            "through tourism and fishing. Rising ocean temperatures pose the "
            "greatest threat, causing mass coral bleaching events that have "
            "intensified in recent decades."
        ),
    },
    "bora_bora": {
        "a": (
            "Bora Bora is a volcanic island in French Polynesia surrounded by a "
            "barrier reef and turquoise lagoon. Mount Otemanu, the remnant of "
            "an extinct volcano, rises over two thousand three hundred feet at "
            "its center. Polynesian settlers arrived around the fourth century "
            "AD. During World War Two, the United States established a military "
            "base on the island with over six thousand servicemen."
        ),
        "b": (
            "Bora Bora's lagoon is home to manta rays, sea turtles, and "
            "blacktip reef sharks that swim in shallow, crystal-clear water. The "
            "island pioneered the overwater bungalow concept in the 1960s, which "
            "has since spread to tropical resorts worldwide. The island has no "
            "public transportation; most visitors travel by boat. Bora Bora's "
            "name comes from the Tahitian word Pora Pora, meaning First Born."
        ),
    },
    "burj_khalifa": {
        "a": (
            "The Burj Khalifa in Dubai stands over twenty-seven hundred feet "
            "tall, making it the tallest structure ever built by humans. "
            "Designed by Adrian Smith of Skidmore, Owings and Merrill, "
            "construction took six years and was completed in 2010. The Y-shaped "
            "floor plan was inspired by the Hymenocallis flower and helps reduce "
            "wind forces on the tower."
        ),
        "b": (
            "The Burj Khalifa contains over one hundred sixty floors, fifty-seven "
            "elevators, and over twenty-four thousand glass panels. The building "
            "is so tall that temperatures at the top can be over ten degrees "
            "cooler than at the base. Its observation deck on the 148th floor is "
            "the highest in the world. The tower uses a condensation collection "
            "system that harvests roughly fifteen million gallons of water "
            "annually for landscape irrigation."
        ),
    },
    "wadi_rum": {
        "a": (
            "Wadi Rum, meaning Valley of the Moon in Arabic, has been inhabited "
            "for over twelve thousand years. Nabataean traders left behind "
            "petroglyphs and temple ruins throughout the valley. T. E. Lawrence, "
            "known as Lawrence of Arabia, used Wadi Rum as a base during the "
            "Arab Revolt against the Ottoman Empire in 1917 and described the "
            "landscape as vast, echoing, and godlike."
        ),
        "b": (
            "Wadi Rum's sandstone and granite formations rise up to nearly six "
            "thousand feet from the desert floor. Bedouin communities have lived "
            "in the valley for generations and now host visitors in traditional "
            "camps. The desert served as a filming location for The Martian, "
            "doubling as the surface of Mars. Ancient rock inscriptions in over "
            "twenty-five thousand locations record thousands of years of human "
            "passage through the valley."
        ),
    },
    "sheikh_zayed_mosque": {
        "a": (
            "The Sheikh Zayed Grand Mosque in Abu Dhabi was commissioned by the "
            "late President Sheikh Zayed bin Sultan Al Nahyan and completed in "
            "2007 after twelve years of construction. Over three thousand workers "
            "and thirty-eight contractors from around the world contributed to "
            "the project. The mosque blends Mamluk, Ottoman, and Fatimid "
            "architectural styles using materials from over twenty countries."
        ),
        "b": (
            "The Sheikh Zayed Grand Mosque can accommodate over forty thousand "
            "worshippers. Its main prayer hall contains the world's largest hand-"
            "knotted carpet, covering over sixty thousand square feet and made "
            "by twelve hundred artisans over two years. Seven chandeliers contain "
            "millions of Swarovski crystals. The mosque's eighty-two white marble "
            "domes and over a thousand columns reflect in surrounding pools, "
            "creating a luminous effect at night."
        ),
    },
    "cappadocia": {
        "a": (
            "Cappadocia's fairy chimneys formed over millions of years as volcanic "
            "eruptions blanketed central Turkey in thick layers of soft tuff, "
            "which eroded unevenly beneath harder basalt caps. Early Christians "
            "carved churches, monasteries, and entire underground cities into "
            "the soft rock beginning in the fourth century to shelter from Roman "
            "persecution and later Arab raids."
        ),
        "b": (
            "Cappadocia's underground cities extend as deep as eight levels, with "
            "Derinkuyu capable of sheltering up to twenty thousand people. Each "
            "morning, hundreds of hot air balloons rise over the fairy chimneys "
            "at dawn, creating one of the world's most photographed scenes. The "
            "Goreme Open-Air Museum preserves rock-cut churches with Byzantine "
            "frescoes dating from the tenth to twelfth centuries. UNESCO designated "
            "the region a World Heritage Site in 1985."
        ),
    },
    "northern_lights_iceland": {
        "a": (
            "The Northern Lights, or aurora borealis, occur when charged particles "
            "from the sun interact with gases in Earth's atmosphere along magnetic "
            "field lines near the poles. Iceland's location just below the Arctic "
            "Circle places it in the auroral zone, making it one of the best "
            "places on Earth to witness the phenomenon. Norse mythology attributed "
            "the lights to reflections from the armor of the Valkyries."
        ),
        "b": (
            "Iceland's dark winters from September to March provide ideal viewing "
            "conditions for the Northern Lights. The lights can appear as green, "
            "pink, purple, or red, depending on which atmospheric gas is excited "
            "and at what altitude. Solar activity follows an eleven-year cycle, "
            "with more frequent and vivid displays during solar maximum. The "
            "lights are often visible from Reykjavik itself, but remote areas "
            "away from light pollution offer the most spectacular views."
        ),
    },
    "li_river_guilin": {
        "a": (
            "The Li River flows for over one hundred miles through some of "
            "China's most dramatic karst landscapes in the Guangxi region. The "
            "limestone peaks along its banks formed over three hundred million "
            "years ago from ancient seabeds pushed upward by tectonic forces, "
            "then sculpted by tropical rainfall. Chinese painters have depicted "
            "this scenery for over a thousand years."
        ),
        "b": (
            "The twenty-yuan banknote features the Li River landscape near the "
            "town of Yangshuo. Traditional cormorant fishermen still work the "
            "river at night using trained birds to catch fish by lantern light, "
            "a technique practiced for over a thousand years. The river cruise "
            "from Guilin to Yangshuo passes hundreds of karst peaks, each with "
            "a poetic name inspired by its shape."
        ),
    },
    "mysore_palace": {
        "a": (
            "Mysore Palace was originally built in the fourteenth century as a "
            "wooden structure for the Wadiyar dynasty, rulers of the Kingdom of "
            "Mysore. After a fire destroyed the previous palace in 1897, the "
            "current Indo-Saracenic building was designed by British architect "
            "Henry Irwin and completed in 1912. The Wadiyar rulers commissioned "
            "stained glass, carved doors, and mosaic floors from across the world."
        ),
        "b": (
            "During the annual Dasara festival, Mysore Palace is illuminated "
            "by nearly one hundred thousand light bulbs, transforming it into "
            "a glowing spectacle visible for miles. The palace's Durbar Hall "
            "features ornate ceilings painted with scenes from Hindu mythology. "
            "Mysore Palace is one of India's most visited tourist attractions "
            "after the Taj Mahal, drawing over six million visitors annually."
        ),
    },
    "banaue_rice_terraces": {
        "a": (
            "The Banaue Rice Terraces were carved into the mountains of Ifugao "
            "province in the Philippines by the ancestors of the indigenous "
            "Ifugao people, beginning roughly two thousand years ago. The "
            "terraces follow the natural contours of the Cordillera mountains "
            "and are irrigated by a sophisticated system of channels fed by "
            "rainforests above. If laid end to end, the terraces would stretch "
            "over twelve thousand miles."
        ),
        "b": (
            "The Banaue Rice Terraces are often called the Eighth Wonder of the "
            "World. They were designated a UNESCO World Heritage Site in 1995. "
            "The Ifugao people continue to cultivate rice on these terraces using "
            "traditional methods passed down through generations. The terraces "
            "face threats from erosion and younger generations moving to cities. "
            "Local conservation efforts work to maintain both the physical "
            "structures and the cultural traditions that sustain them."
        ),
    },
}
