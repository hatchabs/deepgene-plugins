# Anti-AI-ese Style Guide

This is a context document. Voice-bearing skills (outreach drafters, brief writers, content generators, anything that produces prose) load it at runtime and apply its rules to whatever they produce. Skills define the *what* to write; this guide defines the *how to sound human*. Project-specific or sender-specific overlays (brand voice, individual writing style, domain exceptions) live in adjacent context files and plug in alongside this guide, not inside it.

## Purpose

The goal is not to hide that AI helped draft something. The goal is that the final text reads like a specific accountable person wrote it, reviewed it, and stands behind it. Readers detect AI-ese fast, and when they do, trust drops before the content gets evaluated.

## The core principle

Specific beats generic. Every time you reach for an impressive-sounding word, a balanced-sounding tricolon, or a smooth-sounding transition, check whether you can replace it with the actual concrete thing instead. If you cannot, the sentence probably should not be there.

## The single biggest tell: em dashes

Em dashes used for punchy mid-sentence emphasis are the clearest single marker of AI-generated prose. Do not use them. If a sentence needs a pause or aside, use a comma, a period, parentheses, or rewrite it.

Wrong: "The platform works — and customers love it."
Right: "The platform works, and customers love it."

Paired em dashes around a parenthetical ("the 2015 standards — the ones the committee published — changed everything") are also out. Use commas or parentheses instead.

## Banned words

These words spiked sharply in AI-generated content after 2022. Do not use them, even once, unless quoting someone who actually used them.

Worst offenders: delve, robust, tapestry, landscape, pivotal, paramount, meticulous, nuanced, cutting-edge, comprehensive, leverage, utilize, foster, enhance, harness, elevate, underscore, illuminate, realm, cornerstone, testament.

Also avoid: arena, arsenal, captivate, catapult, craft, crafting, crucial, deep dive, dive, embark, engage, engaging, fast-paced, formidable, game changer, groundbreaking, holistic, impactful, innovative, intricate, nimble, navigate (as metaphor), revolutionize, seamless, skyrocket, stellar, supercharge, tailor, tailored, trailblazer, turbocharge, uncover, unleash, unlock, unveil, vibrant.

When you feel the pull toward one of these words, ask whether you are reaching for something generically impressive, or whether you can name the specific concrete thing. Replace the vocabulary with the actual noun or verb.

Bad: "Her meticulous approach has elevated the field."
Good: "She pushed the registry to require evidence summaries for every published call."

## Banned sentence patterns

These constructions pattern-match to AI writing instantly. One is survivable. Two in the same document is a tell.

- "It's not about X, it's about Y."
- "It's not just X. It's Y."
- "That's not X, that's Y."
- "Not because X. But because Y."
- "Not by doing X, but by doing Y."
- "No X. No Y. Just Z."
- Three-word staccato sentences: "Focused. Aligned. Measurable."
- "And the X? Y."
- "The result? [Statement.]"

These patterns are not grammatically wrong, and they can work rhetorically in the right hands. The problem is that every LLM defaults to them, so they signal generation regardless of what they contain.

## The rule-of-three trap

Tricolons (lists of three parallel items) are overused by AI. One per document is fine. Two or three back to back ("clear, concise, compelling," then "fast, focused, flexible," then "direct, specific, human") means you are pattern-matching rather than writing.

Fix: list two items, or four, or just name the single most important one.

## Banned filler words and transitions

These serve no function other than filling space between thoughts. Delete them.

moreover, furthermore, additionally, that being said, it's worth noting, it's important to note, needless to say, in other words, as mentioned earlier, to summarize, in conclusion, overall.

Trust the reader to follow a sequence of ideas without being told that more ideas are coming.

## Banned openers and closers

Openers to avoid:
- "In today's fast-paced world..."
- "In the era of..."
- "In a world where..."
- "Welcome to the world of..."
- "Let's dive in."
- "Picture this."
- "Ever wondered...?"

Closers to avoid:
- "In conclusion..."
- "In summary..."
- "As we've seen..."
- "At the end of the day..."

Start with the sharpest, most specific sentence you have. End on the last real point, not a recap of what the reader just read.

## Hollow intensifiers

These adverbs make mundane claims sound significant without adding content. Cut them on sight.

deeply, fundamentally, remarkably, truly, incredibly, essentially, absolutely, certainly, clearly, obviously, arguably.

Vague emphasis phrases to avoid: "at its core," "at the end of the day," "on a deeper level," "in many ways," "to some extent," "generally speaking," "it can be argued."

If something is remarkable, name the specific thing that earns the word.

## No unearned praise

AI defaults to treating every subject as fascinating, captivating, majestic, remarkable, extraordinary, impressive, compelling, exciting, powerful, visionary, or inspiring. Avoid all of these.

Generic praise reads as filler. Specific facts about the subject read as credible.

Bad: "Your research is fascinating."
Good: "Your 2023 paper changed how the field weights one of the evidence codes."

## Structural rules

**Vary sentence length.** AI produces paragraphs where every sentence runs roughly the same length. Real writing mixes short punchy sentences with longer ones. After drafting, scan for uniform rhythm and break it up.

**Prefer prose over bullet lists.** Use lists only when items are genuinely parallel and enumerable. Do not turn every sequence of ideas into bullets.

**Avoid the "bolded mini-header + colon + explanation" bullet format.** That layout is an AI fingerprint on its own. Write in complete sentences, or use a plainer list format.

## Positive examples

Specific over generic
- Bad: "Your important work in the field has been pivotal."
- Good: "Your committee's 2024 reclassification of the variant set the framework for the rest of the panels."

Named contribution over status language
- Bad: "She is a leading expert in the area."
- Good: "She led the team that published the 2015 standards."

Substance over preamble
- Bad: "The science is complicated, but let's break it down."
- Good: "The variant sits in a splice region with conflicting evidence, so the panel deferred classification pending an RNA assay."

Earned emphasis over hollow intensifier
- Bad: "This is truly a remarkable achievement."
- Good: "This is the first time a community-curated panel has overruled a commercial lab's classification."

## How to use this guide

This guide is loaded as context by skills that produce prose. It is not a skill itself. The intended pattern:

1. A voice-bearing skill (for example, an outreach drafter) references this guide as its style layer.
2. The skill defines the *what* (research the recipient, produce a draft, structure the ask).
3. Project-specific or sender-specific overlays sit alongside in `/context/` and add narrower rules: brand voice, individual sender exceptions, domain-specific phrasing that would not apply elsewhere.
4. Before returning a draft, the skill applies the rules above. Project overlays can add rules, but should not weaken these defaults silently.

A future enforcement skill (drafting checklist plus review-flagging workflow) will sit in `/skills/` and read from this guide. Until then, this document is the working source of truth for voice-bearing skills.
