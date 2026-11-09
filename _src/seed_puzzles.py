"""Seed puzzle content for riddleverse.com. Re-run safe (overwrites data/puzzles.json and data/library.json)."""
import json, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
START = datetime.date(2026, 11, 9)

# ---------- Daily riddles: (riddle, [accepted answers], [hint1, hint2, hint3], explanation, trivia, difficulty 1-5, category)
RIDDLES = [
 ("I have keys but open no locks. I have space but no room. You can enter, but you can't go inside. What am I?", ["keyboard", "a keyboard", "computer keyboard"], ["I'm something you probably touched in the last hour.", "Every word on this screen passed through me.", "QWERTY."], "A keyboard has keys, a space bar and an Enter key, and none of them are what they sound like.", "The QWERTY layout dates to 1873 and was designed, in part, to keep typewriter arms from jamming.", 2, "wordplay"),
 ("The more you take, the more you leave behind. What am I?", ["footsteps", "steps", "footprints", "footstep"], ["Think about walking.", "Each one you take leaves a mark.", "Sand on a beach shows them clearly."], "Every step you take leaves a footprint behind you.", "A typical person takes around 100 million steps in a lifetime.", 1, "classic"),
 ("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", ["echo", "an echo"], ["You might hear me in a canyon.", "I repeat what you say.", "Hello… hello… hello…"], "An echo repeats sound without a mouth or ears, and travels on the air.", "Echo was a mountain nymph in Greek myth, cursed to only repeat the last words spoken to her.", 2, "classic"),
 ("What has cities but no houses, forests but no trees, and water but no fish?", ["map", "a map", "maps"], ["I fold.", "You'd use me on a road trip, or your phone replaces me.", "I show you where you are."], "A map shows cities, forests and water without containing any of them.", "The oldest known map is a Babylonian clay tablet from around 600 BC.", 2, "classic"),
 ("What can travel around the world while staying in a corner?", ["stamp", "a stamp", "postage stamp", "a postage stamp"], ["Think about mail.", "I'm small, square and sticky.", "I live on the top right of an envelope."], "A postage stamp sits in the corner of an envelope and travels anywhere the letter goes.", "The first adhesive postage stamp, the Penny Black, was issued in Britain in 1840.", 2, "classic"),
 ("I'm tall when I'm young and short when I'm old. What am I?", ["candle", "a candle", "candles"], ["I give light.", "I melt.", "You blow me out on your birthday."], "A candle burns down and gets shorter as it ages.", "Before electric light, a single candle was the standard unit of brightness, hence 'candlepower'.", 1, "kids"),
 ("What gets wetter the more it dries?", ["towel", "a towel", "towels"], ["I hang in a bathroom.", "I'm fluffy.", "You use me after a shower."], "A towel gets wetter as it dries you off.", "Turkish towels from Bursa were the first to use looped pile, in the 18th century.", 1, "kids"),
 ("I have a head and a tail but no body. What am I?", ["coin", "a coin", "coins"], ["I'm metal.", "You flip me to decide things.", "Heads or tails?"], "A coin has a heads side and a tails side and nothing else.", "The phrase 'heads or tails' goes back to Roman coins, which showed a ruler's head and a ship's stern.", 1, "kids"),
 ("What has an eye but cannot see?", ["needle", "a needle", "needles", "hurricane", "a hurricane", "storm", "potato", "a potato"], ["I'm used in sewing.", "Thread goes through my eye.", "Sharp at one end."], "A needle's eye is the hole for the thread. (A hurricane, a potato and a storm also work, and we accept them.)", "Bone needles with eyes have been found that are more than 40,000 years old.", 1, "kids"),
 ("What breaks yet never falls, and what falls yet never breaks?", ["day and night", "day night", "dawn and nightfall", "daybreak and nightfall", "night and day", "day, night"], ["Two answers, one each.", "One happens every morning, the other every evening.", "Daybreak and…"], "Day breaks and night falls.", "At the equator, 'day' and 'night' are almost exactly twelve hours each all year round.", 3, "wordplay"),
 ("I am not alive, but I grow. I don't have lungs, but I need air. I don't have a mouth, but water kills me. What am I?", ["fire", "a fire", "flame", "a flame"], ["I'm hot.", "I'm useful in a fireplace and dangerous in a forest.", "Water puts me out."], "Fire grows, needs oxygen and is extinguished by water.", "Humans have controlled fire for at least a million years.", 2, "classic"),
 ("What has many teeth but cannot bite?", ["comb", "a comb", "combs", "zipper", "a zipper", "saw", "a saw", "gear", "a gear"], ["I'm in your bathroom.", "I help with your hair.", "Run me through tangles."], "A comb has teeth it never bites with. Zippers, saws and gears also qualify, and we accept them.", "The oldest combs found are about 5,000 years old, from Persia.", 1, "kids"),
 ("Forward I am heavy, backward I am not. What am I?", ["ton", "a ton"], ["I'm a unit of weight.", "Spell me backwards.", "Three letters."], "'Ton' spelled backwards is 'not'.", "A metric tonne is 1,000 kg; a US ton is 907 kg; a UK ton is 1,016 kg. Nobody agrees.", 3, "wordplay"),
 ("What word becomes shorter when you add two letters to it?", ["short", "the word short"], ["The answer is a word about length.", "Add 'er'.", "Short + er."], "Add 'er' to 'short' and it becomes 'shorter'.", "English has about 170,000 words in current use; most adults know 20,000–35,000 of them.", 3, "wordplay"),
 ("I have branches but no fruit, trunk or leaves. What am I?", ["bank", "a bank", "banks"], ["Money.", "You might have an account with me.", "I have many locations."], "A bank has branches.", "The word 'bank' comes from the Italian 'banco', the bench moneylenders sat at.", 2, "wordplay"),
 ("What can fill a room but takes up no space?", ["light", "sound", "air", "music"], ["Flip a switch.", "I'm gone the moment you turn me off.", "Sunlight does it too."], "Light fills a room without occupying space. We also accept sound, air and music.", "Light from the sun takes about 8 minutes and 20 seconds to reach your room.", 2, "classic"),
 ("If you drop me I'm sure to crack, but give me a smile and I'll always smile back. What am I?", ["mirror", "a mirror", "mirrors"], ["I show you something familiar.", "Seven years' bad luck.", "Reflect on it."], "A mirror cracks when dropped and reflects your smile.", "Silver-backed glass mirrors were invented in Germany in 1835.", 1, "kids"),
 ("A man looks at a painting and says, 'Brothers and sisters I have none, but that man's father is my father's son.' Who is in the painting?", ["his son", "son", "the man's son", "the speaker's son"], ["Work from the inside out.", "'My father's son', with no siblings, is the speaker himself.", "So the man in the painting's father is the speaker."], "'My father's son' with no siblings is the speaker. So the painting's subject has the speaker as a father: it's his son.", "This riddle has been printed since at least 1850 and still trips most people up on the first read.", 4, "logic"),
 ("What has one head, one foot and four legs?", ["bed", "a bed", "beds"], ["You spend a third of your life here.", "Head, foot and legs are parts of furniture.", "Sleep on it."], "A bed has a headboard, a footboard and four legs.", "The average person spends about 26 years of their life asleep.", 2, "kids"),
 ("I shave every day, but my beard stays the same. What am I?", ["barber", "a barber", "barbers"], ["It's a job.", "Other people's beards.", "Chair, cape, clippers."], "A barber shaves others every day.", "The barber's pole's red and white stripes date from when barbers also performed bloodletting.", 2, "classic"),
 ("What goes up but never comes down?", ["age", "your age", "my age"], ["Everyone has one.", "It increases every birthday.", "You can't get younger."], "Your age only ever increases.", "The oldest verified human lifespan is 122 years and 164 days.", 1, "kids"),
 ("I have lakes with no water, mountains with no stone and cities with no buildings. What am I?", ["map", "a map", "globe", "a globe"], ["I'm flat, or round if I'm fancy.", "North is usually at the top.", "Unfold me."], "A map (or globe) depicts lakes, mountains and cities.", "Mercator's 1569 projection makes Greenland look as big as Africa; Africa is 14 times larger.", 2, "classic"),
 ("What is seen in the middle of March and April that can't be seen at the beginning or end of either month?", ["the letter r", "r", "letter r", "an r"], ["Look at the words, not the calendar.", "M-A-R-C-H. A-P-R-I-L.", "One letter they share in the middle."], "The letter R is in the middle of 'March' and 'April'.", "In many English dialects, R at the end of a word isn't pronounced at all, which is why 'car' and 'ca' can sound alike.", 3, "wordplay"),
 ("You see a boat filled with people. It has not sunk, but when you look again you don't see a single person on the boat. Why?", ["they are all married", "all married", "everyone is married", "they're married", "married", "no single people", "none of them are single"], ["Read the question again, slowly.", "What's another meaning of 'single'?", "Nobody on the boat is single…"], "Every person on the boat is married, so there isn't a single person aboard.", "The world's largest cruise ship carries nearly 10,000 people, crew included.", 4, "wordplay"),
 ("What has a neck but no head, and wears a cap?", ["bottle", "a bottle", "bottles"], ["I hold liquid.", "I can be glass or plastic.", "Twist my cap off."], "A bottle has a neck and a cap.", "The crown bottle cap was patented in 1892 and is still used today.", 1, "kids"),
 ("I am an odd number. Take away a letter and I become even. What number am I?", ["seven", "7"], ["Spell the number out.", "Remove the first letter.", "S-even."], "'Seven' minus the S is 'even'.", "Seven is the most common 'random' number people pick when asked for a number between 1 and 10.", 3, "math"),
 ("Two fathers and two sons go fishing. Each catches one fish, yet they bring home only three fish. How?", ["grandfather father and son", "grandfather, father, son", "three people", "they are grandfather father and son", "there are only three people", "a grandfather his son and his grandson", "grandfather father son"], ["Count the people, not the roles.", "One person can be both a father and a son.", "Three generations."], "A grandfather, his son and his grandson: two fathers and two sons, but three people.", "The oldest fishing hooks ever found are about 23,000 years old, from Okinawa.", 3, "logic"),
 ("What building has the most stories?", ["library", "a library", "the library", "libraries"], ["Not 'storeys'.", "It's full of books.", "Shh."], "A library has the most stories (books), not storeys (floors).", "The Library of Congress holds about 175 million items on roughly 838 miles of shelving.", 2, "wordplay"),
 ("I can be cracked, made, told and played. What am I?", ["joke", "a joke", "jokes"], ["I'm meant to be funny.", "Knock knock.", "Punchline."], "You can crack, make, tell and play a joke.", "The oldest recorded joke, from Sumer around 1900 BC, is a fart joke.", 2, "classic"),
 ("What runs all around a backyard yet never moves?", ["fence", "a fence", "fences"], ["I'm wooden or wire.", "I mark a boundary.", "Good ones make good neighbours."], "A fence runs around the yard without moving.", "The 'good fences make good neighbors' line comes from Robert Frost's 1914 poem 'Mending Wall', which argues the opposite.", 1, "kids"),
 ("A woman shoots her husband, then holds him under water for five minutes. Next she hangs him. Right after, they enjoy a lovely dinner. How?", ["she is a photographer", "photographer", "photography", "she took his photo", "she's a photographer", "she took a photograph", "developing a photo", "photo"], ["Nobody is hurt.", "Think darkroom.", "Shoot, develop, hang to dry."], "She's a photographer: she shoots a photo, develops it in water, and hangs it to dry.", "The first photograph of a person was taken in Paris in 1838; the man was getting his boots shined.", 4, "logic"),
]

# ---------- Rebus: (emoji string, [answers], [hints], explanation, difficulty)
REBUS = [
 ("🐝 + 🍃", ["believe", "be leaf"], ["Say the pictures out loud.", "Bee… leaf…", "I do."], "Bee + leaf = 'believe'.", 1),
 ("🌧️ + 🏹", ["rainbow", "rain bow"], ["Rain plus something you shoot with.", "After a storm.", "Seven colours."], "Rain + bow = 'rainbow'.", 1),
 ("🚗 + 🐧", ["carpenguin", "car penguin", "car pet", "carpet"], ["Car + the first syllable of the bird.", "Something on the floor.", "Car-pe(nguin)."], "Car + pen(guin) = 'carpet'.", 3),
 ("🔥 + 🧯 ➡️ 🫖", ["fire kettle", "kettle", "put the kettle on"], ["Think British.", "What you do before tea.", "Put the… on."], "Fire out, then put the kettle on.", 3),
 ("👁️ + 🌊", ["eyesea", "icy", "i see", "eye sea"], ["Say it out loud.", "'I understand'.", "Eye… sea…"], "Eye + sea = 'I see'.", 1),
 ("🧊 + 🧊 + 🧊 ➡️ ⛸️", ["ice skating", "skating", "ice skate", "ice skates"], ["Lots of ice, then…", "A winter sport.", "Blades on your feet."], "Ice, ice, ice, then skates: ice skating.", 1),
 ("🌞 + 🌻", ["sunflower", "sun flower"], ["Say both.", "It follows the sun.", "Yellow petals."], "Sun + flower = 'sunflower'.", 1),
 ("📚 + 🐛", ["bookworm", "book worm"], ["Someone who reads a lot.", "Book + …", "A nickname for a keen reader."], "Book + worm = 'bookworm'.", 1),
 ("🧠 + 🌩️", ["brainstorm", "brain storm", "brainstorming"], ["What you do in a meeting.", "Brain + weather.", "Ideas, fast."], "Brain + storm = 'brainstorm'.", 1),
 ("🍯 + 🌙", ["honeymoon", "honey moon"], ["After a wedding.", "Honey + …", "A trip for two."], "Honey + moon = 'honeymoon'.", 1),
 ("⏰ + 🐝", ["alarm bee", "to be", "2 b", "2b", "to bee"], ["It's not the obvious word.", "Say the time and the bug.", "…or not to be."], "A clock showing 2 + bee = '2 B' = 'to be'.", 4),
 ("🐱 + 🐟 ➡️ 🎣", ["catfish", "cat fish", "catfishing"], ["A fish with whiskers, or an online deception.", "Cat + fish.", "Also a dating-app warning."], "Cat + fish = 'catfish'.", 2),
 ("🌍 + 🥤", ["world cup", "worldcup"], ["A tournament.", "World + what you drink from.", "Every four years."], "World + cup = 'World Cup'.", 2),
 ("🔑 + ⌨️", ["keyboard", "key board"], ["Key + …", "You type on it.", "QWERTY."], "Key + board = 'keyboard'.", 1),
 ("🦶 + ⚽", ["football", "foot ball", "soccer"], ["The world's game.", "Foot + ball.", "Also called soccer."], "Foot + ball = 'football'.", 1),
 ("🧈 + 🪰", ["butterfly", "butter fly"], ["An insect.", "Butter + …", "It was a caterpillar."], "Butter + fly = 'butterfly'.", 1),
 ("🌧️ + ✔️", ["raincheck", "rain check"], ["An American idiom.", "'Can I take a…'", "Postpone politely."], "Rain + check = 'rain check'.", 2),
 ("🐴 + 👟", ["horseshoe", "horse shoe"], ["Lucky.", "Horse + …", "Hang it above the door."], "Horse + shoe = 'horseshoe'.", 1),
 ("🌟 + 🐟", ["starfish", "star fish"], ["Lives in the sea.", "Star + fish.", "Five arms."], "Star + fish = 'starfish'.", 1),
 ("🍳 + 🏠", ["eggplant", "pan house", "egg house", "greenhouse", "house egg"], ["Not what you cook, but where.", "Think of the pan's contents and a building.", "Aubergine."], "Egg + plant (a plant-house is a greenhouse, but the intended answer is 'eggplant': egg + (plant)). We accept eggplant.", 3),
 ("🧊 + 🍦", ["ice cream", "icecream"], ["Dessert.", "Ice + …", "Scoops."], "Ice + cream = 'ice cream'.", 1),
 ("👂 + 💍", ["earring", "ear ring"], ["Jewellery.", "Ear + ring.", "Pierced."], "Ear + ring = 'earring'.", 1),
 ("🚪 + 🔔", ["doorbell", "door bell"], ["Ding dong.", "Door + bell.", "Press it."], "Door + bell = 'doorbell'.", 1),
 ("🧲 + 🎥 ➡️ 🎬", ["attraction", "magnetic film", "attractive movie", "blockbuster"], ["What a magnet does, in a cinema.", "Also what you feel for someone.", "Main… "], "Magnet (attraction) + film = 'main attraction' / 'attraction'. We accept 'attraction'.", 4),
 ("🐍 + 👁️", ["snake eyes", "snakeeyes", "snake eye"], ["Dice.", "Two ones.", "Snake + …"], "Snake + eyes = 'snake eyes', a roll of double ones.", 2),
 ("🧍 + 🟰 + 🧍", ["equality", "equal", "equals", "we are equal", "equal rights"], ["A value.", "Person = person.", "Fairness."], "Person equals person: equality.", 3),
 ("🌊 + 🏄 + 🌐", ["surf the web", "surfing the web", "web surfing", "surf the internet"], ["A 1990s phrase.", "Wave, surfer, globe.", "Browse."], "Surf + the web.", 2),
 ("☕ + 💤 ➡️ 😮", ["coffee wakes you up", "wake up", "awake", "caffeine", "coffee"], ["What coffee does.", "Sleep, then eyes open.", "Caffeine."], "Coffee turns sleep into alertness: wake up.", 2),
 ("🎩 + 🐇", ["magic", "magic trick", "magician", "rabbit in a hat", "abracadabra"], ["Abracadabra.", "Hat + rabbit.", "A trick."], "A hat and a rabbit: magic.", 2),
 ("🧱 + 🧱 + 🧱 + 🚪", ["wall", "a wall", "brick wall", "house", "building"], ["Bricks around a door.", "What keeps the outside out.", "Humpty sat on one."], "Bricks and a door make a wall.", 2),
]

# ---------- Chains: five mini clues; first letters of answers spell the final word. (clues:[(clue,[answers])], final:[answers], theme)
CHAINS = [
 ([("Frozen water", ["ice"]), ("Opposite of day", ["night"]), ("Big cat with a mane", ["lion"]), ("Sound a dog makes", ["bark", "woof"]), ("Our planet", ["earth"])], ["inlbe"], None),
]
# Build chains programmatically from a bank so first letters spell a word.
BANK = {
 "a": ("Red or green fruit that keeps doctors away", ["apple"]), "b": ("Yellow fruit monkeys love", ["banana"]), "c": ("Pet that purrs", ["cat"]), "d": ("Pet that barks", ["dog"]),
 "e": ("The planet we live on", ["earth"]), "f": ("Animal with a bushy red tail", ["fox"]), "g": ("Precious yellow metal", ["gold"]), "h": ("Where the heart is, they say", ["home"]),
 "i": ("Frozen water", ["ice"]), "j": ("Sweet spread made from fruit", ["jam", "jelly"]), "k": ("Royal man with a crown", ["king"]), "l": ("Big cat with a mane", ["lion"]),
 "m": ("Earth's natural satellite", ["moon"]), "n": ("Opposite of day", ["night"]), "o": ("Vast body of salt water", ["ocean"]), "p": ("Large flightless bird in a tuxedo", ["penguin"]),
 "q": ("Royal woman with a crown", ["queen"]), "r": ("Water falling from clouds", ["rain"]), "s": ("The star we orbit", ["sun"]), "t": ("Tall plant with a trunk", ["tree"]),
 "u": ("What you carry in the rain", ["umbrella"]), "v": ("Red day in February", ["valentine", "valentines"]), "w": ("What fish live in", ["water"]), "x": ("Instrument with wooden bars you strike", ["xylophone"]),
 "y": ("Colour of a banana", ["yellow"]), "z": ("Striped horse-like animal", ["zebra"]),
}
FINALS = ["smile", "dream", "light", "brave", "ocean", "magic", "storm", "piano", "crown", "music", "grace", "honey", "lemon", "tiger", "cloud", "fable", "glide", "bloom", "amber", "candy", "ember", "frost", "ivory", "jolly", "karma", "lunar", "mango", "noble", "olive", "pearl"]
CHAINS = []
for w in FINALS:
    CHAINS.append(([BANK[ch] for ch in w], [w], None))

# ---------- Library of extra riddles for collections (riddle, answer(s), category, difficulty)
LIBRARY = [
 ("What has hands but can't clap?", ["clock", "a clock"], "kids", 1), ("What has a face and two hands but no arms or legs?", ["clock", "a clock"], "kids", 1),
 ("What has to be broken before you can use it?", ["egg", "an egg"], "kids", 1), ("What has a thumb and four fingers but isn't alive?", ["glove", "a glove"], "kids", 1),
 ("What kind of room has no doors or windows?", ["mushroom", "a mushroom"], "wordplay", 2), ("What begins with T, ends with T, and has T in it?", ["teapot", "a teapot"], "wordplay", 2),
 ("What has words but never speaks?", ["book", "a book"], "kids", 1), ("What can you catch but not throw?", ["cold", "a cold"], "wordplay", 2),
 ("What has legs but doesn't walk?", ["table", "a table", "chair", "a chair"], "kids", 1), ("What invention lets you look right through a wall?", ["window", "a window"], "kids", 1),
 ("I'm light as a feather, yet the strongest person can't hold me for five minutes. What am I?", ["breath", "your breath"], "classic", 2), ("What can run but never walks, has a mouth but never talks, has a bed but never sleeps?", ["river", "a river"], "classic", 2),
 ("What goes through cities and fields but never moves?", ["road", "a road", "roads"], "classic", 2), ("What has a bottom at the top?", ["legs", "your legs", "leg"], "wordplay", 3),
 ("What five-letter word becomes shorter when you add two letters?", ["short"], "wordplay", 3), ("What is full of holes but still holds water?", ["sponge", "a sponge"], "classic", 1),
 ("What is always in front of you but can't be seen?", ["future", "the future"], "classic", 2), ("What can you keep after giving it to someone?", ["your word", "word", "a promise", "promise"], "classic", 2),
 ("What month of the year has 28 days?", ["all of them", "every month", "all"], "wordplay", 2), ("If there are three apples and you take away two, how many do you have?", ["two", "2"], "math", 2),
 ("How many months have 30 days?", ["eleven", "11", "all but february"], "math", 2), ("I am a three-digit number. My tens digit is five more than my ones digit, and my hundreds digit is eight less than my tens digit. What number am I?", ["194"], "math", 4),
 ("What three positive numbers give the same result when multiplied and added together?", ["1 2 3", "1, 2, 3", "1 2 and 3", "one two three"], "math", 3), ("A farmer has 17 sheep and all but 9 die. How many are left?", ["nine", "9"], "math", 2),
 ("Using only addition, how can you add eight 8s to get 1,000?", ["888+88+8+8+8", "888 + 88 + 8 + 8 + 8"], "math", 5), ("What comes once in a minute, twice in a moment, but never in a thousand years?", ["the letter m", "m", "letter m"], "wordplay", 3),
 ("I have cities but no people, forests but no trees, and rivers but no water. What am I?", ["map", "a map"], "classic", 2), ("What disappears as soon as you say its name?", ["silence"], "classic", 2),
 ("What can you hold in your right hand but never in your left?", ["your left hand", "left hand", "my left hand"], "logic", 3), ("What is so fragile that saying its name breaks it?", ["silence"], "classic", 2),
 ("A man is pushing his car along a road when he comes to a hotel. He shouts, 'I'm bankrupt!' Why?", ["monopoly", "he is playing monopoly", "playing monopoly", "it's a game of monopoly"], "logic", 4),
 ("Which is heavier, a kilogram of feathers or a kilogram of bricks?", ["neither", "same", "the same", "they weigh the same", "equal"], "math", 1),
 ("What word is spelled incorrectly in every dictionary?", ["incorrectly"], "wordplay", 2), ("What has 13 hearts but no other organs?", ["deck of cards", "a deck of cards", "cards", "pack of cards"], "logic", 3),
 ("What goes up and down but never moves?", ["stairs", "staircase", "a staircase", "the stairs"], "kids", 1), ("What has a ring but no finger?", ["telephone", "a telephone", "phone", "a phone"], "kids", 1),
 ("Where does today come before yesterday?", ["dictionary", "the dictionary", "in the dictionary", "a dictionary"], "wordplay", 3), ("What is at the end of a rainbow?", ["the letter w", "w", "letter w"], "wordplay", 2),
 ("What has four wheels and flies?", ["garbage truck", "a garbage truck", "rubbish truck", "bin lorry"], "wordplay", 3), ("What kind of coat is best put on wet?", ["coat of paint", "a coat of paint", "paint"], "wordplay", 3),
 ("What can be measured but has no length, width or height?", ["temperature", "time"], "classic", 3), ("What do you throw out when you want to use it, but take in when you don't?", ["anchor", "an anchor"], "classic", 3),
 ("I follow you all day long, but when night comes I disappear. What am I?", ["shadow", "your shadow", "a shadow"], "kids", 1), ("You walk into a room with a match, a candle, a lamp and a fireplace. What do you light first?", ["the match", "match"], "logic", 2),
 ("What has a spine but no bones?", ["book", "a book"], "kids", 2), ("What gets bigger the more you take away from it?", ["hole", "a hole"], "classic", 2),
 ("What can go up a chimney down, but can't go down a chimney up?", ["umbrella", "an umbrella"], "logic", 4), ("Mary's father has five daughters: Nana, Nene, Nini, Nono. What is the fifth daughter's name?", ["mary"], "logic", 2),
 ("What has one eye but can't see, and is worse than a wind?", ["hurricane", "a hurricane", "cyclone"], "classic", 3), ("I'm found in socks, scarves and mittens, and often in the paws of playful kittens. What am I?", ["yarn", "wool"], "kids", 2),
 ("What tastes better than it smells?", ["tongue", "your tongue", "a tongue"], "wordplay", 3), ("What has a head, a tail, is brown, and has no legs?", ["penny", "a penny", "coin", "a coin"], "kids", 2),
 ("Which word in the dictionary is always spelled wrong?", ["wrong"], "wordplay", 2), ("How many letters are in the alphabet?", ["eleven", "11"], "wordplay", 3),
 ("What is black when it's clean and white when it's dirty?", ["chalkboard", "a chalkboard", "blackboard", "a blackboard"], "classic", 2), ("What has many needles but doesn't sew?", ["pine tree", "a pine tree", "christmas tree", "a christmas tree", "cactus", "a cactus"], "kids", 1),
 ("I am taken from a mine and shut in a wooden case, from which I am never released, and yet I am used by almost everyone. What am I?", ["pencil lead", "lead", "graphite", "pencil"], "classic", 3), ("What is cut on a table but never eaten?", ["deck of cards", "cards", "a deck of cards"], "logic", 3),
 ("What is always coming but never arrives?", ["tomorrow"], "classic", 2), ("What can you break, even if you never pick it up or touch it?", ["a promise", "promise", "silence", "a record", "record"], "classic", 2),
]

def norm_answers(a): return sorted({x.strip().lower() for x in a})
puzzles = {}
for i in range(30):
    d = (START + datetime.timedelta(days=i)).isoformat()
    r = RIDDLES[i]; b = REBUS[i]; c = CHAINS[i]
    puzzles[d] = {
        "n": i + 1,
        "riddle": {"q": r[0], "a": norm_answers(r[1]), "display": r[1][0], "hints": r[2], "why": r[3], "trivia": r[4], "difficulty": r[5], "category": r[6]},
        "rebus": {"q": b[0], "a": norm_answers(b[1]), "display": b[1][0], "hints": b[2], "why": b[3], "difficulty": b[4]},
        "chain": {"clues": [{"q": q, "a": norm_answers(a)} for q, a in c[0]], "final": norm_answers(c[1]), "why": f"The first letters of the five answers spell {c[1][0].upper()}."},
    }
json.dump(puzzles, open(os.path.join(D, "puzzles.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump([{"q": q, "a": norm_answers(a), "category": c, "difficulty": dd} for q, a, c, dd in LIBRARY], open(os.path.join(D, "library.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("seeded", len(puzzles), "days,", len(LIBRARY), "library riddles")
