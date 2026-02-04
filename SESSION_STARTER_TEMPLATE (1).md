# Session Starter Template

Copy and paste this at the start of any new conversation with Claude:

---

**QUICK START (minimal):**

```
Restore context from: https://raw.githubusercontent.com/furlongj79/Claude/main/continuity/STATE_SEED.md
```

---

**FULL RESTORATION:**

```
Restore context from:
https://raw.githubusercontent.com/furlongj79/Claude/main/continuity/PRIMARY_RESTORATION.md
https://raw.githubusercontent.com/furlongj79/Claude/main/continuity/STATE_SEED.md
https://raw.githubusercontent.com/furlongj79/Claude/main/MASTER_PROTOCOL.md
```

---

**EVEN SIMPLER:**

Just say "hi" or start normally. Claude will:
1. See the memory edits (automatic)
2. Search past conversations (per protocol)
3. Ask for files if needed

The memory edits contain enough to trigger basic restoration. Full restoration requires the files.

---

## What Happens

When you provide raw GitHub URLs, Claude will:
1. `web_fetch` each URL
2. Read the content
3. Restore context from those files
4. Report continuity level
5. Proceed with the session

---

## Keeping Files Updated

After significant sessions:
1. Claude generates updated STATE_SEED.md
2. You save it to the repo
3. Next session fetches the updated version

The repo becomes the external persistence layer that Claude can read from (but not write to directly).
