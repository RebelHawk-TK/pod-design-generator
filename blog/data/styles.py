"""Art style data for the 6 neural style transfer painting styles."""

STYLES = [
    {
        "key": "starry_night",
        "name": "The Starry Night",
        "artist": "Vincent van Gogh",
        "artist_years": "1853-1890",
        "movement": "Post-Impressionism",
        "painting_year": "1889",
        "description": (
            "Painted in June 1889 from the east-facing window of his asylum room "
            "at Saint-Remy-de-Provence, The Starry Night captures a swirling night "
            "sky over a quiet village. It has become one of the most recognized "
            "paintings in Western art, housed at the Museum of Modern Art in New "
            "York since 1941. The painting blends observed reality with van Gogh's "
            "emotional inner world, transforming a simple nightscape into a cosmic vision."
        ),
        "characteristics": (
            "swirling brushstrokes, bold impasto texture, luminous yellows and "
            "deep blues, rhythmic spiral patterns, dramatic contrast between "
            "the turbulent sky and the calm village below"
        ),
        "collection_handle": "starry-night-collection",
    },
    {
        "key": "great_wave",
        "name": "The Great Wave off Kanagawa",
        "artist": "Katsushika Hokusai",
        "artist_years": "1760-1849",
        "movement": "Ukiyo-e",
        "painting_year": "1831",
        "description": (
            "Published around 1831 as the first print in Hokusai's series "
            "Thirty-six Views of Mount Fuji, The Great Wave off Kanagawa depicts "
            "an enormous wave threatening boats near the Japanese coast with Mount "
            "Fuji rising in the background. Created when Hokusai was about seventy "
            "years old, it is one of the most iconic works of Japanese art and "
            "profoundly influenced European Impressionists during the Japonisme "
            "movement of the late 19th century."
        ),
        "characteristics": (
            "bold outlines, flat areas of color, dynamic wave forms with foaming "
            "crests, Prussian blue and white palette, dramatic sense of scale "
            "and motion, fine linear detail in the water spray"
        ),
        "collection_handle": "the-great-wave-collection",
    },
    {
        "key": "water_lilies",
        "name": "Water Lilies",
        "artist": "Claude Monet",
        "artist_years": "1840-1926",
        "movement": "Impressionism",
        "painting_year": "1906",
        "description": (
            "Water Lilies is part of a series of approximately 250 oil paintings "
            "that Monet created of his flower garden at Giverny during the last "
            "thirty years of his life. The 1906 works mark a pivotal shift toward "
            "larger canvases and an increasingly abstract treatment of the water "
            "surface. These paintings dissolved the boundary between sky and pond, "
            "anticipating the abstract art movements that would follow decades later."
        ),
        "characteristics": (
            "soft dappled brushwork, pastel greens and purples, shimmering "
            "reflections on water, diffused natural light, dissolved edges "
            "between forms, a tranquil and meditative atmosphere"
        ),
        "collection_handle": "water-lilies-collection",
    },
    {
        "key": "the_scream",
        "name": "The Scream",
        "artist": "Edvard Munch",
        "artist_years": "1863-1944",
        "movement": "Expressionism",
        "painting_year": "1893",
        "description": (
            "Created in 1893, The Scream shows a figure on a bridge clutching its "
            "head against a blood-red sky over the Oslofjord. Munch described the "
            "inspiration as a moment when he felt an infinite scream passing through "
            "nature. The composition exists in four versions across paint and pastel, "
            "and has become one of the most universally recognized symbols of modern "
            "anxiety and existential dread."
        ),
        "characteristics": (
            "undulating wavy lines, vivid reds and oranges against dark blues, "
            "distorted forms, raw emotional intensity, stark contrasts, "
            "an unsettling sense of movement rippling through the entire landscape"
        ),
        "collection_handle": "the-scream-collection",
    },
    {
        "key": "cafe_terrace",
        "name": "Cafe Terrace at Night",
        "artist": "Vincent van Gogh",
        "artist_years": "1853-1890",
        "movement": "Post-Impressionism",
        "painting_year": "1888",
        "description": (
            "Painted in September 1888 in Arles, France, Cafe Terrace at Night "
            "was one of the first paintings in which van Gogh used a starry "
            "background. It depicts the terrace of what is now called Cafe Van "
            "Gogh on the Place du Forum. The painting is notable for its warm "
            "artificial lighting against the deep blue night sky, created entirely "
            "on site without the use of black paint."
        ),
        "characteristics": (
            "warm golden yellows from gaslight, cobalt blue night sky with bright "
            "stars, strong perspective lines drawing the eye inward, rich contrast "
            "between warm and cool tones, thick confident brushstrokes, "
            "an inviting nocturnal warmth"
        ),
        "collection_handle": "cafe-terrace-collection",
    },
    {
        "key": "composition_vii",
        "name": "Composition VII",
        "artist": "Wassily Kandinsky",
        "artist_years": "1866-1944",
        "movement": "Abstract Art",
        "painting_year": "1913",
        "description": (
            "Completed in 1913 after more than thirty preparatory studies, "
            "Composition VII is widely considered Kandinsky's masterpiece and one "
            "of the most important abstract paintings ever created. Painted in just "
            "four days, its complex layering of forms draws on themes of resurrection, "
            "judgment, and the flood. Kandinsky believed abstract forms and colors "
            "could express spiritual truths as powerfully as music, and this painting "
            "represents the culmination of that philosophy."
        ),
        "characteristics": (
            "overlapping geometric and organic shapes, vibrant multicolored palette, "
            "energetic diagonal lines, layered transparent forms, a sense of "
            "controlled chaos and rhythmic movement across the canvas"
        ),
        "collection_handle": "composition-vii-collection",
    },
]

STYLES_BY_KEY = {s["key"]: s for s in STYLES}
