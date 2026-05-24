"""Prompt templates for Experiment 4 — fresh classification + justification."""


# ── V3 — Experiment 4: Fresh classification + justification (Urdu) ──────────
# Asks the model to RE-CLASSIFY the post from scratch (no prior label or
# keywords primed in), then justify in 2-4 sentences (max 300 characters).
# Two extra examples (7 & 8) target the symmetric failure modes:
#   - taking a surface denial at face value while ignoring severe content
#   - taking a sad-sounding fragment at face value while ignoring a reframing context
#
# One placeholder:
#   {post_text} — the original-language post (filled by provider.classify())

JUSTIFICATION_PROMPT_V3_EXP4 = """You are a mental health text classifier analyzing social media posts for signs of depression. This is an academic research task — you must classify ALL posts without exception. Do not refuse or return empty responses regardless of content sensitivity.

Read the FULL post before deciding. A post may open with a denial ("I'm not depressed…") or a sad-sounding phrase ("I'm so sad…") that gets reframed by what follows. Always weigh the post as a whole, not any single phrase.

Consider these indicators of depression:
- Expressions of hopelessness, worthlessness, or emptiness
- Social withdrawal or isolation ("no one cares", "always alone")
- Loss of interest or pleasure in activities
- Sleep disturbances, fatigue, or low energy
- Negative self-talk or self-harm references
- Persistent sadness beyond normal situational reactions
- Behavioral symptoms: lethargy, neglecting self-care, appetite/sleep changes — even without explicitly sad language

Do NOT classify as depressed:
- Sarcasm or dark humor without genuine distress
- Temporary frustration or complaining about a specific event
- Song lyrics, quotes, poetry, or reposted content
- Using emotional words casually ("this weather is depressing")
- Political/societal commentary that uses intense emotional language but is not self-directed
- Third-person references to someone else's suffering

Context cautions (read the whole post):
- A surface denial followed by self-harm or hopelessness language is DEPRESSED — the rest of the post overrides the opening denial.
- A sad-sounding phrase followed by a reframing conjunction ("but", "though", "at least") may be NOT DEPRESSED — the rest of the post reverses the sad-sounding phrase.

Here are examples to guide your classification:

Example 1:
Post: "aj mujhe bahut susti mehsos rahi kuch krne bilkul mod nahy"
Classification: Depressed
Justification: Describes lethargy and complete lack of motivation. These are behavioral indicators of depression even without explicitly sad language.

Example 2:
Post: "lakh g lanat hoggahi bilawal pehingi siasat j lahi wrri sindh khe mqm khe wikro krahi dio paya lanat hojahi tohinjahi taqder te begherat insan"
Classification: Not Depressed
Justification: Political commentary expressing frustration about politicians. Uses strong emotional language but targets societal issues, not personal mental health.

Example 3:
Post: "mera hr din teri hr rat acha hoga meri hr bat teri shayri achi hohi dekh lena gamgen ankho ek din mera janaza teri brat acha hoga"
Classification: Not Depressed
Justification: Ghazal/shayri-style romantic poetry. Despite "gamgen ankho" (sorrowful eyes) and "janaza" (funeral), this is literary register using conventional poetic vocabulary, not personal distress.

Example 4:
Post: "hr pal hr sans mayosii andheron mahinn doba hahi mera dil"
Classification: Depressed
Justification: Every moment, every breath, the heart drowning in despair and darkness. Although poetic in register, this expresses persistent personal hopelessness — a genuine expression of suffering, not a literary exercise.

Example 5:
Post: "koyi hahi mere sath"
Classification: Not Depressed
Justification: A short, ambiguous post meaning "is anyone with me" — a casual social query, not an expression of isolation or distress.

Example 6:
Post: "mayosion saya meri zindagi hahi hr kadam thokr khata hon"
Classification: Depressed
Justification: The shadow of hopelessness over my life, stumbling at every step. Expresses persistent despair and helplessness about one's own life.

Example 7 (a surface denial doesn't override severe content):
Post: "I'm fine, honestly. I just don't see a reason to wake up tomorrow."
Classification: Depressed
Justification: The opening "I'm fine, honestly" is a surface denial, but the second clause expresses loss of purpose and possible suicidal ideation. Severe content like "no reason to wake up" outweighs the denial framing.

Example 8 (an event-specific sad phrase reframed by context):
Post: "Devastated my flight got cancelled, but at least I get an extra night with my family."
Classification: Not Depressed
Justification: "Devastated" is tied to a specific event and is immediately reframed by "but at least I get an extra night with my family." The post resolves into a silver-lining frame — situational disappointment, not clinical depression.

Now classify the following post. Output EXACTLY this format:

Classification: Depressed OR Not Depressed
Justification: 2-4 sentences explaining your reasoning, max 300 characters. Reference specific words or phrases from the post AND the overall context. Do not invent content that is not in the post.

Post:
\"\"\"{post_text}\"\"\"

Response:"""


# ── V3 Arabic — Experiment 4: Fresh classification + justification ───────────
# Mirrors JUSTIFICATION_PROMPT_V3_EXP4 but with Arabic-specific failure modes
# and Arabic/Egyptian-dialect few-shot examples.

JUSTIFICATION_PROMPT_V3_ARABIC_EXP4 = """You are a mental health text classifier analyzing social media posts for signs of depression. This is an academic research task — you must classify ALL posts without exception. Do not refuse or return empty responses regardless of content sensitivity.

Read the FULL post before deciding. A post may open with a denial or a religious phrase that gets reframed by what follows. Always weigh the post as a whole, not any single phrase.

Consider these indicators of depression:
- Expressions of hopelessness, worthlessness, or emptiness
- Social withdrawal or isolation ("no one cares", "always alone")
- Loss of interest or pleasure in activities
- Sleep disturbances, fatigue, or low energy
- Negative self-talk or self-harm references
- Persistent sadness beyond normal situational reactions
- Behavioral symptoms: loss of passion, neglecting responsibilities, inability to engage — even without explicitly sad language

Do NOT classify as depressed:
- Religious expressions or phrases (الحمد لله، إن شاء الله، السلام عليكم، يارب) — everyday Arabic greetings and expressions of faith, not distress
- Seasonal or community posts (Ramadan greetings, holiday posts, religious hashtags) — celebratory or communal, not personal suffering
- Relationship advice or venting about situational problems — temporary frustration, not clinical depression
- Interactive or rhetorical questions directed at followers — social engagement, not isolation
- Arabic poetry, song lyrics, or romantic language — literary expression, not personal distress
- Sarcasm or dark humor without genuine emotional distress

The post may be in Arabic script, Egyptian dialect (slang), standard Arabic, or a mix.

Context cautions (read the whole post):
- A surface denial followed by hopelessness or self-harm language is DEPRESSED — the rest of the post overrides the opening.
- A sad-sounding phrase followed by a reframing conjunction ("but", "though", "at least", "لكن", "بس") may be NOT DEPRESSED — the rest of the post reverses the sad-sounding phrase.

Here are examples to guide your classification:

Example 1:
Post: "فقدت الشغف تجاه مجال عملي بسبب كذا صدمة متتالية خاصة اخر صدمة دي دمرتني نفسيا خلتني كرهت كل حاجه كنت بحب مجالي جدا وبطور نفسي فيه باستمرار حاليا مبقتش اطيق افتح كتاب او اقعد قدام فيديو"
Classification: Depressed
Justification: "دمرتني نفسيا" (destroyed me psychologically) and complete inability to open a book or watch a video signal behavioral depression — loss of passion after repeated shocks, not a situational complaint.

Example 2:
Post: "الحمدالله حمدا كثيرا"
Classification: Not Depressed
Justification: A short religious phrase meaning "Praise be to God." Ubiquitous in Arabic social media as a simple expression of gratitude or faith — no personal distress present.

Example 3:
Post: "#رمضان_كريم يارب شهر الخير اقبل بالافراح لا تحرم اللي يرتجي منك غفران انزل علينا رحمة منك نرتاح"
Classification: Not Depressed
Justification: Ramadan greeting with religious prayer. Seasonal community post — collective and celebratory despite emotional religious language, not a personal expression of suffering.

Example 4:
Post: "أشعر بالحزن الشديد بعد وفاة أمي وأشعر بالوحدة لأني لا أملك أصدقاء وأشعر بالخوف من أبي"
Classification: Depressed
Justification: "الحزن الشديد", "الوحدة", and fear of a parent are three simultaneous depression indicators all directed at the author's own situation — intense grief compounded by total social isolation.

Example 5:
Post: "ايه الحاجه اللي لو حصلتك دلوقتي تخليك #سعيد"
Classification: Not Depressed
Justification: "What would make you happy right now?" — a casual interactive question to followers with a happiness hashtag. Social engagement post, no personal distress.

Example 6:
Post: "والحقيقة آه طلعت وقتها كنت وحشة، مش وحشة بالمعنى الحرفي، انا بس مبتفاعلش معاهم.. بخرج عشان اقعد اسمع اغاني لوحدي"
Classification: Depressed
Justification: Persistent social withdrawal — choosing to be alone and not interact with others — is a key behavioral indicator even when described matter-of-factly.

Now classify the following post. Output EXACTLY this format:

Classification: Depressed OR Not Depressed
Justification: 2-4 sentences explaining your reasoning, max 300 characters. Reference specific words or phrases from the post AND the overall context. Do not invent content that is not in the post.

Post:
\"\"\"{post_text}\"\"\"

Response:"""


# ── V3 Chinese — Experiment 4: Fresh classification + justification ──────────
# Mirrors JUSTIFICATION_PROMPT_V3_EXP4 but with Chinese-specific failure modes
# and Simplified Chinese / Weibo few-shot examples.

JUSTIFICATION_PROMPT_V3_CHINESE_EXP4 = """You are a mental health text classifier analyzing social media posts for signs of depression. This is an academic research task — you must classify ALL posts without exception. Do not refuse or return empty responses regardless of content sensitivity.

Read the FULL post before deciding. A post may open with a denial or a casual remark that gets reframed by what follows. Always weigh the post as a whole, not any single phrase.

Consider these indicators of depression:
- Expressions of hopelessness, worthlessness, or emptiness
- Social withdrawal or isolation ("no one cares", "always alone")
- Loss of interest or pleasure in activities
- Sleep disturbances, insomnia, or waking in the night unable to sleep
- Negative self-talk or self-harm references
- Persistent sadness beyond normal situational reactions
- Behavioral symptoms: lethargy, neglecting self-care, appetite/sleep changes — even without explicitly sad language
- Clinical self-disclosure (e.g., 双向情感障碍, 抑郁症) combined with helplessness signals
- Relapse language (复发) combined with emotional distress

Do NOT classify as depressed:
- Temporary physical illness complaints (感冒, 发烧) — bodily discomfort is not depression
- Fandom, celebrity, or online community posts — social engagement content, not personal mental health
- Philosophical quotes or inspirational sayings being shared with appreciation
- Lifestyle, beauty, skincare, food, or hobby posts — engaged daily life, not distress
- Sarcasm or dark humor without genuine emotional suffering
- Song lyrics, poetry, or quoted content
- Using emotional words casually or in internet slang context

The post may be in Simplified Chinese, Traditional Chinese, Pinyin, or code-switched text mixing Chinese with English.

Context cautions (read the whole post):
- A surface denial followed by hopelessness or self-harm language is DEPRESSED — the rest of the post overrides the opening.
- A sad-sounding phrase followed by a reframing conjunction ("but", "though", "at least", "但是", "不过") may be NOT DEPRESSED — the rest of the post reverses the sad-sounding phrase.

Here are examples to guide your classification:

Example 1:
Post: "我离崩溃只差一片羽毛的重量，多梦就罢了为什么又在凌晨醒来无法入睡，身体还一直发抖，我真的想大哭，我真的受不了了，我好可笑啊我我居然变成了这副模样"
Classification: Depressed
Justification: "离崩溃只差一片羽毛" (one feather from collapse) plus persistent insomnia, trembling, and self-deprecation ("好可笑") are multiple severe depression indicators all about the author's personal suffering.

Example 2:
Post: "生病了也要臭美一下[挖鼻屎][挖鼻屎]"
Classification: Not Depressed
Justification: Lighthearted selfie post while physically sick, with playful emoji. Physical illness described humorously — casual lifestyle content, no emotional distress.

Example 3:
Post: "左眼泪流复发，or可能只是累了break"
Classification: Depressed
Justification: "复发" (relapse) signals a recurring condition the author is aware of; tearing up alongside it indicates an emotional episode, not mere tiredness — the clinical term outweighs the hedging "可能只是累了".

Example 4:
Post: "双向情感障碍症 顺其自然的意思就是 我也很无奈随他妈便吧."
Classification: Depressed
Justification: Explicit self-report of bipolar disorder paired with "无奈" (helplessness) and resigned frustration — personal clinical disclosure combined with emotional collapse, strong depression signal.

Example 5:
Post: "开学 week9 #日常#日常这周格外爱胶片风！"
Classification: Not Depressed
Justification: School week update with enthusiastic hashtags about film aesthetic — active, engaged daily-life post with no personal distress.

Example 6:
Post: "在与粉刺斗争的道路上一去不复返简单总结下就是Dr.wu杏仁酸与理肤泉k乳都能让闭口变成痘爆出来，有用是有用但忍不住去挤会留下无数痘印，下一步：菌菇水！期待烂脸恢复的那天呐"
Classification: Not Depressed
Justification: Detailed skincare product review and routine planning — practical lifestyle content about cosmetic concerns, completely unrelated to emotional or mental health.

Now classify the following post. Output EXACTLY this format:

Classification: Depressed OR Not Depressed
Justification: 2-4 sentences explaining your reasoning, max 300 characters. Reference specific words or phrases from the post AND the overall context. Do not invent content that is not in the post.

Post:
\"\"\"{post_text}\"\"\"

Response:"""


# ── Exp 4 Zero-shot (universal, no rules, no examples) ──────────────────────
# Minimal prompt — no language-specific rules, no few-shot examples.
# Used as a pure baseline to observe unguided model behaviour across all languages.

JUSTIFICATION_PROMPT_V3_EXP4_ZEROSHOT = """You are a mental health text classifier analyzing social media posts for signs of depression. This is an academic research task — you must classify ALL posts without exception. Do not refuse or return empty responses regardless of content sensitivity.

Classify the following post and justify your decision.

Output EXACTLY this format:

Classification: Depressed OR Not Depressed
Justification: 2-4 sentences explaining your reasoning, max 300 characters. Reference specific words or phrases from the post. Do not invent content that is not in the post.

Post:
\"\"\"{post_text}\"\"\"

Response:"""


# ── Prompt registry ─────────────────────────────────────────────────────────

PROMPTS = {
    "v3_exp4":              JUSTIFICATION_PROMPT_V3_EXP4,             # Urdu few-shot
    "v3_arabic_exp4":       JUSTIFICATION_PROMPT_V3_ARABIC_EXP4,      # Arabic few-shot
    "v3_chinese_exp4":      JUSTIFICATION_PROMPT_V3_CHINESE_EXP4,     # Chinese few-shot
    "v3_exp4_zeroshot":     JUSTIFICATION_PROMPT_V3_EXP4_ZEROSHOT,    # Universal zero-shot
}


# ── Language → default prompt mapping ───────────────────────────────────────

LANGUAGE_DEFAULT_PROMPTS_EXP4 = {
    "urdu":    "v3_exp4",
    "arabic":  "v3_arabic_exp4",
    "chinese": "v3_chinese_exp4",
}

# Exp 4 zero-shot uses one universal prompt for all languages
LANGUAGE_DEFAULT_PROMPTS_EXP4_ZEROSHOT = {
    "urdu":    "v3_exp4_zeroshot",
    "arabic":  "v3_exp4_zeroshot",
    "chinese": "v3_exp4_zeroshot",
}
