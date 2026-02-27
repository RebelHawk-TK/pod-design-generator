"""HTML blog post templates for landmark + art style content.

Three template variations with different narrative structures,
each producing ~500-800 words of semantic HTML body content.
"""

STORE_URL = "https://modern-design-concept-2.myshopify.com"


def template_a(landmark: dict, style: dict) -> str:
    """Variation A: Starts with landmark hook, then art context."""
    landmark_url = f'{STORE_URL}/collections/{landmark["collection_handle"]}'
    style_url = f'{STORE_URL}/collections/{style["collection_handle"]}'
    fun_fact = landmark["fun_facts"][0] if landmark["fun_facts"] else ""

    return f"""<h2>{landmark["name"]} Through the Lens of {style["name"]}</h2>

<p>
Standing before {landmark["name"]} in {landmark["location"]}, it is impossible not to feel
the weight of history pressing against the present. {landmark["description"]}
But what happens when one of the world's most recognizable structures meets one of art
history's most celebrated visual languages? That question is exactly what drew us to
reimagine {landmark["name"]} through the aesthetic of {style["artist"]}'s
<a href="{style_url}">{style["name"]}</a>.
</p>

<h3>The Story of {landmark["name"]}</h3>

<p>
Located in {landmark["location"]}, {landmark["country"]},
<a href="{landmark_url}">{landmark["name"]}</a> has captivated visitors
since {landmark["year"]}. Its enduring presence speaks to the ambition and artistry of
the people who built it, and the generations who have preserved it. Over the centuries,
it has served as a symbol of cultural identity, architectural innovation, and human
determination. Travelers from every corner of the globe make pilgrimages to stand in its
shadow, each one carrying away a slightly different memory of the experience.
</p>

<p>
Here is something many visitors never learn: {fun_fact}
</p>

<h3>{style["artist"]} and the World of {style["name"]}</h3>

<p>
{style["artist"]} ({style["artist_years"]}) was a defining figure in the
{style["movement"]} movement. Painted in {style["painting_year"]},
{style["name"]} remains one of the most studied and admired works in art history.
{style["description"]}
</p>

<p>
The painting is characterized by {style["characteristics"]}. These visual qualities
have made it a touchstone for artists and designers seeking to understand how color,
form, and emotion intertwine on canvas.
</p>

<h3>When {landmark["name"]} Meets {style["name"]}</h3>

<p>
Neural style transfer is a technique that takes the structural content of one image and
reinterprets it through the visual vocabulary of another. When we applied the textures,
brushwork, and color palette of {style["name"]} to photographs of {landmark["name"]},
the results were striking. The rigid geometry of the architecture dissolved into flowing
strokes and saturated hues, while the landmark's silhouette remained unmistakable.
</p>

<p>
The visual qualities of the original painting — its distinctive textures, palette, and
energy — translate into unexpected details when mapped onto {landmark["name"]}'s surfaces. Stone and steel take on an
organic warmth. Shadows become pools of deep color rather than mere absence of light.
The result is not a copy of either source, but something genuinely new: a conversation
between a place and a painting, mediated by an algorithm that finds harmonies neither
could produce alone.
</p>

<h3>Bring This Fusion Home</h3>

<p>
We have turned these neural style transfer creations into museum-quality prints and
comfortable everyday apparel. Explore our full
<a href="{landmark_url}">{landmark["name"]} collection</a> for every art style
interpretation, or browse the complete
<a href="{style_url}">{style["name"]} collection</a> to see how
{style["artist"]}'s aesthetic transforms landmarks from around the world.
Whether you hang it on your wall or wear it on your back, each piece is a reminder
that art and architecture have always been in dialogue.
</p>"""


def template_b(landmark: dict, style: dict) -> str:
    """Variation B: Starts with art/artist hook, then landmark."""
    landmark_url = f'{STORE_URL}/collections/{landmark["collection_handle"]}'
    style_url = f'{STORE_URL}/collections/{style["collection_handle"]}'
    fun_fact = landmark["fun_facts"][1] if len(landmark["fun_facts"]) > 1 else (
        landmark["fun_facts"][0] if landmark["fun_facts"] else ""
    )

    return f"""<h2>{style["artist"]}'s Vision Meets {landmark["name"]}</h2>

<p>
In {style["painting_year"]}, {style["artist"]} created a painting that would
alter the trajectory of Western art. {style["name"]} did not simply depict a scene;
it reinvented the way artists could communicate feeling through paint. Decades later,
we asked a different kind of question: what would {style["artist"]} have seen in
<a href="{landmark_url}">{landmark["name"]}</a>?
</p>

<h3>Inside {style["name"]}</h3>

<p>
{style["artist"]} ({style["artist_years"]}) worked within the
{style["movement"]} tradition, though the artist's approach often pushed well beyond
its boundaries. {style["description"]}
</p>

<p>
Critics and admirers alike have pointed to the painting's {style["characteristics"]}
as the qualities that give it lasting power. Every reproduction, every reference in
popular culture, only deepens the original's hold on our collective imagination.
The <a href="{style_url}">{style["name"]} collection</a> explores what happens when
that visual language escapes the frame and wraps itself around the real world.
</p>

<h3>A Closer Look at {landmark["name"]}</h3>

<p>
{landmark["name"]} rises from the landscape of {landmark["location"]},
{landmark["country"]}, a monument that has defined its skyline since {landmark["year"]}.
{landmark["description"]} It is a place that rewards repeated visits, revealing new
details with each encounter, whether in person or through photographs.
</p>

<p>
A lesser-known detail adds another layer to its story: {fun_fact}
</p>

<h3>The Transformation: Neural Style Transfer in Action</h3>

<p>
Neural style transfer works by separating an image into its content, the shapes and
structures that make it recognizable, and its style, the textures, colors, and
brushwork that give it character. Our process fed {landmark["name"]}'s architectural
lines into an algorithm trained on {style["name"]}'s visual DNA. The output is a
hybrid image where {style["artist"]}'s palette washes over ancient stone and modern
steel alike.
</p>

<p>
What makes these pieces compelling is the tension between the two sources. The
{style["characteristics"]} clash productively with the precise engineering of
{landmark["name"]}. Straight edges ripple. Flat surfaces bloom with color gradients
that {style["artist"]} might have recognized as kin. The landmark does not disappear
into the painting; instead, both sources assert themselves, creating a visual
negotiation that holds the viewer's attention.
</p>

<h3>Own a Piece of This Collaboration</h3>

<p>
These transformed images are available as premium posters and soft cotton tees.
Visit the <a href="{landmark_url}">{landmark["name"]} collection</a> to see every
artistic reinterpretation of this iconic landmark, or explore the
<a href="{style_url}">{style["name"]} collection</a> for all the world landmarks
rendered in {style["artist"]}'s unmistakable style. Each purchase is a small act of
bringing two great traditions, architecture and fine art, into your daily life.
</p>"""


def template_c(landmark: dict, style: dict) -> str:
    """Variation C: Starts with travel/imagination hook."""
    landmark_url = f'{STORE_URL}/collections/{landmark["collection_handle"]}'
    style_url = f'{STORE_URL}/collections/{style["collection_handle"]}'
    fun_fact = landmark["fun_facts"][-1] if landmark["fun_facts"] else ""

    return f"""<h2>Imagine {landmark["name"]} Painted by {style["artist"]}</h2>

<p>
Picture yourself walking through {landmark["location"]} as the light shifts and the
crowds thin. {landmark["name"]} stands ahead of you, monumental and familiar. Now
imagine the scene transformed: the sky swirls with thick, expressive strokes, the
building's surfaces ripple with unexpected color, and every shadow carries the
signature of <a href="{style_url}">{style["artist"]}</a>. This is the world we
created by merging {landmark["name"]} with the visual language of {style["name"]}.
</p>

<h3>Why {landmark["name"]} Endures</h3>

<p>
Since {landmark["year"]}, <a href="{landmark_url}">{landmark["name"]}</a> has occupied
a singular place in the cultural landscape of {landmark["country"]}. Situated in
{landmark["location"]}, it draws millions of visitors who arrive with expectations
shaped by postcards, films, and the stories of those who came before them.
{landmark["description"]}
</p>

<p>
And then there are the details that surprise even seasoned travelers: {fun_fact}
</p>

<h3>The Art That Inspired the Transformation</h3>

<p>
{style["name"]}, painted in {style["painting_year"]} by {style["artist"]}
({style["artist_years"]}), belongs to the {style["movement"]} movement but transcends
any single label. {style["description"]} The work's {style["characteristics"]} have
inspired countless artists to rethink the relationship between observation and expression.
</p>

<p>
What makes this painting a particularly rich source for style transfer is the way its
visual elements carry emotional weight. Every brushstroke communicates something beyond
the literal subject, and that emotional surplus is exactly what gets transferred when
the algorithm goes to work.
</p>

<h3>Two Icons, One Image</h3>

<p>
Neural style transfer is deceptively simple in concept: take the content of one image
and render it in the style of another. In practice, the results depend enormously on the
pairing. {landmark["name"]} and {style["name"]} turn out to be a remarkable match.
The landmark's bold forms give the algorithm strong contours to work with, while the
painting's {style["characteristics"]} provide a rich visual texture that fills every
surface with life.
</p>

<p>
The transformed image preserves {landmark["name"]}'s proportions and presence while
replacing photographic realism with something more interpretive. Architectural details
become painterly gestures. The sky is no longer a backdrop but an active participant in
the composition. The overall effect is one of recognition and surprise in equal measure:
you know exactly what you are looking at, yet you have never seen it quite like this.
</p>

<h3>Take the Journey Home</h3>

<p>
These art-meets-architecture pieces are ready for your walls and your wardrobe.
Browse the full <a href="{landmark_url}">{landmark["name"]} collection</a> to discover
every style interpretation of this beloved landmark. Or dive into the
<a href="{style_url}">{style["name"]} collection</a> to see {style["artist"]}'s
aesthetic applied to iconic sites across the globe. From poster to tee, each design
captures a moment where two worlds collide and create something worth holding onto.
</p>"""


TEMPLATES = [template_a, template_b, template_c]


def get_template(index: int):
    """Get template function by index (rotates through 3 variations)."""
    return TEMPLATES[index % len(TEMPLATES)]
