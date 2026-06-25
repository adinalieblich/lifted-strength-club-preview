# Build two root content pages reusing membership.html's shell (head+style+header / footer)
# so they visually match the rest of the site. Content per Sharon's existing pages.
import re, io

src = open("membership.html", encoding="utf-8").read()
head = src[: src.index("</header>") + len("</header>")]
foot = src[src.index("<footer>"):]

def shell(title, desc, body):
    h = head.replace(
        "<title>Membership &mdash; Lifted Strength Club</title>",
        "<title>%s</title>" % title,
    )
    h = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="%s">' % desc, h, count=1)
    h = h.replace('class="on" href="membership.html"', 'href="membership.html"')
    return h + "\n" + body + "\n" + foot

# ---------- The Science / Mental Health ----------
mh_body = """
<section class="wrap phero"><div class="k">The Science</div>
<h1>Strength training really can <em>improve your mental health</em></h1>
<p>The evidence is strong &mdash; and it shapes how every program at Lifted is built. Here&rsquo;s how lifting changes the brain and the body.</p></section>

<section class="sec"><div class="wrap" style="max-width:840px">
<h2>The research</h2>
<p class="lead">Scientific evidence shows physical activity delivers mental-health benefits comparable to conventional treatments. The 2022 <em>Move Your Mental Health Report</em> reviewed over 1,200 studies from 1990&ndash;2022 and found 89% confirmed a positive link between physical activity and mental health. Of the 48 studies looking specifically at resistance training, 85% identified positive mental-health outcomes.</p>
<p>Research shows exercise substantially reduces depression symptoms &mdash; on par with antidepressants and therapy &mdash; with two or more resistance sessions per week producing meaningful reductions. The same holds for anxiety, benefiting both diagnosed individuals and those with symptoms but no formal diagnosis.</p>

<h2>Changing your brain</h2>
<p>Physical activity triggers the release of endorphins, neurotransmitters, endocannabinoids and neurotrophic factors &mdash; many of them the very targets of psychiatric medication. Scientists call these &ldquo;hope molecules&rdquo; for their capacity to lift optimism and wellbeing.</p>
<p>Regular exercise doesn&rsquo;t just stimulate these receptors, it increases their abundance, making the brain more responsive over time. Brain-derived neurotrophic factor (BDNF) supports the protection, growth and formation of brain cells, and exercise helps regulate the HPA axis that manages stress and inflammation &mdash; typically overactive in anxiety.</p>

<h2>Getting back in touch with your body</h2>
<p>Interoception &mdash; the ability to recognise and interpret your body&rsquo;s signals &mdash; often deteriorates when those signals are dismissed for years. Strength training rebuilds that awareness by demanding attention to movement quality and physical response.</p>
<p>With practice you grow sensitive to changes in heart rate and breathing, which makes it possible to intervene early &mdash; through breathing techniques or cognitive reframing &mdash; when anxiety or low mood begins to surface.</p>

<h2>Creating confidence</h2>
<p>Resistance training builds genuine confidence through &ldquo;mastery experiences&rdquo; &mdash; achieving incremental goals and developing real skill. It teaches patience, persistence and resilience, reinforcing an identity as someone capable of change.</p>
<p>Lifting heavier or completing an extra repetition gives a tangible sense of improvement. Those physical accomplishments become emotional experiences that reinforce capability and determination.</p>

<h2>Getting comfortable with discomfort</h2>
<p>Depression and anxiety encourage avoidance of discomfort, slowly shrinking life&rsquo;s possibilities &mdash; yet growth requires tolerating discomfort. Strength training offers a controlled, safe place to practise navigating it: in the gym, an elevated heart rate and tired muscles have a known, manageable cause.</p>
<p>Repeated exposure normalises that discomfort, transforming it from frightening to manageable &mdash; and that resilience transfers to social and professional challenges in everyday life.</p>

<h2>Changing your thought patterns and self-identity</h2>
<p>Depression and anxiety sustain restrictive stories about what you&rsquo;re capable of. Arguing with those beliefs rarely works &mdash; but behavioural evidence is transformative. Each repetition and improvement quietly contests an unhelpful thought, while the neurochemistry of exercise supports the formation of healthier thinking pathways.</p>

<h2>How we put it to work</h2>
<p>Few trainers build mental health into their programming. The science-backed methods woven through coaching at Lifted include:</p>
<ul>
<li><strong>Intention-setting</strong> &mdash; linking gym achievements to identity change</li>
<li><strong>Ramp-down sets</strong> &mdash; optimising post-workout mood</li>
<li><strong>Time under tension &amp; drop sets</strong> &mdash; building discomfort tolerance</li>
<li><strong>Parasympathetic breathing</strong> &mdash; activating the body&rsquo;s relaxation response</li>
</ul>
</div></section>

<section class="sec"><div class="wrap"><div class="cta">
<h2>Ready to feel it <em>for yourself?</em></h2>
<p>Your first step is a free, no-pressure consultation. We&rsquo;ll talk through your goals and how strength training can support both body and mind.</p>
<a class="btn" href="flagship.html#book">Book a free consult</a></div></div></section>
"""

# ---------- Neural Circuit Symptoms (kept, unlinked) ----------
nc_body = """
<section class="wrap phero"><div class="k">Specialised program</div>
<h1>Strength Training for <em>Neural Circuit Symptoms</em></h1>
<p>A 12-week, self-paced, holistic approach to building strength and healing from dizziness, pain, anxiety and more.</p></section>

<section class="sec"><div class="wrap" style="max-width:840px">
<h2>Don&rsquo;t let your symptoms stand in your way</h2>
<p class="lead">You can become more resilient and train your body and mind to respond to your triggers differently. This isn&rsquo;t a cure (because there&rsquo;s nothing wrong with you) &mdash; it&rsquo;s about building confidence and strengthening your vestibular and stress-response systems while supporting your overall health.</p>

<h2>What&rsquo;s included</h2>
<ul>
<li>12 weeks of expertly designed workouts &mdash; your choice of 2 or 3 sessions per week</li>
<li>Weekly video modules to support habit change and teach you how to rewire your nervous system</li>
<li>Video demonstrations and instructions for every exercise</li>
<li>An eBook with in-depth guidance for getting the most from the program</li>
</ul>
<p><strong>Get started for just $99.</strong> Both the 2&times; and 3&times; per week paths are $99 &mdash; choose what&rsquo;s realistic and sustainable for you. Delivered through the EverFit app.</p>

<h2>Why it works</h2>
<p>Beyond physical conditioning, the program helps rewire the nervous system and address the mindsets that contribute to symptoms, using research-backed neuroplasticity practices. It addresses dizziness, pain and related symptoms through both physical and nervous-system training &mdash; building mental resilience and physical strength over 12 weeks with proper support.</p>

<h2>Frequently asked questions</h2>
<p><strong>What makes this program unique?</strong><br>Beyond physical conditioning, it rewires the nervous system and addresses the mindsets contributing to symptoms, through research-backed neuroplasticity practices.</p>
<p><strong>Can beginners participate?</strong><br>Yes &mdash; it&rsquo;s designed for beginner to intermediate exercisers, or anyone with less than six months of consistent training experience.</p>
<p><strong>Which training frequency should I choose?</strong><br>Both 2 and 3 weekly sessions deliver benefits. Choose what&rsquo;s realistic and sustainable for you.</p>
<p><strong>Are exercise substitutions available?</strong><br>Yes &mdash; alternate exercises are included in the app for equipment or ability adjustments.</p>
<p><strong>What equipment do I need?</strong><br>Basic gym equipment: dumbbells, barbells, a bench, cables, resistance bands and battle ropes.</p>
<p><strong>How long are the workouts?</strong><br>Approximately one hour per session.</p>
<p><strong>Is coaching included?</strong><br>This is a self-guided program; technical app support is provided by EverFit.</p>
</div></section>

<section class="sec"><div class="wrap"><div class="cta">
<h2>Have questions <em>first?</em></h2>
<p>Book a free consultation and we&rsquo;ll talk through whether this program is right for you.</p>
<a class="btn" href="flagship.html#book">Book a free consult</a></div></div></section>
"""

open("mental-health.html", "w", encoding="utf-8").write(
    shell("The Science — Strength Training &amp; Mental Health | Lifted Strength Club",
          "The science of how strength training improves mental health — research, brain chemistry, confidence and resilience. Dr. Sharon Gam, PhD.",
          mh_body))
open("strength-training-neurological-symptoms.html", "w", encoding="utf-8").write(
    shell("Strength Training for Neural Circuit Symptoms | Lifted Strength Club",
          "A 12-week self-paced strength program for dizziness, pain, anxiety and neural circuit symptoms, with Dr. Sharon Gam, PhD.",
          nc_body))
print("built mental-health.html + strength-training-neurological-symptoms.html")
