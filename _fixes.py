from PIL import Image
from bs4 import BeautifulSoup

# 1) crop Sharon's all-white logo to its content (it's white-on-transparent)
src = r"C:\Users\adina\Downloads\Lifted Strength Club Logo all white transparent background.png"
im = Image.open(src).convert("RGBA")
bbox = im.getchannel("A").getbbox()
im.crop(bbox).save("lifted-logo-white.png")
print("logo:", im.size, "-> cropped", im.crop(bbox).size)

# 2) About page: move the "About Lifted Strength Club" section to the very top
s = BeautifulSoup(open("about.html", encoding="utf-8").read(), "html.parser")
secs = s.find_all("section")
her = secs[0]
studio = next((x for x in secs if "About Lifted Strength Club" in x.get_text()), None)
if studio and studio is not her:
    studio.extract(); her.insert_before(studio)
    open("about.html", "w", encoding="utf-8").write(str(s)); print("about: studio section moved to top")
else:
    print("about: WARNING not reordered")

# 3) Membership: flatten Sharon's accidental nested bullet (a <ul> inside an <li>)
s = BeautifulSoup(open("membership.html", encoding="utf-8").read(), "html.parser")
fixed = 0
for li in s.find_all("li"):
    inner = li.find("ul")
    if inner:
        inner_li = inner.find("li")
        txt = (inner_li.get_text(strip=True) if inner_li else li.get_text(strip=True))
        li.clear(); li.append(txt); fixed += 1
if fixed: open("membership.html", "w", encoding="utf-8").write(str(s))
print("membership: flattened", fixed, "nested bullet(s)")

# 4) Blog: add the do-the-hard-thing card to the journal feed
s = BeautifulSoup(open("blog.html", encoding="utf-8").read(), "html.parser")
feed = s.find(id="feed")
tpl = feed.find("a", class_="card")
new = BeautifulSoup(str(tpl), "html.parser").a
new["href"] = "articles/do-the-hard-thing-after-your-workout.html"
new["data-cat"] = "Mindset"
new.find("img")["src"] = "https://images.squarespace-cdn.com/content/v1/65b7df6a90c12b5744244219/a40f2fbd-2287-499f-96ed-de9b27a3adb1/Sharon+Gam+Personal+Training+2.jpg?format=600w"
m = new.find("div", class_="meta").find_all("span")
m[0].string = "Mindset"; m[1].string = "4 min read"
new.find("h2").string = "Do The Hard Thing After Your Workout"
new.find("p").string = "A simple strategy: tackle the tasks you've been avoiding right after a workout, when exercise has primed your brain to act."
for a in ("data-edit", "data-edit-img"):
    for el in new.find_all(attrs={a: True}): del el[a]
feed.insert(0, new)
open("blog.html", "w", encoding="utf-8").write(str(s)); print("blog: prepended do-the-hard-thing card")
