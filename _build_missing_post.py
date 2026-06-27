# Republish the one missing article (do-the-hard-thing-after-your-workout) using an existing
# article as the template shell (head/nav/footer/styles), swapping in title + body.
import re
TPL = "articles/how-to-work-out-if-you-have-low-energy.html"
OUT = "articles/do-the-hard-thing-after-your-workout.html"
TITLE = "Do The Hard Thing After Your Workout"
DESC = "A simple strategy: tackle the tasks you've been avoiding right after a workout, when exercise has primed your brain to act. By Dr. Sharon Gam, PhD."

tpl = open(TPL, encoding="utf-8").read()
head = tpl[: tpl.index("<article>")]
foot = tpl[tpl.index("<footer"):]

# swap <title> and meta description in the head
head = re.sub(r"<title>.*?</title>", "<title>" + TITLE + " -- Lifted Strength Club</title>", head, count=1, flags=re.S)
head = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + DESC + m.group(2), head, count=1)
head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + TITLE + m.group(2), head, count=1)

P = lambda t: "<p>" + t + "</p>"
H = lambda t: "<h2>" + t + "</h2>"
body_parts = [
 P("Have you ever had something on your to-do list that you knew would only take five minutes, but you put it off anyway? Maybe it was responding to a text message, making an important phone call, sending an email, or tidying the kitchen."),
 P("The problem usually isn&rsquo;t a lack of time. Most of the tasks we avoid don&rsquo;t take much time at all. The deeper problem is the discomfort that comes with taking action. We avoid things because they feel uncomfortable, scary, awkward, stressful, or overwhelming &mdash; sometimes in ways we don&rsquo;t even realize."),
 P("Recently, I discovered a simple strategy that makes those difficult tasks noticeably easier: I do them immediately after a workout."),
 H("The avoidance issue"),
 P("I have used exercise to manage my depression and anxiety for many years. These days, my main mental-health hurdle isn&rsquo;t depression, it&rsquo;s social anxiety. While that&rsquo;s gotten a lot better, there are still situations that are difficult for me &mdash; two big ones being responding to messages in group chats, and posting my work and marketing my business on social media."),
 P("Both of these activities are important to me. I&rsquo;m in several group chats with friends and family I love and want healthy relationships with, and others with business owners for networking. And while I don&rsquo;t really use social media personally, I want to be active on it for my business."),
 P("Like many people with goals and good intentions, I often struggle to follow through. I used to blame a lack of time, but that&rsquo;s not really true. Over the years I&rsquo;ve built enough self-awareness to know the friction actually comes from fear &mdash; a fear of being judged in public group settings."),
 P("That resistance has held me back, personally and professionally. And the repercussions aren&rsquo;t just about the end result of my inaction &mdash; avoidance in itself damages my mental health. It feeds a vicious cycle: I avoid, then feel bad about avoiding, then the thing seems even more overwhelming, so I avoid again, and feel even worse."),
 H("How I leverage exercise to help my mental health"),
 P("One day I realized there was something I could do. I had a WhatsApp notification from a networking accountability group staring at me every time I looked at my phone. I&rsquo;d read the messages and needed to send my update &mdash; and yet I didn&rsquo;t. Until I got into the gym."),
 P("About halfway through my workout, I picked up my phone to change a song and noticed my hesitation to send the message wasn&rsquo;t as strong as usual. I quickly typed a draft, did another set, re-read it, did another set, re-read it again, did another set, and then hit send."),
 P("I felt so relieved. Knowing what I know about exercise science, it was clear what had happened &mdash; but I was surprised it hadn&rsquo;t previously occurred to me to leverage the brain-changing power of exercise. Once it did, I never looked back. These days, if there&rsquo;s something difficult or scary I need to do, I try to do it immediately after a workout."),
 P("That&rsquo;s not always possible &mdash; for an in-person meeting I&rsquo;ll want time to shower first. But when it involves sending messages or posting online, I can do that whether I&rsquo;m sweaty and out of breath or not."),
 H("The brain-changing power of exercise"),
 P("When you exercise, your muscles release chemicals called myokines that travel throughout your body, including to your brain. At the same time, exercise releases neurotransmitters and other compounds in your brain that can improve mood, motivation, resilience, and mental clarity."),
 P("Scientists call these chemicals &ldquo;hope molecules&rdquo; because of the way they can induce feelings of joy, hope, and social connection. Exercise temporarily changes your brain in ways that make difficult actions feel more manageable &mdash; and those effects generally last at least half an hour, and sometimes a couple of hours, beyond your workout."),
 H("How you can use it"),
 P("If there&rsquo;s something you&rsquo;re avoiding, the period during and immediately after a workout may be the best time to tackle it. Try pairing a workout with:"),
 "<ul><li>Sending a difficult email</li><li>Returning a phone call you&rsquo;ve been avoiding</li><li>Posting on social media</li><li>Scheduling a doctor&rsquo;s appointment</li><li>Completing a job application</li><li>Meal prepping for the week</li><li>Having an important conversation</li><li>Tidying a room</li><li>Tackling a project you&rsquo;ve been procrastinating on</li></ul>",
 P("<strong>Exercise intensity matters.</strong> Higher-intensity exercise (faster or harder cardio, heavier lifting) tends to produce the biggest changes in brain chemistry. If you have the fitness and experience for it, it gives a bigger boost &mdash; if not, work your way up."),
 P("<strong>Don&rsquo;t expect magic.</strong> Even right after a workout, I still triple-check my messages before sending. Exercise doesn&rsquo;t make me a different person who loves group interactions &mdash; but it does let me do what I need to do with less resistance, and feel better about myself in the process."),
 P("The next time you&rsquo;re putting off something important, don&rsquo;t wait until you feel motivated or confident enough. Instead, try scheduling it immediately after your workout. You might still feel nervous. You might still want to procrastinate. But you might also find the resistance is lower and taking action feels just a little easier. Sometimes that&rsquo;s all it takes to get moving."),
 H("If you need help"),
 P("If you have health and fitness goals, learning how to structure them and break them into actionable steps is incredibly important. Have a look through the <a href=\"/guides.html\">free guides</a> &mdash; including the goal-setting guide and the guide to exercise for your mental health."),
]
article = ('<article><div class="art"><div class="artmeta"><span>Mindset</span><span class="rt">4 min read</span></div>'
 '<h1>' + TITLE + '</h1>'
 '<div class="byline">By <b>Dr. Sharon Gam, PhD</b> &middot; CSCS &middot; ACE-HC</div></div>'
 '<div class="art"><div class="prose">' + "".join(body_parts) + '</div></div></article>')

open(OUT, "w", encoding="utf-8").write(head + article + foot)
print("wrote", OUT, "(", len(body_parts), "blocks )")
