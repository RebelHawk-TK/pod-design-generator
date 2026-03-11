#!/usr/bin/env python3
"""Generate project documentation PDFs."""

from fpdf import FPDF
from pathlib import Path
from datetime import date

DOCS_DIR = Path(__file__).parent / "docs"
TODAY = date.today().strftime("%B %d, %Y")


class DocPDF(FPDF):
    """Custom PDF with header/footer branding."""

    def __init__(self, title: str):
        super().__init__()
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Modern Design Concept", align="L")
        self.cell(0, 8, self.doc_title, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 170, 80)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Confidential | {TODAY} | Page {self.page_no()}/{{nb}}", align="C")

    def title_page(self, title: str, subtitle: str):
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 14, title, align="C")
        self.ln(8)
        self.set_draw_color(200, 170, 80)
        self.set_line_width(1)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(10)
        self.set_font("Helvetica", "", 14)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, subtitle, align="C")
        self.ln(30)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 7, f"Modern Design Concept\nmoderndesignconcept.com\n{TODAY}", align="C")

    def section(self, title: str, level: int = 1):
        if level == 1:
            self.ln(6)
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(30, 30, 30)
            self.multi_cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(200, 170, 80)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 100, self.get_y())
            self.ln(4)
        elif level == 2:
            self.ln(4)
            self.set_font("Helvetica", "B", 13)
            self.set_text_color(50, 50, 50)
            self.multi_cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
            self.ln(2)
        else:
            self.ln(2)
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(70, 70, 70)
            self.multi_cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

    def body(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.set_x(10)
        self.multi_cell(190, 5.5, "     - " + text)

    def bold_body(self, label: str, text: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(40, 40, 40)
        self.cell(self.get_string_width(label) + 1, 5.5, label)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)

    def table_row(self, cols: list[str], widths: list[int], bold: bool = False):
        self.set_font("Helvetica", "B" if bold else "", 9)
        self.set_text_color(40, 40, 40)
        if bold:
            self.set_fill_color(240, 235, 220)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=bold, align="L" if i == 0 else "C")
        self.ln()


def generate_mission_statement():
    pdf = DocPDF("Mission Statement")
    pdf.alias_nb_pages()

    # Title page
    pdf.title_page(
        "Mission Statement\n& Business Overview",
        "Automated Print-on-Demand Design\nGeneration & Multi-Platform Publishing"
    )

    # Mission
    pdf.add_page()
    pdf.section("Mission Statement")
    pdf.body(
        "Modern Design Concept exists to democratize art-inspired merchandise by combining "
        "AI-powered design generation with automated multi-platform distribution. We transform "
        "the world's most iconic landmarks into stunning art-style prints, making gallery-quality "
        "artwork accessible to everyone through affordable, on-demand products.\n\n"
        "Our mission is to build a fully automated creative commerce engine that generates, "
        "publishes, and markets thousands of unique designs across every major print-on-demand "
        "marketplace -- without manual intervention."
    )

    # Vision
    pdf.section("Vision")
    pdf.body(
        "To become a leading automated art commerce brand, recognized for bringing "
        "world-class landmark art to everyday products. We envision a future where every "
        "traveler, art lover, and design enthusiast can find a product that captures the "
        "beauty of their favorite place in a timeless artistic style."
    )

    # Values
    pdf.section("Core Values")
    pdf.bullet("Automation First: Every repetitive task should be automated")
    pdf.bullet("Quality at Scale: Thousands of designs, each individually crafted")
    pdf.bullet("Multi-Platform Presence: Meet customers wherever they shop")
    pdf.bullet("Data-Driven: Track everything, optimize continuously")
    pdf.bullet("Security-Conscious: Protect credentials and customer data")
    pdf.ln(4)

    # Business Model
    pdf.section("Business Model")
    pdf.body(
        "Modern Design Concept operates a zero-inventory print-on-demand business. "
        "Designs are generated algorithmically and uploaded to fulfillment partners who "
        "handle printing, shipping, and returns. Revenue comes from the margin between "
        "retail price and production cost."
    )

    pdf.section("Revenue Streams", 2)
    w = [60, 35, 35, 30, 30]
    pdf.table_row(["Platform", "Products", "Price Range", "Margin", "Status"], w, bold=True)
    pdf.table_row(["Printify (via Shopify)", "601", "$4.99-$24.99", "~40%", "Active"], w)
    pdf.table_row(["TeePublic", "67", "$14-$25", "~15%", "Active"], w)
    pdf.table_row(["Pinterest (referral)", "32 pins", "N/A", "Traffic", "Active"], w)
    pdf.table_row(["Instagram Reels", "45 videos", "N/A", "Brand", "Active"], w)
    pdf.table_row(["TikTok", "27 videos", "N/A", "Brand", "Active"], w)
    pdf.table_row(["Redbubble", "158", "$15-$30", "~20%", "Legacy"], w)
    pdf.ln(4)

    # Products
    pdf.section("Product Catalog")
    pdf.body(
        "The product catalog spans three main categories, all featuring landmark "
        "artwork in six distinct art styles inspired by masters like Van Gogh, Monet, "
        "Hokusai, and Munch."
    )
    pdf.section("Product Types", 3)
    pdf.bullet("T-Shirts ($24.99) -- Unisex heavy cotton tee, 15+ color options, S-3XL")
    pdf.bullet("Posters ($19.99) -- Museum-quality matte prints, 8x10 through 24x36")
    pdf.bullet("Stickers ($4.99) -- Die-cut vinyl, weather-resistant, 3x3 to 5x5")
    pdf.ln(2)

    pdf.section("Design Collection", 3)
    pdf.bullet("50 world landmarks across 2 phases (25 per phase)")
    pdf.bullet("6 art styles per landmark = 300 unique landmark designs")
    pdf.bullet("709 template-based t-shirt designs (14 themed categories)")
    pdf.bullet("705 template-based sticker designs")
    pdf.bullet("702 template-based poster designs")
    pdf.bullet("Total: ~2,816 unique product designs")
    pdf.ln(4)

    # Landmarks
    pdf.section("Featured Landmarks")
    pdf.section("Phase 1 (25 Landmarks)", 3)
    pdf.body(
        "Eiffel Tower, Taj Mahal, Colosseum, Great Wall, Notre Dame, Neuschwanstein, "
        "Mount Fuji, Statue of Liberty, Big Ben, Golden Gate Bridge, Leaning Tower of Pisa, "
        "Sagrada Familia, Christ the Redeemer, Machu Picchu, Petra, Angkor Wat, Alhambra, "
        "Brooklyn Bridge, Hagia Sophia, Kremlin, Versailles, Forbidden City, "
        "Cinque Terre, and more."
    )
    pdf.section("Phase 2 (25 Landmarks)", 3)
    pdf.body(
        "Amsterdam Canals, Bagan Temples, Bruges Medieval, Charles Bridge, Chefchaouen, "
        "Edinburgh Old Town, Fushimi Inari, Giant's Causeway, Guanajuato, Hallgrimskirkja, "
        "Ha'penny Bridge, Havana Vieja, Hawa Mahal, Hoi An, Milford Sound, "
        "Mont Saint-Michel, Moraine Lake, Nyhavn, Ponte Vecchio, Rialto Bridge, "
        "Rijksmuseum, Temple Bar, Twelve Apostles, Zanzibar Stone Town."
    )

    # Art Styles
    pdf.section("Art Styles", 2)
    pdf.bullet("Starry Night (Vincent van Gogh) -- Swirling night sky, bold brushstrokes")
    pdf.bullet("The Great Wave (Katsushika Hokusai) -- Japanese woodblock, dramatic waves")
    pdf.bullet("Water Lilies (Claude Monet) -- Impressionist, soft pastels, garden scenes")
    pdf.bullet("The Scream (Edvard Munch) -- Expressionist, vivid colors, emotional intensity")
    pdf.bullet("Sunflowers (Vincent van Gogh) -- Warm golden tones, textured impasto")
    pdf.bullet("Composition (Piet Mondrian) -- Geometric abstraction, primary colors")
    pdf.ln(4)

    # Marketing
    pdf.section("Marketing Channels")
    pdf.bullet("Shopify Storefront (moderndesignconcept.com) -- Primary sales channel")
    pdf.bullet("AI Art Gallery (rebelhawk-tk.github.io/ai-art-gallery) -- Showcase + SEO")
    pdf.bullet("Blog (300 SEO-optimized posts, auto-published 6/week)")
    pdf.bullet("Instagram Reels (landmark promo + travel art videos)")
    pdf.bullet("TikTok (short-form video content)")
    pdf.bullet("Pinterest (product discovery, 32 pins)")
    pdf.bullet("Google Shopping Feed (product listings)")
    pdf.bullet("Telegram Bot (customer/admin notifications)")
    pdf.ln(4)

    # Growth
    pdf.section("Growth Strategy")
    pdf.body(
        "1. Content Velocity: Automated publishing of 6 blog posts and 2 videos per week "
        "builds SEO authority and social presence with zero manual effort.\n\n"
        "2. Platform Expansion: Currently on 6+ platforms with planned expansion to Etsy "
        "and TikTok Shop for marketplace syndication.\n\n"
        "3. Catalog Expansion: 705 sticker designs ready for Printify upload. Additional "
        "landmark phases and art styles can be generated on demand.\n\n"
        "4. Organic Discovery: Blog posts target long-tail keywords like 'Eiffel Tower "
        "Starry Night poster' that have low competition and high purchase intent."
    )

    out = DOCS_DIR / "01_Mission_Statement.pdf"
    pdf.output(str(out))
    print(f"  Generated: {out}")


def generate_technical_breakdown():
    pdf = DocPDF("Technical Architecture")
    pdf.alias_nb_pages()

    pdf.title_page(
        "Technical Architecture\n& System Design",
        "Infrastructure, Automation, and\nIntegration Documentation"
    )

    # System Overview
    pdf.add_page()
    pdf.section("System Overview")
    pdf.body(
        "The Modern Design Concept platform is a Python-based automation system that "
        "generates print-on-demand product designs, uploads them to multiple marketplaces, "
        "publishes SEO content, distributes video across social platforms, and monitors "
        "business operations -- all running autonomously on a macOS workstation via launchd "
        "scheduled services.\n\n"
        "The system is divided into five core subsystems: Design Generation, Upload Pipeline, "
        "Content Marketing, Video Distribution, and Operations & Monitoring."
    )

    # Tech Stack
    pdf.section("Technology Stack")
    w = [50, 60, 80]
    pdf.table_row(["Component", "Technology", "Purpose"], w, bold=True)
    pdf.table_row(["Runtime", "Python 3.9+", "Core application language"], w)
    pdf.table_row(["Image Generation", "Pillow (PIL)", "Design rendering & compositing"], w)
    pdf.table_row(["Video Generation", "FFmpeg + moviepy", "Video compositing & encoding"], w)
    pdf.table_row(["Browser Automation", "Playwright", "Platform uploads (TeePublic, etc.)"], w)
    pdf.table_row(["HTTP Client", "requests", "REST API calls"], w)
    pdf.table_row(["Bot Framework", "python-telegram-bot", "Telegram notifications"], w)
    pdf.table_row(["Dashboard", "Flask + Chart.js", "Analytics visualization"], w)
    pdf.table_row(["Gallery Site", "Next.js 16 + React 19", "Static art gallery"], w)
    pdf.table_row(["Styling", "Tailwind CSS 4", "Gallery UI"], w)
    pdf.table_row(["E-commerce", "Shopify REST/GraphQL", "Product & blog management"], w)
    pdf.table_row(["Scheduling", "macOS launchd", "Automated task execution"], w)
    pdf.table_row(["Credentials", "macOS Keychain", "Encrypted secret storage"], w)
    pdf.table_row(["Email", "Microsoft Graph API", "Inbox monitoring"], w)
    pdf.table_row(["Version Control", "Git + GitHub", "Source management"], w)
    pdf.ln(4)

    # Design Generation
    pdf.section("1. Design Generation Engine")
    pdf.body(
        "The design engine creates three categories of products using a modular generator "
        "architecture. Each generator produces PNG images paired with JSON metadata files "
        "containing title, description, tags, and SEO-optimized content."
    )

    pdf.section("Architecture", 2)
    pdf.body(
        "Entry point: generate.py (CLI)\n"
        "Modules:\n"
        "  src/generators/text_design.py    -- Quote & slogan designs\n"
        "  src/generators/pattern_design.py -- Geometric/abstract patterns\n"
        "  src/generators/niche_design.py   -- 14-theme template system\n"
        "  src/layouts/centered.py          -- Center-aligned layout\n"
        "  src/layouts/stacked.py           -- Multi-line stacked layout\n"
        "  src/layouts/arced.py             -- Curved/arced text layout\n"
        "  src/effects/shadow.py            -- Drop shadow effects\n"
        "  src/effects/gradient.py          -- Color gradient fills\n"
        "  src/effects/shapes.py            -- Decorative shape overlays\n"
        "  src/canvas.py                    -- Image rendering engine\n"
        "  src/fonts.py                     -- Google Fonts management\n"
        "  src/metadata.py                  -- SEO tagging & description"
    )

    pdf.section("Product Specifications", 2)
    w2 = [40, 40, 35, 35, 40]
    pdf.table_row(["Product", "Resolution", "Format", "DPI", "Color Mode"], w2, bold=True)
    pdf.table_row(["T-shirt", "4500x5400", "PNG", "300", "RGBA"], w2)
    pdf.table_row(["Poster", "7200x10800", "PNG", "300", "RGB"], w2)
    pdf.table_row(["Sticker", "3600x3600", "PNG", "300", "RGBA"], w2)
    pdf.ln(2)

    pdf.section("Niche Template System", 2)
    pdf.body(
        "14 themed categories with 50 phrases each = 700 unique templates:\n"
        "Motivational, Funny, Profession, Hobby, Gaming, Fitness, Mom, Dad, "
        "Pets, Coffee, Introvert, Sarcasm, Seasonal, Drinking.\n\n"
        "Each theme has pre-configured fonts, color palettes, and layouts "
        "optimized for its target audience."
    )

    # Landmark Style Transfer
    pdf.section("Landmark Style Transfer", 2)
    pdf.body(
        "A separate neural style transfer pipeline applies famous art styles to "
        "landmark photography. This produces the premium 'art print' collection.\n\n"
        "Phase 1: 25 landmarks x 6 styles = 150 poster + 150 tshirt designs\n"
        "Phase 2: 25 landmarks x 6 styles = 150 poster + 150 tshirt designs\n"
        "Total: 600 landmark art designs\n\n"
        "Each design includes rich metadata: landmark history, art style description, "
        "geographic coordinates, and SEO-optimized tags."
    )

    # Upload Pipeline
    pdf.section("2. Upload Pipeline")
    pdf.body(
        "The upload system uses a modular architecture with platform-specific uploaders "
        "and a central orchestrator. Each platform has its own script, tracker file, "
        "rate limiting, and error handling."
    )

    pdf.section("API-Based Platforms (Fully Automated)", 2)

    pdf.section("Printify", 3)
    pdf.body(
        "Primary fulfillment partner. REST API integration.\n"
        "Flow: Base64 image upload -> Product creation -> Variant assignment -> Publish\n"
        "Blueprints: T-shirt (ID 6), Poster (ID 282), Sticker (ID 600)\n"
        "Rate: 5-second delay between API calls\n"
        "Tracker: uploaded_printify.json\n"
        "Script: upload_printify.py"
    )

    pdf.section("Pinterest", 3)
    pdf.body(
        "Discovery channel via API v5 (OAuth 2.0).\n"
        "Flow: OAuth browser login -> Pin creation -> Board assignment\n"
        "Rate: 240-second delay, 10 pins/day max (sandbox)\n"
        "Tracker: uploaded_pinterest.json\n"
        "Script: upload_pinterest.py"
    )

    pdf.section("Browser-Based Platforms (Playwright)", 2)

    pdf.section("TeePublic", 3)
    pdf.body(
        "Marketplace with browser automation via Playwright.\n"
        "Flow: Login -> Quick Create -> Upload image -> Fill metadata -> Select colors -> Publish\n"
        "Features: Taggle widget for tags, Minicolors for product colors, content flag toggle\n"
        "Rate: 45-second delay, 10-15 designs/day\n"
        "Requires: Mac awake (non-headless browser)\n"
        "Script: upload_teepublic.py"
    )

    pdf.section("Instagram & TikTok", 3)
    pdf.body(
        "Video upload via Playwright browser automation.\n"
        "Flow: Login -> Create Reel/Video -> Upload file -> Add caption -> Share\n"
        "Rate: 120-second delay between uploads\n"
        "Queue: upload_queue.json (250 videos, randomized order)\n"
        "Scripts: upload_instagram.py, upload_tiktok.py"
    )

    pdf.section("Batch Orchestrator", 2)
    pdf.body(
        "Script: batch_upload.py\n"
        "Runs multiple platform uploads in sequence with per-platform limits.\n"
        "Features: Niche-shuffled ordering, report generation, macOS notifications, "
        "retry-failed mode, status dashboard."
    )

    # Content Marketing
    pdf.section("3. Content Marketing System")

    pdf.section("Blog Engine", 2)
    pdf.body(
        "Generates and publishes SEO-optimized blog posts to Shopify.\n\n"
        "Pipeline:\n"
        "  blog/data/landmarks.py    -- 50 landmark definitions\n"
        "  blog/data/styles.py       -- 6 art style definitions\n"
        "  blog/generator.py         -- Cartesian product (300 posts)\n"
        "  blog/templates.py         -- 3 rotating HTML templates\n"
        "  blog/shopify_blog.py      -- Shopify REST API client\n"
        "  generate_blog_posts.py    -- Publishing script\n\n"
        "Each post includes:\n"
        "  - SEO title (~70 chars)\n"
        "  - Meta description (~160 chars)\n"
        "  - Rich HTML with landmark images\n"
        "  - 10 targeted tags\n"
        "  - Social media follow links (Instagram, TikTok, Pinterest)\n\n"
        "Publishing: 2 posts/run, Mon/Wed/Fri = 6/week\n"
        "Total: 300 drafts -> ~50 weeks to publish all"
    )

    pdf.section("Google Shopping Feed", 2)
    pdf.body(
        "Script: generate_google_feed.py\n"
        "Generates XML product feed for Google Merchant Center.\n"
        "Includes: Product data, shipping rates ($4.99 posters/tees, $3.49 stickers), "
        "return policy (30-day), category mappings.\n"
        "Feed URL: rebelhawk-tk.github.io/pod-design-generator/feed/google_shopping_feed.xml\n"
        "Merchant Center Account: 5733510036"
    )

    # Video System
    pdf.section("4. Video Distribution")
    pdf.body(
        "Three types of videos, all in 1080x1920 portrait format (TikTok/Reels optimized):"
    )

    w3 = [45, 25, 25, 30, 65]
    pdf.table_row(["Type", "Duration", "Count", "Generator", "Description"], w3, bold=True)
    pdf.table_row(["Promo", "14s", "50", "generate_videos.py", "Ken Burns on landmark art"], w3)
    pdf.table_row(["Travel Art", "28s", "100", "generate_travel_videos.py", "Narrative + art showcase"], w3)
    pdf.table_row(["Stock Footage", "28s", "100", "stock_compositor.py", "Real footage + art overlay"], w3)
    pdf.ln(2)

    pdf.body(
        "Upload queue: 250 videos in randomized order (upload_queue.json)\n"
        "Schedule: 3 videos per run, Tuesday + Friday at 5:00 AM\n"
        "Platforms: Instagram Reels + TikTok simultaneously"
    )

    # Automation
    pdf.section("5. Automation & Scheduling")
    pdf.body(
        "All automation runs via macOS launchd with plist configuration files "
        "in ~/Library/LaunchAgents/. Each service has a shell wrapper script "
        "that sets up the environment and invokes the Python script."
    )

    w4 = [45, 30, 55, 60]
    pdf.table_row(["Schedule", "Time", "Script", "Action"], w4, bold=True)
    pdf.table_row(["Daily", "2:00 AM", "run_landmark_daily.sh", "Pinterest + Printify uploads"], w4)
    pdf.table_row(["Daily (paused)", "3:00 AM", "run_teepublic_daily.sh", "TeePublic landmark tshirts"], w4)
    pdf.table_row(["Mon/Wed/Fri", "4:00 AM", "run_blog_publish.sh", "Publish 2 blog posts"], w4)
    pdf.table_row(["Tue/Fri", "5:00 AM", "run_video_uploads.sh", "Upload 3 videos"], w4)
    pdf.ln(2)

    pdf.section("Persistent Services", 2)
    w5 = [55, 50, 85]
    pdf.table_row(["Service", "Script", "Purpose"], w5, bold=True)
    pdf.table_row(["Telegram Bot", "telegram_bot.py", "AI assistant via Telegram (Claude CLI)"], w5)
    pdf.table_row(["Email Monitor", "email_monitor.py", "Inbox polling via MS Graph API"], w5)
    pdf.ln(4)

    # Operations
    pdf.section("6. Operations & Monitoring")

    pdf.section("Telegram Bot (Henry)", 2)
    pdf.body(
        "A persistent Telegram bot that forwards messages to the Claude Code CLI "
        "and returns AI-generated responses. Used for:\n"
        "  - Quick project queries from mobile\n"
        "  - Email inbox notifications (new emails forwarded to Telegram)\n"
        "  - Remote status checks\n\n"
        "Architecture: python-telegram-bot v22.5 -> subprocess(claude -p) -> response\n"
        "Security: User ID whitelist (single authorized user)\n"
        "Model: Configurable via /model command (sonnet/opus/haiku)"
    )

    pdf.section("Email Monitor", 2)
    pdf.body(
        "Monitors tom@moderndesignconcept.com via Microsoft Graph API.\n"
        "Polls every 2 minutes for unread emails.\n"
        "Sends Telegram notification with sender, subject, and preview.\n"
        "Authentication: Azure AD OAuth2 client credentials flow.\n"
        "State tracking: .email_monitor_state (seen message IDs)"
    )

    pdf.section("Analytics Dashboard", 2)
    pdf.body(
        "Flask web dashboard at localhost:8050.\n"
        "Metrics: Sales by platform, revenue trends, product popularity.\n"
        "Data source: Shopify REST API.\n"
        "Script: run_dashboard.py"
    )

    # Security
    pdf.section("7. Security Architecture")
    pdf.body(
        "All API credentials are stored in macOS Keychain using the "
        "keychain_config.py helper module. No plaintext secrets exist on disk."
    )

    pdf.section("Credential Storage", 2)
    w6 = [45, 55, 45, 45]
    pdf.table_row(["Config", "Contents", "Access", "Rotation"], w6, bold=True)
    pdf.table_row(["printify", "JWT API token, shop ID", "Keychain", "2031 expiry"], w6)
    pdf.table_row(["shopify", "API token, client secret", "Keychain", "Manual"], w6)
    pdf.table_row(["pinterest", "OAuth tokens", "Keychain", "60-day refresh"], w6)
    pdf.table_row(["pinterest_tokens", "Access + refresh tokens", "Keychain", "Auto-refresh"], w6)
    pdf.table_row(["telegram", "Bot token, user IDs", "Keychain", "Manual"], w6)
    pdf.table_row(["email_monitor", "Azure AD credentials", "Keychain", "Sep 2026"], w6)
    pdf.table_row(["pexels", "API key", "Keychain", "None"], w6)
    pdf.ln(2)

    pdf.section("Security Measures", 2)
    pdf.bullet("macOS Keychain encryption for all credentials (7 configs)")
    pdf.bullet("Subprocess list-based arguments (no shell injection)")
    pdf.bullet("HTTP client log suppression (prevents token leaks)")
    pdf.bullet("User ID whitelist on Telegram bot")
    pdf.bullet(".gitignore covers all sensitive files and session directories")
    pdf.bullet("HTTPS enforced for all external API calls")
    pdf.bullet("Browser sessions in .gitignored directories")
    pdf.ln(4)

    # File Structure
    pdf.section("8. Repository Structure")
    pdf.body(
        "pod-design-generator/\n"
        "  generate.py              CLI entry point\n"
        "  generate_all.py          Bulk generation (700 templates)\n"
        "  keychain_config.py       Secure credential storage\n"
        "  src/                     Core generation engine\n"
        "    generators/            Text, pattern, niche generators\n"
        "    layouts/               Centered, stacked, arced\n"
        "    effects/               Shadow, gradient, shapes\n"
        "    config.py              Product specifications\n"
        "    canvas.py              Image rendering\n"
        "    fonts.py               Font management\n"
        "    metadata.py            SEO tagging\n"
        "  upload_*.py              Platform-specific uploaders (8)\n"
        "  batch_upload.py          Multi-platform orchestrator\n"
        "  blog/                    Blog generation & publishing\n"
        "  video_gen/               Promo video generator\n"
        "  video_gen_travel/        Travel art video generator\n"
        "  google_feed/             Google Shopping feed\n"
        "  dashboard/               Flask analytics dashboard\n"
        "  templates/               Niche JSON configs (14 themes)\n"
        "  run_*.sh                 Automation shell wrappers\n"
        "  telegram_bot.py          Telegram AI interface\n"
        "  email_monitor.py         Email inbox monitor\n"
        "  output/                  Generated assets (~5K files)\n"
        "  logs/                    Service execution logs"
    )

    out = DOCS_DIR / "02_Technical_Architecture.pdf"
    pdf.output(str(out))
    print(f"  Generated: {out}")


def generate_operations_guide():
    pdf = DocPDF("Operations Guide")
    pdf.alias_nb_pages()

    pdf.title_page(
        "Operations &\nStatus Report",
        "Current State, Inventory,\nand Roadmap"
    )

    # Current Status
    pdf.add_page()
    pdf.section("Platform Status Overview")

    w = [45, 30, 35, 40, 40]
    pdf.table_row(["Platform", "Products", "Status", "Upload Method", "Schedule"], w, bold=True)
    pdf.table_row(["Printify", "601", "Active", "REST API", "Daily 2 AM"], w)
    pdf.table_row(["Shopify Store", "601", "Active", "Via Printify", "N/A"], w)
    pdf.table_row(["TeePublic", "67", "Active", "Playwright", "Daily 3 AM*"], w)
    pdf.table_row(["Pinterest", "32 pins", "Sandbox", "API v5", "Daily 2 AM"], w)
    pdf.table_row(["Instagram", "45 videos", "Active", "Playwright", "Tue/Fri 5 AM"], w)
    pdf.table_row(["TikTok", "27 videos", "Active", "Playwright", "Tue/Fri 5 AM"], w)
    pdf.table_row(["Redbubble", "158", "Legacy", "Playwright", "None"], w)
    pdf.table_row(["Society6", "5", "Blocked", "Playwright", "None"], w)
    pdf.table_row(["Blog", "~300 posts", "Active", "Shopify API", "M/W/F 4 AM"], w)
    pdf.ln(2)
    pdf.body("* TeePublic daily schedule paused as of March 9, 2026")

    # Inventory
    pdf.section("Design Inventory")

    pdf.section("Generated Assets", 2)
    w2 = [70, 40, 40, 40]
    pdf.table_row(["Category", "T-shirts", "Posters", "Stickers"], w2, bold=True)
    pdf.table_row(["POD Templates (14 themes)", "709", "702", "705"], w2)
    pdf.table_row(["Landmark Phase 1 (25)", "150", "150", "0"], w2)
    pdf.table_row(["Landmark Phase 2 (25)", "150", "150", "0"], w2)
    pdf.table_row(["TOTAL", "1,009", "1,002", "705"], w2)
    pdf.ln(2)

    pdf.section("Video Assets", 2)
    w3 = [60, 30, 30, 35, 35]
    pdf.table_row(["Type", "Phase 1", "Phase 2", "Duration", "Format"], w3, bold=True)
    pdf.table_row(["Promo", "25", "25", "14 sec", "1080x1920"], w3)
    pdf.table_row(["Travel Art", "50", "50", "28 sec", "1080x1920"], w3)
    pdf.table_row(["Stock Footage", "50", "50", "28 sec", "1080x1920"], w3)
    pdf.table_row(["TOTAL", "125", "125", "", "250 videos"], w3)
    pdf.ln(4)

    # Active Services
    pdf.section("Active Services")

    pdf.section("Scheduled Tasks", 2)
    pdf.body(
        "All tasks run via macOS launchd. Plist files are in ~/Library/LaunchAgents/."
    )
    pdf.bullet("com.moderndesignconcept.pod-upload-landmark-pinterest -- Daily 2:00 AM")
    pdf.bullet("com.moderndesignconcept.pod-upload-teepublic -- Daily 3:00 AM (PAUSED)")
    pdf.bullet("com.moderndesignconcept.blog-publish -- Mon/Wed/Fri 4:00 AM")
    pdf.bullet("com.moderndesignconcept.pod-upload-video-social -- Tue/Fri 5:00 AM")
    pdf.ln(2)

    pdf.section("Persistent Daemons", 2)
    pdf.bullet("com.moderndesignconcept.telegram-bot -- Always-on Telegram bot (Henry)")
    pdf.bullet("com.moderndesignconcept.email-monitor -- Email inbox polling (2-min interval)")
    pdf.ln(4)

    # Key Accounts
    pdf.section("Account & Service Inventory")

    w4 = [50, 80, 60]
    pdf.table_row(["Service", "Account", "Notes"], w4, bold=True)
    pdf.table_row(["Shopify", "moderndesignconcept.com", "Store ID: 4iahhg-sk"], w4)
    pdf.table_row(["Printify", "Shop ID: 26629878", "Shopify-linked"], w4)
    pdf.table_row(["TeePublic", "modern_design_concept", "URL typo (permanent)"], w4)
    pdf.table_row(["Pinterest", "moderndesignconcept", "Sandbox access only"], w4)
    pdf.table_row(["Instagram", "@mdcmoderndesignconcept", "Business account"], w4)
    pdf.table_row(["TikTok", "@moderndesignconcept", "Creator account"], w4)
    pdf.table_row(["GitHub", "RebelHawk-TK", "Gallery + generator repos"], w4)
    pdf.table_row(["Google Merchant", "ID: 5733510036", "Free listings enabled"], w4)
    pdf.table_row(["Azure AD", "MDC Email Monitor app", "Expires Sep 2026"], w4)
    pdf.table_row(["Email", "tom@moderndesignconcept.com", "Microsoft 365"], w4)
    pdf.ln(4)

    # Roadmap
    pdf.section("Roadmap & Pending Tasks")

    pdf.section("Immediate (This Week)", 2)
    pdf.bullet("Upload 705 sticker designs to Printify")
    pdf.bullet("Resume TeePublic daily schedule")
    pdf.bullet("Complete Printify Phase 2 poster/tshirt uploads")
    pdf.ln(2)

    pdf.section("Short-Term (1-4 Weeks)", 2)
    pdf.bullet("Set up gallery.moderndesignconcept.com custom domain")
    pdf.bullet("Create Best Sellers + New Arrivals Shopify collections")
    pdf.bullet("Submit gallery sitemap to Google Search Console")
    pdf.bullet("Connect TikTok Shop to Printify for marketplace syndication")
    pdf.bullet("Re-apply for Pinterest Standard Access (remove sandbox limit)")
    pdf.ln(2)

    pdf.section("Medium-Term (1-3 Months)", 2)
    pdf.bullet("Expand design catalog with new landmark phases or themes")
    pdf.bullet("Add Etsy marketplace integration")
    pdf.bullet("Implement OAuth token rotation automation")
    pdf.bullet("Set up Google Analytics + conversion tracking")
    pdf.bullet("Investigate Society6 platform block resolution")
    pdf.ln(2)

    pdf.section("Long-Term", 2)
    pdf.bullet("Scale to 5,000+ products across 10+ platforms")
    pdf.bullet("Add AI-generated custom designs (customer requests)")
    pdf.bullet("YouTube channel for longer-form travel art content")
    pdf.bullet("Affiliate marketing partnerships with travel bloggers")
    pdf.bullet("International expansion (multi-language listings)")
    pdf.ln(4)

    # Key Metrics
    pdf.section("Key Metrics to Track")
    pdf.bullet("Products listed per platform (target: 1,000+ on Printify)")
    pdf.bullet("Blog posts published (target: 300 total, 6/week)")
    pdf.bullet("Video uploads (target: 250 total across IG + TikTok)")
    pdf.bullet("Organic search impressions (Google Search Console)")
    pdf.bullet("Shopify store sessions and conversion rate")
    pdf.bullet("Revenue per platform per month")

    out = DOCS_DIR / "03_Operations_Guide.pdf"
    pdf.output(str(out))
    print(f"  Generated: {out}")


if __name__ == "__main__":
    print("Generating project documentation PDFs...\n")
    generate_mission_statement()
    generate_technical_breakdown()
    generate_operations_guide()
    print(f"\nAll documents saved to: {DOCS_DIR}/")
