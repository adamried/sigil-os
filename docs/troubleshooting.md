# Troubleshooting Guide

> Take a breath. Most problems have a quick fix. This page walks you through the common ones step by step.

---

## Quick Diagnosis

Find your symptom in the table below and jump to the matching section.

| Symptom | Likely Cause | Quick Fix | Section |
|---------|--------------|-----------|---------|
| "Maximum clarification rounds reached" | Vague requirements | Simplify scope | [Clarification Limits](#clarification-limits) |
| "QA (quality check) validation failed after 5 attempts" | Design conflict | Review with tech lead | [Quality-Check Loop Issues](#quality-check-loop-issues) |
| Unexpected output format | Context mix-up | Start fresh | [Unexpected Output](#unexpected-output) |
| Missing context from a previous session | Session state issue | Check context files | [Session Recovery](#session-recovery) |
| Feature takes wrong direction | Unclear first description | Rewrite your description | [Wrong Direction](#wrong-direction) |
| "No config file found" | Config not yet created | Run `/sigil:config set` to create it | [Configuration Issues](#configuration-issues) |
| "Directed mode requires technical track" | Incompatible settings | Set user_track to technical first | [Configuration Issues](#configuration-issues) |
| "Specialist file not found" | Missing specialist file | Automatic fallback to base agent | [Specialist Issues](#specialist-issues) |
| Standards not in constitution | Not connected or empty standards | Run `/sigil:connect` | [Shared Standards Issues](#shared-standards-issues) |
| "@inherit-pending" in constitution | Standard file missing from shared repo | Create the file in shared-standards/ | [Shared Standards Issues](#shared-standards-issues) |
| Standards conflict warning | Local rule contradicts shared standard | Resolve, waive, or skip | [Shared Standards Issues](#shared-standards-issues) |

---

## Clarification Limits

### What You See

```
Clarification round 3 of 3 complete.
Maximum clarification cycles reached.
Some ambiguities may remain unresolved.
```

### Why This Happens

Sigil allows up to 3 rounds of back-and-forth questions. After that, it stops asking. This usually means one of four things:

- The first description was too short or vague.
- Two requirements conflict with each other.
- The feature scope is too large for one pass.
- Answers to questions were unclear or partial.

### Fix 1 -- Shrink the Scope

Break the feature into smaller pieces.

Instead of:
> "Build a complete user management system"

Try:
> "Add user sign-up with email and password"

You can create separate features for login, profiles, and admin controls later.

### Fix 2 -- Give Direct Answers

When Sigil asks a question, pick one clear option.

Instead of:
> "Maybe option B, but it depends"

Try:
> "Option B. We need password reset via email because our users often forget passwords."

### Fix 3 -- Start Over with More Detail

Run `/sigil:draw "description"` again with a richer description. Try to answer common questions before they come up.

Instead of:
> "Add a contact form"

Try:
> "Add a contact form with name, email, and message fields. Show a success notice on submit. Send an email copy to the user. Use honeypot spam protection. The form must work on mobile and meet accessibility standards."

> **Tip:** Before you type `/sigil:draw "description"`, write down three things: who uses the feature, what they do, and what they see when it works. That alone prevents most clarification loops.

---

## Quality-Check Loop Issues

### What You See

```
QA fix cycle 5 of 5 complete.
Maximum fix attempts exceeded.
Escalating to human review.
```

QA (quality assurance -- the step where Sigil checks each task right after it is built) tried to fix an issue five times on a single task and could not.

### Why This Happens

This usually points to a deeper problem, not a simple bug.

- The requirements may ask for two things that contradict each other.
- The implementation may break a rule in your constitution (the file that holds your project's principles and standards).
- What was requested may not be possible with the current setup.
- The specification (your written feature description) may be missing key details.

### How to Fix

1. Run `/sigil:draw` and look at which check keeps failing.
2. Share the output with your tech lead.
3. Pick the right action from the table below.

| Problem Type | What to Do |
|--------------|------------|
| Contradicting requirements | Keep one, remove the other |
| Constitution rule conflict | Update the constitution or change approach |
| Technical limit | Adjust the feature to fit what is possible |
| Missing information | Add the missing details to your specification |

4. Run `/sigil:draw continue` to regenerate the plan and tasks with the corrected information.

You should now see the quality check pass on the next run.

> **Note:** If you are unsure which problem type applies, share the full `/sigil:draw` output with your tech lead. They can pinpoint the root cause.

---

## Unexpected Output

### What You See

- Specifications that miss key requirements you asked for.
- Plans that seem unrelated to your feature.
- Tasks that do not match the plan.

### Why This Happens

- Context from an earlier conversation may be leaking in.
- Your description may have been read differently than you meant.
- Your project may not have a constitution (project-principles file) yet.

### Fix 1 -- Start a Fresh Session

Run the command below and type out your full feature description. Do not assume Sigil remembers anything from before.

```
/sigil:draw "description" [your complete feature description]
```

You should now see a new specification that matches your description.

### Fix 2 -- Check Your Constitution

Run `/sigil:constitution` and review the technology choices and standards listed. If they do not match your project, update them.

```
/sigil:constitution
```

You should now see a constitution that reflects your real project rules.

### Fix 3 -- Be More Specific

Leave no room for guesswork.

Instead of:
> "Make the dashboard better"

Try:
> "Add a filter to the dashboard that lets users show only items from the last 7 days. The filter should be a dropdown with options: Today, Last 7 Days, Last 30 Days, All Time."

> **Tip:** Use concrete examples with real names, real numbers, and real labels. The more specific you are, the closer the output will be to what you want.

---

## Session Recovery

### What You See

- Sigil does not remember your previous work.
- `/sigil:draw` shows no active features.
- You are asked to set up a constitution again.

### Why This Happens

Sigil stores its state in a `.sigil/` folder inside your project. If that folder is missing, moved, or damaged, Sigil starts with a blank slate. Starting from a different folder can also cause this.

### How to Fix

1. Make sure you opened your terminal in the same project folder you used before.
2. Check that a `.sigil/` folder exists inside your project.
3. Open the `.sigil/` folder and confirm it contains files.
4. If the files are gone, run `/sigil:constitution` to recreate your project principles.
5. Run `/sigil:draw "description"` to restart your feature.

```
$ ls .sigil/
project-context.md   decisions.md   ...
```

You should now see your project state restored or a clean starting point ready to go.

> **Warning:** Do not delete the `.sigil/` folder. It holds all of Sigil's saved context for your project. Losing it means starting over.

---

## Wrong Direction

### What You See

- The plan includes approaches you did not want.
- Tasks cover features you did not ask for.
- Technical choices do not match your expectations.

### Why This Happens

Sigil fills in gaps when your description leaves room for guesses. Rushed answers to clarification questions and unexpected constitution rules can also steer things off course.

### Caught Early (Before Tasks Start)

1. Run `/sigil:draw` and read the specification carefully.
2. Run `/sigil:draw continue` to correct the parts that are wrong.
3. Run `/sigil:draw continue` to generate a new plan.

```
$ /sigil:draw continue
Plan generated: 4 tasks across 2 phases.
Ready for review.
```

You should now see a plan that matches your intent.

### Caught Late (During Building)

1. Stop the current implementation.
2. Open the specification and find what went wrong.
3. Update the specification with corrected requirements.
4. Run `/sigil:draw continue` to regenerate work items.

```
$ /sigil:draw continue
Tasks regenerated: 3 tasks.
Ready for implementation.
```

You should now see new tasks that reflect your corrected requirements.

> **Tip:** Before you approve any specification, read it all the way through. A few minutes of review here can save hours of rework later.

---

## Override Options

Sometimes you need to override a Sigil decision. Use overrides with care.

### When Overrides Make Sense

| Situation | What to Do |
|-----------|------------|
| A constitution rule does not apply to this feature | Document the exception in your specification |
| Your team prefers a different technical choice | State the preference in the requirements |
| An iteration limit was hit but progress was being made | Review the output and continue by hand |

### When NOT to Override

| Situation | Better Approach |
|-----------|-----------------|
| A security check is failing | Fix the security issue |
| Tests will not pass | Find and fix the root cause |
| A constitution rule conflicts | Update the constitution the right way |

### How to Record an Override

Add a section to your specification like the example below.

```markdown
## Exceptions

**Exception:** Using token-only sessions instead of database sessions.
**Reason:** This feature is read-only and does not need session revocation.
**Approved by:** [Name, Date]
```

---

## Configuration Issues

### "No config file found"

Your personal configuration file (`.sigil/config.yaml`) hasn't been created yet. Sigil uses defaults (`non-technical` track, `automatic` mode, `audit_mode: false`) when the file is missing. To create it explicitly:

```
/sigil:config set user_track non-technical
```

### Migrating from older versions

If you upgraded from Sigil 0.23.0 or earlier, your configuration may still be in the `## Configuration` section of `SIGIL.md`. The next time you run `/sigil:draw`, the preflight check automatically migrates your settings to `.sigil/config.yaml` and removes the old section from SIGIL.md. No action needed.

### "Directed mode requires the technical track"

You tried to set `execution_mode: directed` while your `user_track` is `non-technical`. Directed mode is for engineers who want to manually control specialist selection. Switch to the technical track first:

```
/sigil:config set user_track technical
/sigil:config set execution_mode directed
```

### Configuration YAML Parse Error

If `/sigil:config` reports formatting issues, reset to defaults:

```
/sigil:config reset
```

This restores the default configuration in `.sigil/config.yaml`.

---

## Specialist Issues

### "Specialist file not found"

A task was assigned a specialist that does not exist in `agents/specialists/`. Sigil falls back to the base agent automatically. This is not a blocker -- the task will still be built, just without the specialist's domain-specific focus.

### Task Uses Wrong Specialist

If you notice a task being handled by the wrong specialist (visible in technical track), the specialist-selection system may have matched on file path or keywords incorrectly. This does not cause errors -- the base agent behavior still applies. The specialist only adds domain-specific priorities on top.

### Specialist Has No Effect

Specialists only add overrides to their base agent. If a task is very generic (like creating a directory or installing a dependency), the specialist and base agent produce the same result. This is expected for setup tasks.

---

## Shared Standards Issues

### Standards not appearing in constitution

Your constitution does not show any `@inherit` markers or shared standard content.

**Likely causes:**
- Shared context is not active. Run `/sigil:connect` to connect to a shared repo.
- The shared repo's `shared-standards/` directory is empty. Add standards files there first.
- You set up your constitution before connecting. Run `/sigil:connect` again — it will offer to apply available standards to your existing constitution.

### "@inherit-pending" marker in constitution

```
<!-- @inherit-pending: security-standards.md -->
```

The constitution references a shared standard file that does not exist in the shared repo yet.

**Fix:** Create the referenced file in `shared-standards/` in your shared repo on GitHub. The marker will be replaced with actual content on your next `/sigil:draw` session start.

### Standards conflict warning at session start

```
⚠️  Standards Discrepancy Detected
  Shared standard requires: 80% test coverage
  Your local rule says: 60% coverage target
```

Your local rules conflict with a shared standard. Sigil asks you to resolve the conflict.

**Options:**
1. **Update local rule** — change your constitution to match the shared standard
2. **Log a waiver** — keep your local rule and record an exception
3. **Skip** — decide later (the warning will repeat next session)

### Required standard blocks session

```
🚫 Required Standard Missing
  Article 4: Security Mandates (required)
  Your organization requires this standard...
```

A shared standard with enforcement level "required" is not applied to your constitution. Sigil blocks the session until this is resolved.

**Options:**
1. **Apply now** — Sigil adds the `@inherit` marker and expands the standard into your constitution
2. **Request waiver** — log an exception for your team lead to review

**Note:** Required standards are set by whoever manages your shared repo. If you believe a standard should not be required, contact your team lead.

### Ticket key not recognized

```
No integration configured for project "PROJ".
```

You tried `/sigil:draw PROJ-123` but Sigil doesn't have an adapter configured for that project prefix.

**Likely causes:**
- No shared context connection. Run `/sigil:connect` first.
- The shared repo doesn't have an `integrations/` directory with adapter configs.
- The project prefix doesn't match any `project_keys` in the adapter config.

**Fix:** Check `.sigil/config.yaml` for an `integrations:` section. If missing, connect to a shared repo that has adapter configs, or add one manually.

### No adapter configured

```
{Adapter name} MCP is not configured in this session.
```

An adapter was found for the ticket prefix but the required MCP tools are not available.

**Fix:** Configure the required MCP server. For Jira, you need the Atlassian MCP connection. You can still describe the feature in plain text as a fallback.

### @inherit not expanding at session start

The `@inherit` markers exist but the content between start/end markers is not updating.

**Likely causes:**
- GitHub MCP is not available. Check your MCP connection.
- The shared repo is unreachable. Sigil keeps the previously expanded content until the connection returns.
- The constitution file is not at the expected path (`/.sigil/constitution.md`).

**Fix:** Run `/sigil:draw` and check the status output. If it shows "Shared context unavailable," your MCP connection needs attention.

### Override expired warning

```
⚠️  Override Expired
  Article 3: Testing Requirements
  Override: Reduce coverage target to 50%
  Expired: 2026-02-15
```

An override in `/.sigil/waivers.md` has passed its expiration date. The original constitution rule is now in effect.

**Options:**
1. **Acknowledge** — accept that the original rule applies again
2. **Extend** — set a new expiration date for the override
3. **Convert to permanent** — make the override permanent (no expiration)

### Handoff-back failed

```
⚠️  Ticket PROJ-123 partially updated:
  ✅ Summary posted
  ⚠️  Status transition failed
```

After a feature completes, Sigil tried to update the originating ticket but one or more steps failed.

**Likely causes:**
- The ticket's workflow doesn't allow the transition Sigil attempted
- Your permissions don't include status changes
- The MCP connection dropped

**Fix:** Update the ticket status manually in your issue tracker. The summary comment was posted successfully, so the implementation details are captured.

---

## Error Categories

Sigil groups errors into three types. Knowing which type you are facing helps you respond the right way.

### Soft Errors (Fix Themselves)

These are small problems like formatting issues, minor validation failures, or brief network timeouts. Sigil retries up to 3 times on its own.

**Your action:** Usually nothing. These resolve without your help.

### Hard Errors (Need Your Input)

These happen when Sigil finds unclear requirements, multiple valid paths, or a scope decision only you can make. Sigil pauses and asks you to choose.

**Your action:** Review the options Sigil presents and pick one.

### Blocking Errors (Full Stop)

These are serious issues like missing required files, critical security problems, or circular task chains (where task A depends on B and B depends on A). All progress stops until the root cause is fixed.

**Your action:** Address the underlying problem before moving on.

---

## Getting More Help

### Check Existing Docs First

- [User Guide](user-guide.md) -- Full usage guide
- [Command Reference](command-reference.md) -- Every command explained
- [Example Walkthrough](examples/user-auth-feature/README.md) -- A start-to-finish example

### Before You Ask for Help, Gather This

1. What command did you run? Copy the full input.
2. What output did you get? Copy the full response.
3. What did you expect to happen?
4. Run `/sigil:constitution` and copy the output.
5. Run `/sigil:draw` and copy the output.

```
$ /sigil:draw
Phase: planning
Track: standard
Active Feature: user-auth
Status: blocked — QA fix cycle exceeded
```

Having all five items ready makes it much easier for someone to help you.

### Common Questions

**Q: How do I see what Sigil did during a workflow?**
A: Enable audit mode, then use `/sigil:audit` to review a step-by-step record of what happened. To enable: `/sigil:config set audit_mode true`. Once on, every workflow logs events automatically to `.sigil/audit-log.md`. Run `/sigil:audit` after a workflow completes to see a plain-language summary, or `/sigil:audit full` for the complete log.

**Q: Can I undo a clarification answer?**
A: Not directly. Run `/sigil:draw "description"` again to start fresh if you need to change a key decision.

**Q: How do I change the track (the complexity level -- Quick, Standard, or Enterprise)?**
A: The track is chosen based on feature size. Describe a smaller feature to get a simpler track.

**Q: Why does my feature keep getting split into multiple features?**
A: Your scope is likely too large. This is Sigil's way of saying "break it up." Try describing one focused piece at a time.

**Q: Can I skip phases?**
A: No. Each phase builds on the last. Skipping one creates gaps that cause problems later.

---

## Summary

Most issues fall into one of four buckets.

| Category | Common Cause | Solution |
|----------|--------------|----------|
| Clarification loops | Vague requirements | Be more specific up front |
| Quality-check failures | Design conflicts | Review with tech lead |
| Context issues | Session state | Check files or start fresh |
| Wrong direction | Rushed review | Read each phase output carefully |

When in doubt, start here:

1. Run `/sigil:draw` to see where things stand.
2. Review the specification for accuracy.
3. Ask your tech lead if the issue is technical.
4. Start fresh if context seems corrupted.

You should now have a clear next step for any problem you run into.

---

*For technical error handling details, developers can reference [Error Handling Protocol](dev/error-handling.md).*
