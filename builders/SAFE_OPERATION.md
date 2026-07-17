<!--
Type: Builder surface (translation)
Status: implemented
Origin: .meta/DD-001-builder-accessible-layer.md section 3.4
Owner: repository maintainer (assign on adoption)
Evidence: structural and decision-oracle checks in builders/_witness/; runtime agent
  adherence and substrate enforcement are not demonstrated.
-->

# Safe Operation

Saving and acting are different.

- **Save** changes a local file or creates a version you can return to.
- **Publish, deploy, apply, grant, delete, or send** changes something outside your
  workspace that another person or system may rely on.

Before the second kind of action, stop and answer:

1. What exact system, data, access, or audience will change?
2. Who else could be affected?
3. Can the effect itself be undone, not merely the file that caused it?
4. Is there a backup, snapshot, preview, or dry run?
5. Are you using the least powerful access that can perform the task?

Ask the person who owns the affected system for explicit approval before proceeding.
Approval should name the target and action. A general “go ahead” does not cover a
broader or materially different effect.

## Keep An Undo Point

Use git to keep local authoring recoverable. The setup steps are in
[Git Setup](GIT_SETUP.md). Keep each commit to one coherent, checked increment and do not
mix it with someone else's existing work. A commit can restore files and explain what
changed, but it cannot unsend a message, restore every deleted shared record, or reverse
a live service change. For those effects, use controls provided by the system itself:
limited roles, backups, deletion protection, review gates, previews, or dry runs.

## Where To Go Next

Use [Start Here](START_HERE.md) to classify the work. For changes above the line, the
precise engineering gate is the
[Governed Automation Adoption Check](../governed-automation/ADOPTION_CHECK.md).
