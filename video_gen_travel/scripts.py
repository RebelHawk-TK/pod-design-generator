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
}
