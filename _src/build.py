#!/usr/bin/env python3
"""Builds philadelphiascalpmicropigmentation.com.
Usage: build.py OUTDIR [--preview]
--preview swaps remote photos for labeled boxes (artifact previews can't load remote images)."""
import os, sys, json, html, re

OUT = sys.argv[1]
PREVIEW = "--preview" in sys.argv
DOMAIN = "philadelphiascalpmicropigmentation.com"
BASE = f"https://{DOMAIN}"
WP = "https://delawarescalpmicropigmentation.com/wp-content/uploads/"
PHONE = "302-292-0380"
TEL = "+13022920380"
STUDIO = "2601 Annand Drive, Unit 16, Wilmington, DE 19808"
MAIL = "1500 Chestnut St #1758, Philadelphia, PA 19102"
MAPS = "https://www.google.com/maps/search/?api=1&query=2601+Annand+Drive+Unit+16+Wilmington+DE+19808"
MAIN = "https://delawarescalpmicropigmentation.com/"
IG = "https://www.instagram.com/delaware_smp/"
DM = "https://ig.me/m/delaware_smp"

IMG = {
 "hero": ("2026/08/best-scalp-micropigmentation-before-and-after-delaware-smp-joey-dots.jpg", "Scalp micropigmentation before and after by Joey Dots"),
 "hairline": ("2026/08/smp-hairline-before-after-wilmington-delaware.jpg", "SMP hairline before and after"),
 "thinning_f": ("2026/08/female-scalp-micropigmentation-before-after-thinning-hair-delaware.jpg", "Female SMP for thinning hair, before and after"),
 "loss": ("2026/08/hair-loss-solution-smp-before-after-joey-saienni-delaware.jpg", "SMP hair loss before and after"),
 "restore": ("2026/04/hairline-restoration-smp-before-after-wilmington-delaware-scaled.webp", "Hairline restoration with SMP, before and after"),
 "thinning": ("2026/04/smp-for-thinning-hair-delaware-before-after-scaled.webp", "SMP density for thinning hair, before and after"),
 "shaved": ("2026/04/shaved-head-smp-before-after-delaware-results-scaled.webp", "Shaved head SMP, before and after"),
 "fue": ("2025/10/FUE-and-SMP-combined-looks-way-better-than-a-hair-transplant-scaled.jpg", "Hair transplant plus SMP density, before and after"),
 "dark": ("2025/10/hairline-restoration-for-dark-skin-men-smp-Natural-Results-scaled.jpg", "Natural SMP hairline on darker skin"),
 "correct": ("2025/10/smp-hairline-correction-delaware-scaled.jpg", "Corrective SMP hairline result"),
 "crown": ("2025/10/IMG_7015-scaled.jpg", "Crown thinning covered with SMP"),
 "close": ("2025/10/Close-Up-SMP-scalp-micropigmentation-on-dark-skin-natural-results.jpg", "Close-up of a healed SMP hairline"),
 "compare": ("2026/04/Before-SMP-and-After-SMP-great-comparison.webp", "Before SMP and after SMP comparison"),
 "joey": ("2026/08/joey-dots-top-rated-smp-practitioner-delaware.jpeg", "Joey Saienni, SMP practitioner at Delaware SMP"),
}

def img(key, cls="", eager=False):
    path, alt = IMG[key]
    if PREVIEW:
        return (f'<div class="ph {cls}" role="img" aria-label="{html.escape(alt)}"><span>Photo from your site:<br>'
                f'{html.escape(path.split("/")[-1])}</span></div>')
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{WP}{path}" alt="{html.escape(alt)}" {load} decoding="async"{" class=%s" % cls if cls else ""}>'

def fig(key, cap):
    return f'<figure>{img(key)}<figcaption>{cap}</figcaption></figure>'

NAV = [("index.html", "Home"), ("results.html", "Results"), ("services.html", "Services"),
       ("pricing.html", "Pricing and FAQ"), ("about.html", "About Joey"), ("getting-here.html", "Getting Here"), ("areas.html", "Areas"), ("blog/index.html", "Blog")]

SCHEMA = {
 "@context": "https://schema.org", "@type": "HealthAndBeautyBusiness",
 "name": "Delaware Scalp Micropigmentation", "alternateName": ["Delaware SMP", "Philadelphia Scalp Micropigmentation"],
 "url": BASE + "/", "telephone": "+1-302-292-0380", "email": "delawaresmp@gmail.com",
 "image": WP + IMG["hero"][0],
 "address": {"@type": "PostalAddress", "streetAddress": "2601 Annand Drive, Unit 16", "addressLocality": "Wilmington",
             "addressRegion": "DE", "postalCode": "19808", "addressCountry": "US"},
 "areaServed": [{"@type": "City", "name": "Philadelphia"}, {"@type": "AdministrativeArea", "name": "Delaware County, PA"},
                {"@type": "AdministrativeArea", "name": "Chester County, PA"}, {"@type": "AdministrativeArea", "name": "Montgomery County, PA"},
                {"@type": "AdministrativeArea", "name": "Bucks County, PA"}, {"@type": "AdministrativeArea", "name": "South Jersey"}],
 "founder": {"@type": "Person", "name": "Joey Saienni", "jobTitle": "President and SMP Practitioner"},
 "sameAs": [MAIN, IG, "https://www.facebook.com/DelawareSMP", "https://www.youtube.com/@dotdattie"],
}

def page(path, title, desc, body, h1=None, sub=None, crumbs=None, noindex=False):
    depth = path.count("/")
    up = "../" * depth
    canon = BASE + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    nav = "".join(f'<a href="{up}{h}">{t}</a>' for h, t in NAV)
    head_block = ""
    if h1:
        cr = f'<p class="crumbs"><a href="{up}index.html">Home</a> / {crumbs}</p>' if crumbs else ""
        head_block = f'<section class="page-head"><div class="wrap">{cr}<h1>{h1}</h1>{f"<p>{sub}</p>" if sub else ""}</div></section>'
    schema = f'<script type="application/ld+json">{json.dumps(SCHEMA)}</script>' if path == "index.html" else ""
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{WP}{IMG['hero'][0]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Oswald:wght@500;600&display=swap">
<link rel="stylesheet" href="{up}style.css">
{'<style>.ph{display:flex;align-items:center;justify-content:center;text-align:center;aspect-ratio:4/5;background:repeating-linear-gradient(45deg,#d9d4ca,#d9d4ca 12px,#cfc9bd 12px,#cfc9bd 24px);color:#3a434c;font-size:13px;padding:12px;border-radius:inherit;word-break:break-word}</style>' if PREVIEW else ''}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{schema}
<header class="site-head">
<div class="wrap">
<a class="brand" href="{up}index.html">Philadelphia Scalp Micropigmentation<small>by Delaware SMP · Joey Dots</small></a>
<nav aria-label="Main">{nav}</nav>
<a class="head-cta" href="tel:{TEL}">Call {PHONE}</a>
</div>
</header>
<main id="main">
{head_block}
{body}
</main>
<footer class="site-foot">
<div class="wrap">
<div>
<h3>Treatment studio</h3>
<p>Delaware Scalp Micropigmentation<br>2601 Annand Drive, Unit 16<br>Wilmington, DE 19808</p>
<p><a href="{MAPS}">Get directions</a></p>
</div>
<div>
<h3>Philadelphia mailing address</h3>
<p>1500 Chestnut St #1758<br>Philadelphia, PA 19102</p>
<p>Mail only. All consults and sessions happen at the Wilmington studio.</p>
</div>
<div>
<h3>Talk to Joey</h3>
<p>Call: <a href="tel:{TEL}">{PHONE}</a></p>
<p>Email: <a href="mailto:delawaresmp@gmail.com">delawaresmp@gmail.com</a></p>
<p>Instagram: <a href="{IG}">@delaware_smp</a></p>
<p>Main site: <a href="{MAIN}">delawarescalpmicropigmentation.com</a></p>
</div>
<p class="legal">Philadelphia Scalp Micropigmentation is a website of Delaware Scalp Micropigmentation (Saienni Success Solutions LLC, DBA Delaware SMP). Results vary from person to person. SMP is a cosmetic tattoo and does not grow hair.</p>
</div>
</footer>
<nav class="mobile-bar" aria-label="Quick contact"><a class="c" href="tel:{TEL}">Call</a><a class="c" href="{DM}">DM</a><a class="t" href="{up}index.html#book">Free consult</a></nav>
</body>
</html>
"""
    doc = re.sub(r"\n{2,}", "\n", doc)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(doc)

def book_section(up=""):
    return f"""
<section class="band dark book" id="book" aria-labelledby="book-h">
<div class="wrap split">
<div>
<p class="eyebrow">Free consultation</p>
<h2 id="book-h">Tell me what's going on with your hair</h2>
<p>Fill this out and I'll get back to you myself. Tell me what you're dealing with: receding hairline, thinning, a transplant that didn't fill in, scars, or old SMP you want fixed. I'll tell you straight if SMP makes sense for you.</p>
<div class="contact-list">
<p>Rather talk now? Call <a href="tel:{TEL}">{PHONE}</a></p>
<p>Or DM me on Instagram: <a href="{DM}">@delaware_smp</a>. That's the fastest way to reach me.</p>
<p>Consults are free. Financing through PayPal Credit and Cherry.</p>
</div>
</div>
<form class="book-form" action="https://formsubmit.co/delawaresmp@gmail.com" method="POST">
<input type="hidden" name="_subject" value="New SMP consult request from {DOMAIN}">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_next" value="{BASE}/thanks.html">
<input type="hidden" name="Website" value="{DOMAIN}">
<input type="hidden" name="Came from" class="src" value="Direct or unknown">
<input type="hidden" name="Page" class="pg" value="">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<div><label for="f-name">Name</label><input id="f-name" name="Name" required autocomplete="name"></div>
<div class="two"><div><label for="f-phone">Phone</label><input id="f-phone" name="Phone" type="tel" required autocomplete="tel"></div>
<div><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div></div>
<div class="two"><div><label for="f-need">What do you want help with?</label><select id="f-need" name="Looking for"><option>Receding hairline</option><option>Thinning hair, want more density</option><option>Fully bald, want a buzz cut look</option><option>Hair transplant scar or thin transplant</option><option>Alopecia</option><option>Fixing old SMP</option><option>Not sure yet</option></select></div>
<div><label for="f-town">Where are you coming from?</label><input id="f-town" name="Town" placeholder="Example: South Philly, Media, Cherry Hill"></div></div>
<div><label for="f-pref">Best way to reach you</label><select id="f-pref" name="Contact preference"><option>Text</option><option>Call</option><option>Email</option></select></div>
<div><label for="f-msg">Anything else? (optional)</label><textarea id="f-msg" name="Message" rows="3"></textarea></div>
<button class="btn" type="submit">Request my free consult</button>
<p class="fine">Goes straight to Joey at Delaware SMP. No spam, no list.</p>
</form>
<script>
(function(){{try{{document.querySelectorAll('.book-form').forEach(function(f){{
{"f.addEventListener('submit',function(e){e.preventDefault();var b=f.querySelector('button');b.textContent='Preview only. Live site sends this to delawaresmp@gmail.com';});" if PREVIEW else ""}
var q=new URLSearchParams(location.search),r=document.referrer,src='Direct or unknown';
if(q.get('utm_source'))src=q.get('utm_source')+(q.get('utm_campaign')?' / '+q.get('utm_campaign'):'');
else if(q.get('gclid'))src='Google Ads';
else if(r){{var h=new URL(r).hostname.replace(/^www\\./,'');if(h!==location.hostname.replace(/^www\\./,''))src=/google\\./.test(h)?'Google search':/instagram\\./.test(h)?'Instagram':/facebook\\.|fb\\./.test(h)?'Facebook':/reddit\\./.test(h)?'Reddit':/bing\\./.test(h)?'Bing':h;}}
try{{var s=sessionStorage.getItem('lead_src');if(s&&src==='Direct or unknown')src=s;else sessionStorage.setItem('lead_src',src);}}catch(e){{}}
f.querySelector('.src').value=src;f.querySelector('.pg').value=location.href.split('#')[0];}});}}catch(e){{}}}})();
</script>
</div>
</section>"""

# ---------------- HOME ----------------
home = f"""
<section class="hero">
<div class="wrap">
<div>
<p class="eyebrow">Scalp micropigmentation for Philadelphia</p>
<h1>Get your hairline back.</h1>
<p class="lead"><strong>31 miles from Philadelphia International Airport (PHL).</strong> I-95 South to Exit 5A-B (DE-141 North), then Kirkwood Highway (DE-2) to Annand Drive. About 40 minutes.</p>
<p class="lead">I'm Joey Saienni, the guy behind Delaware SMP. I've done SMP on 800+ clients over 3,000+ sessions, and a lot of them drive down from Philly, Delco, the Main Line and South Jersey. My studio is at 2601 Annand Drive in Wilmington, Delaware.</p>
<div class="btns"><a class="btn gold" href="#book">Book a free consult</a><a class="btn alt" href="{DM}">DM me on Instagram</a><a class="btn alt" href="results.html">See real results</a></div>
<div class="stats">
<div><strong>800+</strong><span>SMP clients</span></div>
<div><strong>3,000+</strong><span>sessions done</span></div>
<div><strong>10 yrs</strong><span>on my own head</span></div>
</div>
</div>
<div class="hero-form">
<form class="book-form quick" action="https://formsubmit.co/delawaresmp@gmail.com" method="POST">
<p class="qf-title">Free consult. Takes 20 seconds.</p>
<input type="hidden" name="_subject" value="New SMP consult request from {DOMAIN} (quick form)">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_next" value="{BASE}/thanks.html">
<input type="hidden" name="Website" value="{DOMAIN} (home page quick form)">
<input type="hidden" name="Came from" class="src" value="Direct or unknown">
<input type="hidden" name="Page" class="pg" value="">
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<div><label for="q-name">Name</label><input id="q-name" name="Name" required autocomplete="name"></div>
<div><label for="q-phone">Phone</label><input id="q-phone" name="Phone" type="tel" required autocomplete="tel"></div>
<div><label for="q-need">What's going on?</label><select id="q-need" name="Looking for"><option>Receding hairline</option><option>Thinning hair</option><option>Fully bald, want a buzz cut look</option><option>Hair transplant scar or thin transplant</option><option>Alopecia</option><option>Fixing old SMP</option><option>Not sure yet</option></select></div>
<button class="btn gold" type="submit">Get my free consult</button>
<p class="fine">I'll reach out to you myself. No spam.</p>
</form>
</div>
</div>
</section>

<section class="band white">
<div class="wrap">
<p class="eyebrow">What SMP is</p>
<h2>Tiny pigment dots that look like hair follicles</h2>
<div class="split">
<div>
<p>Scalp micropigmentation is a cosmetic tattoo for hair loss. I place thousands of small dots in the top layer of the scalp so it looks like a fresh buzz cut, or so thin spots stop showing through your hair.</p>
<p>No surgery. No pills. No hair system. You walk out and go back to work the same day.</p>
<ul class="checks">
<li>Rebuild a receding or bald hairline</li>
<li>Add density where your hair is thinning</li>
<li>Fill in a hair transplant that came in thin</li>
<li>Hide FUE and FUT scars</li>
<li>Cover alopecia patches</li>
<li>Fix bad SMP from somewhere else</li>
</ul>
<a class="btn" href="services.html">See all services</a>
</div>
<div class="gal" style="margin-top:0">{fig("hero","Full hairline rebuild")}{fig("thinning","Density for thinning hair")}</div>
</div>
</div>
</section>

<section class="band">
<div class="wrap">
<p class="eyebrow">Real clients</p>
<h2>Results from my chair</h2>
<p>Every photo here is my own work at Delaware SMP. No stock photos.</p>
<div class="gal">{fig("hairline","Receding hairline")}{fig("fue","Transplant plus SMP")}{fig("thinning_f","Women's thinning hair")}{fig("dark","Natural hairline")}</div>
<div class="btns"><a class="btn" href="results.html">See more results</a></div>
</div>
</section>
<section class="band dark">
<div class="wrap">
<p class="eyebrow">Why people trust Joey Dots</p>
<div class="grid3">
<div><h3>800+ clients</h3><p>Over 3,000 SMP sessions done at Delaware SMP.</p></div>
<div><h3>I wear it</h3><p>My own SMP is about 10 years old with 12+ sessions. I know how it heals and how it holds up.</p></div>
<div><h3>I teach it</h3><p>I train new SMP artists through the Delaware SMP Training Academy.</p></div>
<div><h3>I talk about it</h3><p>Hair loss and SMP videos on my YouTube channel, <a href="https://www.youtube.com/@dotdattie">Dot Dattie World</a>, and on the Dot Dattie Podcast.</p></div>
<div><h3>Navy veteran</h3><p>I tell you straight, including when SMP isn't right for you.</p></div>
<div><h3>Pay over time</h3><p>Free consults. Financing through PayPal Credit and Cherry.</p></div>
</div>
</div>
</section>


<section class="band white">
<div class="wrap split">
<div>
<p class="eyebrow">Why Philly people make the drive</p>
<h2>One guy, a lot of heads, and I wear it too</h2>
<ul class="checks">
<li>You work with me, not whoever is on shift. I do the consult and I do the work.</li>
<li>800+ clients and 3,000+ sessions. I've seen pretty much every kind of hair loss.</li>
<li>My own SMP is about 10 years old with 12+ sessions. I'm my own experiment, so I know how it holds up.</li>
<li>Free consults, and financing through PayPal Credit and Cherry.</li>
<li>Navy veteran. I tell you straight if SMP isn't right for you.</li>
</ul>
<a class="btn" href="about.html">More about me</a>
</div>
<div>{img("joey")}</div>
</div>
</section>

<section class="band">
<div class="wrap">
<p class="eyebrow">How it works</p>
<h2>From first text to finished hairline</h2>
<ol class="steps narrow">
<li><strong>Free consult.</strong> Come in or send photos. We talk about the hairline you want and what fits your face and age.</li>
<li><strong>Session one.</strong> I lay down the base and the hairline shape. Usually 2 to 4 hours.</li>
<li><strong>Sessions two and three.</strong> Spaced 2 to 3 weeks apart. This is where density gets built and the look gets dialed in.</li>
<li><strong>Healed and done.</strong> Most people are finished in about 5 to 8 weeks. Touch-ups every few years keep it sharp.</li>
</ol>
<p><a href="getting-here.html">How to get to the studio from Philly</a></p>
</div>
</section>
{book_section()}
"""
page("index.html", "Scalp Micropigmentation Philadelphia | Joey Dots at Delaware SMP",
     "Scalp micropigmentation for Philadelphia men and women. 800+ clients, 3,000+ sessions. Free consults, financing. Studio in Wilmington, DE, off I-95 Exit 5A-B, about 31 miles from Philadelphia International Airport. Call 302-292-0380.",
     home)

# ---------------- RESULTS ----------------
results = f"""
<section class="band">
<div class="wrap">
<p>These are my clients. Different ages, skin tones and types of hair loss. Some wanted a full buzz cut look, some just wanted the thin spots to stop showing.</p>
<div class="gal">
{fig("hero","Full hairline rebuild")}
{fig("hairline","Receding hairline")}
{fig("restore","Hairline restoration")}
{fig("shaved","Shaved head look")}
{fig("thinning","Density for thinning hair")}
{fig("thinning_f","Women's thinning hair")}
{fig("fue","Hair transplant plus SMP")}
{fig("crown","Crown thinning")}
{fig("dark","Natural hairline on darker skin")}
{fig("close","Healed hairline up close")}
{fig("correct","Corrective SMP")}
{fig("compare","Before and after")}
{fig("loss","Hair loss to full look")}
</div>
<p style="margin-top:22px">Want to see more? I post new work on Instagram at <a href="{IG}">@delaware_smp</a> and the full gallery is on <a href="{MAIN}gallery/">my main site</a>.</p>
</div>
</section>
{book_section()}
"""
page("results.html", "SMP Before and After Photos | Philadelphia Scalp Micropigmentation",
     "Real scalp micropigmentation before and after photos by Joey Dots at Delaware SMP. Hairlines, thinning hair, transplant scars, alopecia and corrective SMP.",
     results, h1="Real before and afters", sub="My own clients. No stock photos, no filters.", crumbs="Results")

# ---------------- SERVICES ----------------
svc = [
 ("Hairline restoration", "restore", "For a receding or fully bald hairline. I design a hairline that fits your face and your age, not a straight line that screams fake. Most guys go with a short buzz cut look.", MAIN + "smp/"),
 ("Density for thinning hair", "thinning", "You keep your hair longer and I add pigment between the hairs so the scalp stops shining through. You don't have to shave your head for this.", MAIN + "smp-for-thinning-hair/"),
 ("SMP for women", "thinning_f", "Thinning along the part or crown. Done through existing hair so it blends in. Women often come in after trying everything else first.", MAIN + "scalp-micropigmentation-for-women/"),
 ("Hair transplant help", "fue", "Transplant came in thin or left you with scars? SMP fills in the gaps between grafts and can hide healed FUE dots and FUT strip scars.", MAIN + "smp-after-hair-transplant/"),
 ("Alopecia", "crown", "Patches from alopecia can be blended in so they don't stand out. We talk about whether your alopecia is stable enough first.", MAIN + "scalp-micropigmentation-for-alopecia/"),
 ("Fixing bad SMP", "correct", "Too dark, too blurry, hairline in the wrong spot. A lot of bad SMP can be corrected without laser. Send me photos and I'll be honest about what's fixable.", MAIN + "corrective-smp-bad-smp-repair/"),
]
SLUGS = ["hairline-restoration-philadelphia.html","thinning-hair-smp-philadelphia.html","smp-for-women-philadelphia.html",
         "hair-transplant-smp-philadelphia.html","alopecia-smp-philadelphia.html","fix-bad-smp-philadelphia.html"]
cards = "".join(f'<div class="card">{img(k)}<h3 style="margin-top:14px">{t}</h3><p>{d}</p><p><a href="services/{SLUGS[i]}">Learn more</a></p></div>' for i, (t, k, d, u) in enumerate(svc))

SVC_PAGES = [
 ("hairline-restoration-philadelphia.html", "Hairline Restoration with SMP for Philadelphia", "restore",
  "SMP hairline restoration for Philadelphia men with a receding or bald hairline. Joey Dots designs a hairline that fits your face. Free consult. 302-292-0380.",
  "A hairline that fits your face, not a straight line that looks fake.",
  """<p>Most guys who come to me from Philly have the same story. The hairline started going in their twenties, they tried the shampoos and the pills, and now they just want to stop thinking about it.</p>
<h2>How I build a hairline</h2>
<p>I draw it out first so you can see it in the mirror before anything happens. I look at your face shape, your age, and where your hairline would naturally sit. A hairline that looks right at 30 should still look right at 55.</p>
<h2>What it looks like</h2>
<p>Most people go with a short buzz cut look. Done right, it looks like you just left the barber.</p>
<h2>How long it takes</h2>
<p>Usually 3 to 4 sessions, 2 to 3 weeks apart. Each session is about 2 to 4 hours. You can go back to work the same day.</p>"""),
 ("thinning-hair-smp-philadelphia.html", "SMP for Thinning Hair in Philadelphia", "thinning",
  "Scalp micropigmentation density treatment for Philadelphia men with thinning hair. Keep your hair longer and stop the scalp from showing. Free consult.",
  "Keep your hair. Stop the scalp from showing through.",
  """<p>Not everyone wants to shave their head. If your hair is thinning on top or in the crown, I can add pigment between the hairs so the scalp stops shining through.</p>
<h2>Do I have to shave?</h2>
<p>No. Density work is done through your existing hair. You keep your style.</p>
<h2>Who it's for</h2>
<p>Guys with diffuse thinning, a thin crown, or hair that looks fine wet but not under bright lights. It also works alongside a transplant.</p>
<h2>What to expect</h2>
<p>Usually 3 to 4 sessions. Touch-ups every few years keep it sharp.</p>"""),
 ("smp-for-women-philadelphia.html", "Scalp Micropigmentation for Women in Philadelphia", "thinning_f",
  "SMP for Philadelphia women with thinning hair, a widening part, or alopecia. Done through your existing hair so it blends in. Free consult with Joey Dots.",
  "Thinning along the part or crown? SMP blends in under your hair.",
  """<p>Women come to me after trying everything else first: powders, fibers, supplements. SMP adds pigment to the scalp under your hair so the part and crown don't show through.</p>
<h2>Will I have to cut my hair?</h2>
<p>No. For women it's done through your existing hair, and it's meant to blend in, not stand out.</p>
<h2>What it helps with</h2>
<ul class="checks"><li>A widening part</li><li>A see-through crown</li><li>Alopecia patches</li><li>Thinning after hair loss from other causes</li></ul>
<p>We'll talk through your situation at a free consult and I'll tell you straight if it makes sense.</p>"""),
 ("hair-transplant-smp-philadelphia.html", "SMP After a Hair Transplant | Philadelphia", "fue",
  "SMP for Philadelphia hair transplant patients: fill in a thin result and hide healed FUE and FUT scars. Free consult with Joey Dots at Delaware SMP.",
  "Your transplant came in thin, or left scars. SMP fixes the look.",
  """<p>A lot of my clients already had a transplant. Some liked it but wanted it fuller. Some can't stop thinking about the scar.</p>
<h2>Thin results</h2>
<p>Grafts only cover so much. Adding pigment between the transplanted hairs makes the whole area look denser.</p>
<h2>FUE and FUT scars</h2>
<p>Healed FUE dot scars and FUT strip scars can usually be blended in so you can wear your hair short again.</p>
<h2>Timing</h2>
<p>Everything needs to be healed first. Send me photos and when you had the procedure, and we'll pick the right time to start.</p>"""),
 ("alopecia-smp-philadelphia.html", "Alopecia SMP in Philadelphia", "crown",
  "Scalp micropigmentation for alopecia for Philadelphia men and women. Blend in patches so they stop standing out. Free consult with Joey Dots.",
  "Blend alopecia patches in so they stop standing out.",
  """<p>Alopecia patches can make you feel like everyone is looking at your head. SMP can blend those areas in with the rest of your scalp.</p>
<h2>Is my alopecia a fit?</h2>
<p>We talk about how stable it is first. If it's still changing a lot, I'll tell you to wait.</p>
<h2>Men and women</h2>
<p>I work with both. For men it often means a full buzz cut look. For women it's usually blended under existing hair.</p>"""),
 ("fix-bad-smp-philadelphia.html", "Fix Bad SMP | Corrective Scalp Micropigmentation Philadelphia", "correct",
  "Corrective SMP for Philadelphia clients with SMP that's too dark, blurry, or has the hairline in the wrong spot. Send photos to Joey Dots at Delaware SMP.",
  "Too dark, blurry, or the hairline's in the wrong spot? A lot of it can be fixed.",
  """<p>I fix other people's SMP every month. The cheap job looked fine fresh, and six months later the dots spread, the color shifted, or the hairline sits way too low.</p>
<h2>Can it be fixed without laser?</h2>
<p>A lot of the time, yes. Sometimes it needs lightening first. It depends on how dark and how spread out the old work is.</p>
<h2>What to do first</h2>
<p>Send me clear photos from the front, top and sides. I'll be honest about what's fixable and what it will take.</p>""")
]
for f, t, k, d, lead, body in SVC_PAGES:
    others = "".join(f'<li><a href="{f2}">{t2.split("|")[0].strip()}</a></li>' for f2, t2, *_ in SVC_PAGES if f2 != f)
    page(f"services/{f}", f"{t} | Joey Dots", d,
         f'''<section class="band"><div class="wrap split"><div>{body}<div class="btns"><a class="btn gold" href="#book">Book a free consult</a><a class="btn alt" href="../results.html">See results</a></div></div><div>{img(k)}</div></div></section>
<section class="band white"><div class="wrap"><h2>Other things I help with</h2><ul class="checks">{others}</ul><p>Coming from Philly? <a href="../getting-here.html">Exact directions to the studio</a>.</p></div></section>
{book_section()}''',
         h1=t.split("|")[0].strip(), sub=lead, crumbs='<a href="../services.html">Services</a>')
services = f"""
<section class="band"><div class="wrap"><div class="grid3">{cards}</div><p style="margin-top:22px">Looking for microblading or lashes? <a href="permanent-makeup.html">Kelsey does those at the same studio</a>.</p></div></section>
{book_section()}
"""
page("services.html", "SMP Services for Philadelphia | Hairline, Thinning, Scars, Alopecia",
     "Scalp micropigmentation services for Philadelphia clients: hairline restoration, density for thinning hair, SMP for women, transplant scars, alopecia and corrective SMP.",
     services, h1="What I can do for you", sub="Every head is different. These are the main things people come to me for.", crumbs="Services")

# ---------------- PRICING / FAQ ----------------
faqs = [
 ("How much does SMP cost?", "Most full treatments land between $2,000 and $3,500. Smaller areas cost less, bigger areas cost more. I give you an exact price at your free consult."),
 ("Do you offer financing?", "Yes. PayPal Credit and Cherry. Ask about it at your consult."),
 ("How many sessions will I need?", "Usually 3 to 4 sessions, spaced 2 to 3 weeks apart. The whole thing takes about 5 to 8 weeks."),
 ("How long is each session?", "About 2 to 4 hours, depending on the area."),
 ("Does it hurt?", "Everyone's different, but most people say it's more annoying than painful."),
 ("Is it permanent?", "It's considered permanent but it fades some over time. Plan on a touch-up every 2 to 5 years. A touch-up on the same area runs about 25% of the original price."),
 ("Do I have to shave my head?", "Not always. If you're going for a buzz cut look, yes. If you're adding density to thinning hair, you can keep your hair longer."),
 ("Can I go back to work after?", "Same day. Just avoid heavy sweating and getting your scalp wet for 3 to 4 days."),
 ("Will people know?", "Done right, no. It looks like a fresh buzz or like your hair is thicker than it is."),
 ("Is SMP the same as a hair transplant?", "No. A transplant moves real hair around and you hope it grows. SMP is pigment, so you see the result right away. A lot of my clients have done both."),
 ("Can you fix SMP from another shop?", "A lot of the time, yes, without laser. Send me clear photos and I'll tell you what's realistic."),
 ("Can I get SMP if my hair is still shedding?", "If you're shedding a lot right now, from stress, weight loss, a new medication or anything else, see your doctor first and let it settle. SMP covers how your hair looks. It doesn't stop shedding. Once things are stable, we can talk."),
 ("Should I get SMP or a hair transplant?", "Depends on you. A transplant moves real hair and needs donor hair to work with. SMP doesn't, and you see the result right away. Plenty of my clients have done both, with SMP filling in what the transplant couldn't."),
 ("Can I just send photos first?", "Yes. DM me on Instagram at @delaware_smp with photos of the front, top and sides and tell me what's going on."),
 ("Where are you located?", "My studio is at 2601 Annand Drive, Unit 16, Wilmington, DE 19808. From Philadelphia International Airport (PHL) it is about 31 miles: I-95 South to Exit 5A-B, DE-141 North, then Kirkwood Highway to Annand Drive. The Philadelphia address on this site is a mailing address only."),
]
faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
pricing = f"""
<section class="band">
<div class="wrap narrow">
<div class="callout"><strong>Ballpark:</strong> most full treatments are $2,000 to $3,500. Free consult, exact quote, and financing through PayPal Credit and Cherry.</div>
<h2>Cheap SMP costs more later</h2>
<p>I see it every month. Someone pays a few hundred bucks somewhere, the dots blur or turn blue, and now they need it corrected. Fixing bad SMP takes longer than doing it right the first time. Ask whoever you go to how many heads they've done and look at healed work, not just fresh photos.</p>
<h2 style="margin-top:34px">Questions people ask me</h2>
{faq_html}
</div>
</section>
<script type="application/ld+json">{faq_schema}</script>
{book_section()}
"""
page("pricing.html", "SMP Cost in Philadelphia | Pricing, Financing and FAQ",
     "How much scalp micropigmentation costs for Philadelphia clients, how many sessions it takes, financing through PayPal Credit and Cherry, and answers to common SMP questions.",
     pricing, h1="Pricing and FAQ", sub="Straight answers on cost, sessions and what to expect.", crumbs="Pricing and FAQ")

# ---------------- ABOUT ----------------
about = f"""
<section class="band">
<div class="wrap split">
<div>
<h2>I'm Joey. I lost my hair too.</h2>
<p>I got SMP myself about 10 years ago and I've had 12+ sessions on my own head since. I call myself my own experiment. When I tell you how it heals and how it holds up, I'm not reading it off a brochure.</p>
<p>I run Delaware Scalp Micropigmentation in Wilmington. Since opening I've done SMP on 800+ clients and over 3,000 sessions. A lot of them come from Philadelphia and the suburbs.</p>
<p>Before this I was in the Navy, then spent years at JPMorgan Chase. I also train new SMP artists through the Delaware SMP Training Academy, and I talk about hair loss on my YouTube channel, <a href="https://www.youtube.com/@dotdattie">Dot Dattie World</a>.</p>
<p>When you come in, you deal with me. I do the consult, I do the work, and I'll tell you if SMP isn't the right move for you.</p>
<div class="btns"><a class="btn" href="#book">Book a free consult</a><a class="btn alt" href="{MAIN}our-team/">Meet the team</a></div>
</div>
<div>{img("joey")}</div>
</div>
</section>
{book_section()}
"""
page("about.html", "About Joey Saienni (Joey Dots) | SMP Practitioner for Philadelphia",
     "Joey Saienni has done SMP on 800+ clients over 3,000+ sessions and has had his own SMP for about 10 years. Navy veteran. Studio in Wilmington, DE serving Philadelphia.",
     about, h1="About Joey Dots", sub="SMP practitioner, Navy vet, and a client of my own work.", crumbs="About Joey")

# ---------------- GETTING HERE ----------------
here = f"""
<section class="band">
<div class="wrap split">
<div>
<h2>The studio</h2>
<p><strong>Delaware Scalp Micropigmentation</strong><br>2601 Annand Drive, Unit 16<br>Wilmington, DE 19808</p>
<p><a class="btn" href="{MAPS}">Open in Google Maps</a></p>
<p>This is the only place I do consults and sessions. The Philadelphia address on this site (1500 Chestnut St #1758) is for mail only.</p>
</div>
<div>
<h2>From Philly</h2>
<ul class="checks">
<li><strong>Driving from the airport (PHL):</strong> about 31 miles. Google Maps had it at 39 minutes on a weekday morning. Rush hour takes longer.</li>
<li><strong>Train:</strong> SEPTA's Wilmington/Newark Line stops at Churchmans Crossing station, about 4 miles (roughly 8 minutes by car) from the studio.</li>
<li><strong>From the suburbs:</strong> Ardmore is about 38 miles (<a href="main-line-scalp-micropigmentation.html">Main Line directions</a>). Cherry Hill is about 48 miles over the Delaware Memorial Bridge (<a href="south-jersey-scalp-micropigmentation.html">South Jersey directions</a>).</li>
</ul>
<p>Sessions run 2 to 4 hours, so most people make a morning or afternoon of it.</p>
</div>
</div>
</section>
<section class="band white">
<div class="wrap narrow"><div>
<h2>Turn-by-turn from the airport (PHL)</h2>
<ol class="steps">
<li>Leaving Philadelphia International Airport, get on I-95 South.</li>
<li>Stay on I-95 South through Delaware County and into Delaware.</li>
<li>Take Exit 5A-B for DE-141 North.</li>
<li>Follow DE-141 North, then take DE-2 (Kirkwood Highway) to Annand Drive. About 6 miles from the exit.</li>
<li>Pull into Heritage Plaza, 2601 Annand Drive. I'm in Unit 16.</li>
</ol>
<p><a class="btn" href="{MAPS}">Open turn-by-turn in Google Maps</a></p>
</div>
</div>
</section>
<section class="band white">
<div class="wrap">
<h2>Areas I see clients from</h2>
<p>Philadelphia (South Philly, Northeast, Fishtown, Center City, West Philly, Manayunk), Delaware County (Media, Springfield, Upper Darby, Havertown, Chester), Chester County (West Chester, Kennett Square, Exton, Downingtown), the Main Line (King of Prussia, Bryn Mawr, Ardmore, Wayne), Montgomery County, Bucks County, and South Jersey (Cherry Hill, Voorhees, Glassboro).</p>
</div>
</section>
{book_section()}
"""
page("getting-here.html", "Getting to Delaware SMP from Philadelphia | Directions",
     "Directions from Philadelphia to Delaware SMP: I-95 South to Exit 5A-B, DE-141 North, then Kirkwood Highway to 2601 Annand Drive, Wilmington, DE. About 31 miles from Philadelphia International Airport.",
     here, h1="Getting here from Philly", sub="31 miles from Philadelphia International Airport. Exact directions below.", crumbs="Getting Here")

# ---------------- BLOG ----------------
posts = [
 ("cheap-smp-vs-good-smp.html", "Cheap SMP vs good SMP: what the price difference buys you",
  "Why a few hundred dollar SMP job often ends up costing more, and what to look at before you book anyone.",
  """<p>I get messages every month from people who went the cheap route. The story is usually the same. The price looked great, the fresh photos looked fine, and six months later the dots spread, turned bluish, or the hairline sits way too low.</p>
<h2>What you're actually paying for</h2>
<ul class="checks"><li>The right pigment. Regular tattoo ink can shift color over time.</li><li>Depth control. Too deep and the dots blur. Too shallow and they fade fast.</li><li>Hairline design. A hairline that fits your face at 30 and still fits at 55.</li><li>Time. Good SMP is built over 3 to 4 sessions so it heals even.</li></ul>
<h2>What fixing it costs</h2>
<p>Correcting bad SMP takes more time than doing it right once. Sometimes it means lightening or laser first. That's the part people don't budget for.</p>
<h2>What to ask before you book</h2>
<ol class="steps"><li>How many SMP clients have you done?</li><li>Can I see healed results, not just same-day photos?</li><li>Who actually does the work?</li><li>What happens if I need a touch-up?</li></ol>
<p>Most full treatments with me land between $2,000 and $3,500. The consult is free, and I'll give you an exact number.</p>"""),
 ("driving-from-philadelphia-for-smp.html", "Driving from Philadelphia for SMP: what the day looks like",
  "What to expect when you come from Philly to the Wilmington studio for scalp micropigmentation.",
  """<p>A lot of my clients live in Philly and the suburbs. The studio is about 31 miles from Philadelphia International Airport, and almost all of it is I-95 South.</p>
<h2>Getting here</h2>
<p>Take I-95 South to Exit 5A-B (DE-141 North), then Kirkwood Highway (DE-2) to Annand Drive. Google Maps puts it at about an hour at weekday rush hour. If you'd rather not drive, SEPTA's Wilmington/Newark Line stops at Churchmans Crossing, about 4 miles from the studio.</p>
<h2>The consult</h2>
<p>Free. We look at your hair loss, talk about what you want, and I draw out a hairline so you can see it before anything happens. If SMP isn't right for you, I'll tell you.</p>
<h2>Session days</h2>
<p>Each session runs about 2 to 4 hours. Most people need 3 to 4 sessions, 2 to 3 weeks apart. You can go back to work the same day. Just skip the gym and keep your scalp dry for 3 to 4 days.</p>
<h2>Paying for it</h2>
<p>Financing is available through PayPal Credit and Cherry.</p>"""),
 ("hair-shedding-weight-loss-and-smp.html", "Shedding after weight loss? Where SMP fits and where it doesn't",
  "Hair shedding searches are way up. Here's when SMP helps, when to wait, and when to see a doctor first.",
  """<p>More people are asking me about hair shedding than ever, a lot of it after losing weight fast, including on the new weight loss shots. Here's how I look at it.</p>
<h2>See a doctor first</h2>
<p>If your hair is falling out fast right now, talk to your doctor before anything else. Shedding can have a lot of causes, and some of it grows back on its own.</p>
<h2>SMP doesn't stop shedding</h2>
<p>SMP changes how your scalp looks. It doesn't grow hair and it doesn't stop hair from falling out. If we do it while you're still shedding a lot, your coverage can change under it.</p>
<h2>When SMP makes sense</h2>
<p>Once things are stable and the thinning is still there, SMP can add density so the scalp stops showing through. That's the same density work I do for men and women every week.</p>
<h2>Not sure where you're at?</h2>
<p>DM me photos on Instagram at @delaware_smp, or book a free consult. I'll tell you straight if it's time or if you should wait.</p>"""),
 ("smp-after-hair-transplant-philadelphia.html", "SMP after a hair transplant: filling in what didn't grow",
  "How scalp micropigmentation helps after an FUE or FUT transplant, including thin results and scars.",
  """<p>Plenty of my clients already had a transplant. Some loved it but wanted it to look thicker. Some were left with scars they can't stop thinking about.</p>
<h2>Thin transplant results</h2>
<p>Grafts only cover so much. SMP adds pigment between the hairs so the scalp doesn't show through, which makes the transplant look fuller.</p>
<h2>FUE and FUT scars</h2>
<p>Healed FUE dot scars and FUT strip scars can usually be softened with SMP so they blend in when you wear your hair short.</p>
<h2>Timing</h2>
<p>Let everything heal first. Send me photos and tell me when you had the procedure, and we'll figure out the right time to start.</p>"""),
]
cards = "".join(f'<a class="post-card" href="{f}"><h3>{t}</h3><p>{d}</p></a>' for f, t, d, _ in posts)
page("blog/index.html", "SMP Blog for Philadelphia | Philadelphia Scalp Micropigmentation",
     "Straight talk on scalp micropigmentation from Joey Dots: pricing, transplants, and what to expect coming from Philadelphia.",
     f'<section class="band"><div class="wrap"><div class="post-list">{cards}</div></div></section>',
     h1="Blog", sub="Straight talk about SMP and hair loss.", crumbs="Blog")
for f, t, d, b in posts:
    page(f"blog/{f}", f"{t} | Philadelphia Scalp Micropigmentation", d,
         f'<article class="post"><div class="wrap narrow">{b}<div class="btns"><a class="btn" href="../index.html#book">Book a free consult</a></div></div></article>',
         h1=t, crumbs='<a href="index.html">Blog</a>')

# ---------------- AREAS ----------------
AREAS = [
 ("main-line-scalp-micropigmentation.html", "Scalp Micropigmentation for the Main Line",
  "SMP for Main Line men and women from Ardmore, Bryn Mawr, Wayne and King of Prussia. About 38 miles from Ardmore to Delaware SMP. Free consult with Joey Dots.",
  "Ardmore, Bryn Mawr, Wayne, King of Prussia and the rest of the Main Line.",
  """<h2>Getting here from the Main Line</h2>
<ol class="steps">
<li>Take I-476 South (the Blue Route).</li>
<li>Merge onto I-95 South into Delaware.</li>
<li>Take Exit 5A-B for DE-141 North.</li>
<li>Follow DE-141 North, then Kirkwood Highway (DE-2) to 2601 Annand Drive, Unit 16.</li>
</ol>
<p>From Ardmore it's about 38 miles. Google Maps had it at about 56 minutes on a weekday morning.</p>
<h2>What Main Line clients come in for</h2>
<p>Mostly receding hairlines and thinning on top. A lot of guys want it to look like a fresh buzz. A lot of women want the part to stop showing. Some had a transplant and want it to look fuller.</p>"""),
 ("south-jersey-scalp-micropigmentation.html", "Scalp Micropigmentation for South Jersey",
  "SMP for South Jersey men and women from Cherry Hill, Voorhees, Glassboro and nearby. About 48 miles from Cherry Hill to Delaware SMP. Free consult with Joey Dots.",
  "Cherry Hill, Voorhees, Glassboro and the rest of South Jersey.",
  """<h2>Getting here from South Jersey</h2>
<ol class="steps">
<li>Take I-295 South toward the Delaware Memorial Bridge. The bridge has a toll.</li>
<li>Cross into Delaware and follow signs toward I-95 and Wilmington.</li>
<li>Head to DE-141 North, then Kirkwood Highway (DE-2) to 2601 Annand Drive, Unit 16.</li>
</ol>
<p>From Cherry Hill it's about 48 miles. Google Maps had it at about 54 minutes on a weekday morning. Plug the address into your phone for the exact turns.</p>
<h2>What South Jersey clients come in for</h2>
<p>Same as everywhere: receding hairlines, thin crowns, transplant scars, alopecia, and fixing SMP done somewhere else.</p>"""),
]
area_cards = "".join(f'<a class="post-card" href="{f}"><h3>{t}</h3><p>{lead}</p></a>' for f, t, d, lead, b in AREAS)
page("areas.html", "Areas Served | Philadelphia Scalp Micropigmentation",
     "Delaware SMP serves Philadelphia, the Main Line, Delaware County, Chester County, South Jersey and beyond from one studio in Wilmington, DE.",
     f'''<section class="band"><div class="wrap"><div class="post-list"><a class="post-card" href="getting-here.html"><h3>Philadelphia</h3><p>About 31 miles from Philadelphia International Airport. Turn-by-turn directions.</p></a>{area_cards}</div>
<p style="margin-top:22px">Coming from Delaware, Maryland or DC? My main site has pages for you: <a href="{MAIN}">delawarescalpmicropigmentation.com</a>.</p></div></section>
{book_section()}''',
     h1="Where my clients come from", sub="One studio in Wilmington, Delaware. People drive in from all over.", crumbs="Areas")
for f, t, d, lead, b in AREAS:
    page(f, f"{t} | Joey Dots at Delaware SMP", d,
         f'''<section class="band"><div class="wrap split"><div>{b}<div class="btns"><a class="btn gold" href="#book">Book a free consult</a><a class="btn alt" href="{DM}">DM me photos</a></div></div><div>{img("hairline")}</div></div></section>
<section class="band white"><div class="wrap"><h2>What I do</h2><ul class="checks">{"".join(f'<li><a href="services/{x[0]}">{x[1].split("|")[0].strip()}</a></li>' for x in SVC_PAGES)}</ul></div></section>
{book_section()}''',
         h1=t, sub=lead, crumbs='<a href="areas.html">Areas</a>')

# ---------------- PERMANENT MAKEUP ----------------
page("permanent-makeup.html", "Microblading and Lashes at Delaware SMP | Kelsey Tyre",
     "Microblading, brows and lash extensions by Kelsey Tyre of K.A.T Eyes, inside Delaware SMP in Wilmington, DE.",
     f'''<section class="band"><div class="wrap narrow">
<p>SMP is my thing. Brows and lashes are Kelsey's. Kelsey Tyre runs K.A.T Eyes out of the same studio, so if you or someone you bring along wants microblading, brows or lash extensions, she's right here.</p>
<ul class="checks"><li>Microblading and brows</li><li>Lash extensions</li><li>Lash lift and tint</li></ul>
<p>Reach Kelsey directly: call or text <a href="tel:+13025300442">302-530-0442</a>, or DM her on Instagram at <a href="https://www.instagram.com/kat.eyes.bykels/">@kat.eyes.bykels</a>.</p>
<p>Her sites: <a href="https://delawareeyelash.com/">delawareeyelash.com</a> and <a href="https://browandbeautybar.org/">browandbeautybar.org</a>.</p>
<p>Same address: 2601 Annand Drive, Unit 16, Wilmington, DE 19808.</p>
</div></section>
{book_section()}''',
     h1="Brows and lashes at the studio", sub="Microblading and lashes by Kelsey Tyre, inside Delaware SMP.", crumbs="Permanent makeup")

# ---------------- THANKS ----------------
page("thanks.html", "Thanks | Philadelphia Scalp Micropigmentation", "Your consult request was sent.",
     f'<section class="band"><div class="wrap narrow"><h2>Got it.</h2><p>I\'ll get back to you soon. If you want to talk sooner, call <a href="tel:{TEL}">{PHONE}</a> or DM <a href="{IG}">@delaware_smp</a>.</p><p><a class="btn" href="results.html">Look at results while you wait</a></p></div></section>',
     noindex=True)

# ---------------- static files ----------------
import shutil
shutil.copy(os.path.join(os.path.dirname(__file__), "style.css"), os.path.join(OUT, "style.css"))
if not PREVIEW:
    open(os.path.join(OUT, "CNAME"), "w").write(DOMAIN + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    urls = ["", "results.html", "services.html", "pricing.html", "about.html", "getting-here.html", "blog/"] + [f"blog/{p[0]}" for p in posts] + [f"services/{x[0]}" for x in SVC_PAGES] + ["areas.html", "permanent-makeup.html"] + [a[0] for a in AREAS]
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{BASE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("built", OUT, "preview" if PREVIEW else "production")
