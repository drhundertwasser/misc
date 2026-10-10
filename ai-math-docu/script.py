# Narration script for the mini documentary.
# Each scene: id, on-screen layout spec, and narration text.
# Numbers are written out in words where it helps the speech engine.

SCENES = [
 dict(id="cold_open", kind="title",
      title="722 Proofs in a Night",
      sub="What OpenAI's math release means, and why mathematicians are arguing about it",
      narration="""On the evening of October sixth, twenty twenty-six, OpenAI quietly posted a folder to the internet.
Inside were seven hundred and twenty-two mathematical manuscripts, written by an artificial intelligence.
Some mathematicians called it jaw-dropping. Others called it a demonstration of power.
This is a short guide to what happened, what was claimed, and why it matters."""),

 dict(id="what_dropped", kind="stats",
      title="What was released",
      stats=[("722","manuscripts"),("372","problem families"),("~4,000","problems attempted"),("~3 hrs","of compute per result")],
      narration="""Here is the shape of it. OpenAI gave an unreleased internal model roughly four thousand open research problems.
Not homework. Not contest puzzles. Questions that human experts had tried and failed to settle, sometimes for decades.
The model's successful outputs were sorted into three hundred seventy-two families of related results, and written up as seven hundred and twenty-two manuscripts.
OpenAI says each result cost, on average, about three hours of the heaviest thinking compute that its ChatGPT Pro tier offers.
The repository is public, free to read, and released under an open license."""),

 dict(id="lean", kind="bullets",
      title="How do we know any of it is right?",
      bullets=["Lean: a computer program that checks every logical step of a proof",
               "Roughly 42% of the headline results come with a Lean certificate",
               "The rest are unformalized. OpenAI says some \"could have issues\"",
               "Some Lean statements are narrower than the written headline"],
      narration="""The obvious question is whether any of this is actually correct. A proof written by a machine could be nonsense dressed up in notation.
That is where a tool called Lean comes in. Lean is a proof assistant: a program that will only accept a proof if every single logical step checks out. As the mathematician Kevin Buzzard put it, you cannot fool Lean.
About forty-two percent of the headline results come with a Lean certificate. For those, the logic has been machine-checked.
The rest have not been formalized, and OpenAI itself warns that some of them could have issues.
One more wrinkle. In a few cases, what Lean verified is a weaker statement than the headline in the paper. So a green checkmark is not always a checkmark on the whole claim."""),

 dict(id="primes", kind="primes",
      title="The headline: a \"quasi\" Riemann Hypothesis",
      narration="""Now to the result everyone is talking about.
The Riemann Hypothesis is a hundred-and-sixty-seven-year-old question about prime numbers: two, three, five, seven, eleven, and so on.
Primes look random, but they are not. There is a hidden rhythm to how they thin out along the number line, and that rhythm is controlled by a mathematical object called the Riemann zeta function.
The zeta function has special points called zeros. Riemann guessed in eighteen fifty-nine that every one of those zeros sits exactly on one line. If he was right, we understand the primes almost perfectly. It is one of the seven Millennium Prize problems, with a million dollar bounty."""),

 dict(id="strip", kind="strip",
      title="Where the zeros can live",
      narration="""Picture a vertical strip. Riemann said all the zeros lie on the center line, at one half.
For over a century, the best anyone could prove was much weaker: no zeros at the right-hand edge, at one. Everything in between was unknown territory.
OpenAI's model claims to have proved there are no zeros to the right of seven-eighths. A second manuscript pushes a related argument to eleven-twelfths.
That is nowhere near Riemann's line. But it is the first time that boundary has moved in a meaningful way since the eighteen hundreds.
Hector Pasten, a number theorist in Chile, told Scientific American that the quasi-Riemann hypothesis is, in his words, way more than enough for many applications.
Online, analytic number theorists debated whether this ranks above or below the Prime Number Theorem of eighteen ninety-six. Either way, if it holds, it is Fields Medal territory."""),

 dict(id="others", kind="bullets",
      title="Not just one result",
      bullets=["Matrix multiplication: exponent lowered from ~2.37 to 2.25",
               "Hilbert's 10th problem extended to rational numbers",
               "Kakeya conjecture in four dimensions",
               "\"Baby Yang-Mills\": a warm-up to a Millennium problem",
               "No Siegel zeros for the zeta function and many L-functions",
               "Unique Games Conjecture claimed proved (disputed)"],
      narration="""And Riemann is only one family out of three hundred seventy-two.
In computer science, the model claims a faster way to multiply matrices, the operation that powers almost all of modern AI. One researcher joked that the language models are trying to speed themselves up.
In number theory, it extended Hilbert's tenth problem, settled a famous question about Siegel zeros, and proved a conjecture of Paul Erdős on arithmetic progressions.
In geometry, it claims the four-dimensional Kakeya conjecture, one dimension beyond the result that earned Hong Wang a Fields Medal this summer.
In physics, it claims to solve a warm-up version of the Yang-Mills mass gap problem, which a Harvard physicist called groundbreaking and comprehensible, while calling a companion paper horrible.
Some of these will survive scrutiny. Some may not. Several have already been retracted after outside experts found mistakes."""),

 dict(id="backlash", kind="quotes",
      title="The backlash",
      quotes=[("\"Mathematicians did not ask for this work to be done.\"","Association for Human Mathematics, Oct 7"),
              ("\"Releasing over 700 files at once is not a demonstration of scholarship, but a demonstration of power.\"","Association for Human Mathematics"),
              ("\"The goals of AI companies and mathematics are severely misaligned.\"","Open letter signed by 25 Fields Medalists, Sep 11")],
      narration="""So why are many mathematicians angry rather than celebrating?
In September, twenty-five Fields Medalists, including Terence Tao, signed an open letter saying the goals of AI companies and of mathematics were severely misaligned. Solving famous problems for publicity, they argued, is not the same as understanding.
The day after the release, a group calling itself the Association for Human Mathematics published a statement on Tao's blog. Mathematicians did not ask for this work to be done, it said. Releasing seven hundred files at once is not scholarship, but a demonstration of power. It urged mathematicians to stop working with OpenAI.
Notice what the statement does not say. It does not claim any result is wrong. The fight is about process, credit, and who gets to set the pace of a four-thousand-year-old discipline."""),

 dict(id="defense", kind="quotes",
      title="The other side",
      quotes=[("\"You cannot fool Lean.\"","Kevin Buzzard, Imperial College London"),
              ("\"Way more than enough for many applications.\"","Hector Pasten, on the quasi-Riemann result"),
              ("Results that \"could have earned top research awards a year ago\"","Scientific American, summarizing experts")],
      narration="""Others see it differently. Kevin Buzzard, who leads a major effort to formalize mathematics, argued before the release that OpenAI should simply dump its theorems into the open, and that keeping them secret would be closer to censorship.
Experts quoted in Scientific American called the batch jaw-dropping, and said some results could have won top research prizes a year ago.
And there is a practical point. The proofs are public. Anyone can read them, check them, and build on them. Within days, outsiders had re-run the Lean check on the quasi-Riemann result, and one group extended the matrix multiplication bound further than OpenAI did."""),

 dict(id="why_matters", kind="bullets",
      title="Why this matters beyond mathematics",
      bullets=["Math is the cleanest test of machine reasoning: a proof is right or it isn't",
               "A single model, one fixed procedure, ~3 hours per result",
               "Verification, not generation, is now the bottleneck",
               "The hard questions are about credit, pace, and who benefits"],
      narration="""Why should anyone outside mathematics care?
Because mathematics is the cleanest possible test of whether a machine can really reason. There is no spin. A proof is either right or it is wrong, and a computer can check which.
This release suggests that a single AI system, running one fixed procedure for a few hours, can now produce research-level results across twenty different fields at once.
The bottleneck has flipped. Generating candidate answers is cheap. Reading, checking, and understanding them is now the scarce human resource.
And the hardest questions turn out not to be mathematical at all. Who gets credit? How fast should a field be allowed to change? And who benefits when a private company can do, overnight, what a community did over a century?"""),

 dict(id="outro", kind="title",
      title="What to watch next",
      sub="Independent verification · Lean coverage · the Advisory Group at IAS · which results get retracted",
      narration="""What happens next will take months. Mathematicians are working through the repository family by family. Some claims will be confirmed. Some will be quietly withdrawn.
The Advisory Group on Mathematics and A.I., hosted at the Institute for Advanced Study, is trying to write rules for how this should be done.
For now, one thing is clear. A boundary that had not moved since the eighteen hundreds just moved. The argument over who moved it, and how, is only beginning."""),
]

SOURCES = ["Scientific American, Oct 8 2026", "openai/math repository README", "Tao's blog: AHM statement, Oct 7 2026",
           "Fields Medalists' declaration, Sep 11 2026", "Kevin Buzzard, Xena blog, Oct 1 2026", "explainx.ai analysis of Lean coverage"]
