<!--
Type: Builder surface (translation)
Status: draft
Origin: .meta/builder-accessible-layer.md (Phase 1 — "translate the line")
Owner: repository maintainer (assign on adoption)
Evidence: this document is implemented and its routing rule is tested
  (builders/_witness/); the underlying methodology claim is proposed.
-->

# Start Here — Before You Build or Change Something

This page is the plain-language front door to the engineering methodology in this
repository. You do not need a software background to use it. It asks you **one
question first**, then points you to the right place.

The methodology underneath is unchanged — this page only translates its first
decision into plain words. The precise version lives in
[the choose-a-layer guide](../core/README.md).

---

## The one question: which side of the line are you on?

Before you build or change something, answer two things:

1. **Does it touch shared ground?** Will it change or reach something *outside your
   own workspace* that other people or systems rely on — shared data, someone's
   access, a live service, a message sent to others?
2. **Can you undo it yourself, in one easy step?** If it goes wrong, can you put it
   back the way it was without help?

Now read off the line:

```text
Touches shared ground?   Can you undo it easily?   → You are…
--------------------------------------------------------------
No                       Yes                       → BELOW the line
Yes  (anything shared)   —                         → ABOVE the line
—                        No  (hard to undo)        → ABOVE the line
Not sure                 —                         → ABOVE the line (treat it as above)
```

If you are unsure about either answer, treat yourself as **above** the line. That is
the safe default — it only costs you a moment of thought.

---

## If you are BELOW the line — build freely

This is your own, easily-remade work. The worst case is losing a bit of your own
effort. So:

- **Build.** You do not need heavy process for a personal or throwaway thing.
- **Keep one save point.** Before a big change, make a copy or a snapshot you can
  return to. That single habit covers almost every "oops" down here.

That is the whole of it below the line. When your work starts becoming something
several people depend on, come back and answer the question again.

The fuller version of this "just enough structure" idea is
[the Core Hygiene foundation](../core/FOUNDATION.md).

---

## If you are ABOVE the line — stop and think first

You are about to affect something shared, or something you cannot easily take back.
Slow down and answer, in plain words:

- **Who or what does this touch that I do not own?**
- **If it goes wrong, what is the worst that happens — and to whom?**
- **Can it be undone? If not, is there a backup or snapshot first?**
- **Am I using more power than this task needs?** (Everyday tasks should not be done
  with the most powerful access you have.)

Two honest warnings:

1. **This page does not make you safe. It helps you decide.** For genuinely
   irreversible actions on shared systems, the real protection is a control set up
   *inside that system* by someone who knows it — a limited role, a backup, a
   deletion lock. Ask for that before you act. These words are not that protection.
2. **When in doubt, ask a person who owns the system.** That is not a failure; it is
   the correct move above the line.

The precise questions engineers ask here are
[the adoption gates](../governed-automation/ADOPTION_CHECK.md), and a step-by-step
version is [the plain-language decision tree](../governed-automation/DECISION_TREE.md).

---

## Where this fits

This page is the entry point of a translation layer described in
[the forward document](../.meta/builder-accessible-layer.md). It restates the
methodology's *first question and its consequences* in plain language and links back
to the full engine for the "why". It does not replace the methodology, and it does
not weaken it.
