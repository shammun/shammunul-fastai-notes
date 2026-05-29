# Shammunul's fast.ai Part 2 Notes

A growing collection of detailed notebooks, mathematical derivations, and educational blog posts as I work through the [fast.ai Part 2 course](https://github.com/fastai/course22p2) and related topics in deep learning.

## Index

<!-- INDEX_TABLE_START -->
| Title | Type | Topic | Published | Link |
|---|---|---|---|---|
| Notebook 10: Activation Statistics — Monitoring Your Neural Network | Notebook | Activations | 2026-05-28 | [View](https://shammun.github.io/shammunul-fastai-notes/notebooks/10_activations_explained.html) |
<!-- INDEX_TABLE_END -->

## What's here

- **Notebooks** — Annotated walkthroughs of the fast.ai Part 2 notebooks. Detailed comments, "what does this code do" markdown blocks, and deep-dive sections for fundamental concepts.
- **Derivations** — Standalone mathematical walkthroughs that derive every equation from first principles, with code that verifies the math.
- **Blog posts** — Educational explanations of single concepts for readers with rudimentary math/stats/ML background. Interactive visualizations included.

## About

I'm Shammunul Islam, a PhD student in Climate Dynamics at George Mason University, applying deep learning to climate and Earth observation problems. These notes reflect my own learning process — corrections and questions welcome via [issues](https://github.com/shammun/shammunul-fastai-notes/issues).
```

The HTML comments `<!-- INDEX_TABLE_START -->` and `<!-- INDEX_TABLE_END -->` are critical — the `publish-to-github` skill uses them to know where to insert new rows. Don't remove them.

---

## Step 6 — Initial commit and push

```powershell
git add .
git commit -m "Initial repo structure with CSS theme and README skeleton"
git push origin main
```

If `git push` says "src refspec main does not match any" or similar, you might be on `master` instead. Try:

```powershell
git branch -M main
git push -u origin main
```

---

## Step 7 — Enable GitHub Pages

1. Go to `https://github.com/shammun/shammunul-fastai-notes/settings/pages`
2. Source: "Deploy from a branch"
3. Branch: `main`, folder: `/ (root)`
4. Click Save

GitHub will say something like "Your site is ready to be published at https://shammun.github.io/shammunul-fastai-notes/". Wait about 60 seconds, then visit that URL. You should see your README rendered as a basic page.

---

## Step 8 — Fill in `publish_config.md`

Back in your `nbs\` workspace, open `.claude\publish_config.md`. Verify the values are correct:

```yaml
github_username: shammunul
repo_name: shammunul-fastai-notes
local_repo_path: C:\Users\sislam27\Work\Climate Dynamics PHD\fast.ai\shammunul-fastai-notes
pages_url_base: https://shammun.github.io/shammunul-fastai-notes
auto_publish: false
```

The values I pre-filled assume the clone is at the path in Step 2. If you cloned somewhere else, edit `local_repo_path` to match.

---

## Step 9 — First test publish

In Claude Code (inside `nbs\`), try:

```
/html 09_learner_explained.ipynb
```

You should see the skill:
1. Read `publish_config.md`
2. Generate `notebooks/09_learner_explained.html` in the public repo
3. Ask whether to publish

Say yes. After it pushes, click the URL it reports. You should see your annotated notebook rendered with the Clean Educational theme, with a working "← All notes" breadcrumb link.

If anything in this last step doesn't work, that's the diagnostic moment — paste the error and we can fix the specific issue.

---

## What's now live

After Step 9:

- `https://shammun.github.io/shammunul-fastai-notes/` — your README index
- `https://shammun.github.io/shammunul-fastai-notes/notebooks/09_learner_explained.html` — your first published notebook
- The index table on the README now has 1 row pointing to that notebook

Every future `/html` or `/blog` invocation extends from here.
