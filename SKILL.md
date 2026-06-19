---
name: exam-reviewer
description: Chapter-by-chapter HTML study quiz bank generator from subject materials. Use when the user provides a folder of study materials (notes, slides, textbooks, practice exams) and asks to generate review quizzes, study aids, or exam prep HTML pages.
---

# Exam Reviewer

Generate chapter-by-chapter HTML study question banks. The user provides a folder of subject materials; you produce self-contained HTML files — one per chapter — each with a core knowledge summary and an interactive quiz section. Every HTML file must be self-contained (no CDN, no external files, no frameworks) and open directly in any browser.

## Output Location

**ALL generated files MUST be placed in `agentquiz/` subfolder inside the user-provided materials folder.** Do NOT output files to the materials folder root or to the workspace root.

Example: if user provides `D:\study\数据挖掘`, output to `D:\study\数据挖掘\agentquiz\`.

The `agentquiz/` folder structure:
```
<user-materials-folder>/
├── agentquiz/                   ← All generated files here
│   ├── _review_plan.md          ← Scan summaries + chapter plan
│   ├── index.html               ← Navigation index
│   ├── chapter_1_name.html
│   ├── chapter_2_name.html
│   ├── ...
│   └── images/                  ← Extracted images (if any)
├── 复习资料/                    ← Original materials (DO NOT TOUCH)
└── 作业/                        ← Original materials (DO NOT TOUCH)
```

**Rules:**
- Create `agentquiz/` if it doesn't exist.
- Never modify or move any original material files.
- If Markdown references local images, copy them to `agentquiz/images/` (flatten the path with underscores to avoid nesting issues).

## Workflow

### Phase 1: Scan & Summarize

1. Get the folder path from the user (use the path they already gave if provided).
2. Recursively list all files in that folder.
3. Read each file just enough to write a **one-paragraph summary** (3–5 sentences) capturing: what the file covers, key topics, and question types if it contains practice problems.
4. Store these summaries in a **plan file** at `<materials-folder>/agentquiz/_review_plan.md`. This file persists across chapters. Do NOT load full file contents into context beyond what is needed for the summary.

### Phase 2: Chapter Planning

1. From the summaries, group related files into logical chapters (typically 4–8 chapters). Match the subject's natural textbook/module structure.
2. Append a chapter outline to `agentquiz/_review_plan.md`:
   ```markdown
   ## Chapter Plan
   1. Chapter Name — files: a.md, b.pdf
   2. Chapter Name — files: c.md, d.txt
   ...
   ```
3. Present the plan to the user. **Wait for confirmation** (or adjustments) before proceeding.

### Phase 3: Generate HTML Chapter by Chapter

For each chapter in order:

1. Re-read only the files assigned to this chapter. Load their full content now.
2. Generate a single self-contained HTML file: `agentquiz/chapter_N_name.html`.
3. Use the exact HTML structure, CSS, and JS from the **HTML Template** section below. Do NOT invent your own quiz interaction.
4. After generating, **keep all previous chapter HTMLs** — do not delete them.
5. **Append a "← Back to Index" button** at the end of every chapter HTML (after `</div></div>` and before `<script>`), using the exact snippet from the **Back-to-Index Button** section below.
6. Move to the next chapter.

**Context management:** After finishing each chapter, reset context — only keep `agentquiz/_review_plan.md` and the current chapter HTML. Re-read chapter files fresh for each chapter.

### Phase 4: Generate index.html

After all chapters are generated and validated:

1. Generate `agentquiz/index.html` using the **Index Page Template** below.
2. `index.html` links to every chapter HTML via relative paths (same-folder references, e.g. `href="chapter_1_name.html"`).
3. Ensure the index page summarizes total chapter count, question counts (choice + fill), and a brief description per chapter.
4. The index page must also be self-contained (no CDN).

### Phase 5: Post-Generation Validation

After generating all chapters and index:

1. Run `references/validate_quiz.py` against the `agentquiz/` folder.
2. Fix any reported issues before delivering.
3. Confirm `agentquiz/index.html` links all resolve correctly.

---

## HTML Template (MANDATORY)

Every chapter HTML file uses the following exact structure. Read `references/html_skeleton.html` for the complete skeleton. Core rules:

### Structure

```
[Chapter Title with h1]
├── Section 1 — Core Knowledge Summary (.section)
│   ├── h3 sub-topic headers
│   ├── Bullet points — concise, exam-oriented
│   ├── Key formulas / definitions in .highlight or .key-point
│   └── Comparison tables / mnemonics
├── Section 2 — Interactive Quiz (.section)
│   ├── h3 "—— 选择题 ——" header
│   ├── Choice question cards (.card with data-correct)
│   ├── h3 "—— 填空题 ——" header
│   └── Fill-in-blank cards (.card with data-type="fill")
└── Back to index button (centered link to index.html)
```

### Back-to-Index Button

Every chapter HTML MUST include the following button between the quiz section closing `</div></div>` and the `<script>` tag:

```html
<div style="text-align:center;margin:20px 0 40px;">
  <a href="index.html" style="display:inline-block;background:#1a237e;color:#fff;text-decoration:none;padding:10px 36px;border-radius:6px;font-size:0.95em;transition:background 0.2s;" onmouseover="this.style.background='#283593'" onmouseout="this.style.background='#1a237e'">← 返回索引页</a>
</div>
```

Place it exactly here in the document structure:
```html
  </div>   <!-- closes .section (quiz) -->
</div>     <!-- closes .container -->

<!-- === BACK BUTTON HERE === -->

<script>  <!-- quiz JS -->
```

### Choice Question Card Template

```html
<div class="card" data-correct="C">
  <div class="card-header">
    <span class="q-num">Q1</span>
    <span class="q-text">Question text ( )</span>
    <span class="q-type">单选</span>
  </div>
  <div class="options">
    <div class="opt" data-opt="A"><span class="opt-letter">A.</span> Option text<span class="opt-icon"></span></div>
    <div class="opt" data-opt="B"><span class="opt-letter">B.</span> Option text<span class="opt-icon"></span></div>
    <div class="opt" data-opt="C"><span class="opt-letter">C.</span> Option text<span class="opt-icon"></span></div>
    <div class="opt" data-opt="D"><span class="opt-letter">D.</span> Option text<span class="opt-icon"></span></div>
  </div>
  <div class="answer-panel">
    <div><span class="correct">✓ C</span></div>
    <div class="explanation"><b>解析：</b>Explanation of why C is correct and why others are wrong.</div>
  </div>
</div>
```

Key attributes:
- Card: `data-correct="C"` — the correct option letter (A/B/C/D)
- Each `.opt`: `data-opt="A"` — the option letter
- Each `.opt` contains `.opt-letter` span + text + `.opt-icon` span
- `.answer-panel` contains `.correct` answer indicator + `.explanation`
- **Do NOT use `<button>` or toggle buttons inside choice cards**

### Fill-in-Blank Card Template

```html
<div class="card" data-type="fill">
  <div class="card-header">
    <span class="q-num">FIB_1</span>
    <span class="q-text">Question text with __________ blanks.</span>
    <span class="q-type">填空</span>
  </div>
  <button class="reveal-btn" onclick="var p=this.parentElement.querySelector('.answer-panel');p.classList.add('show');this.classList.add('done');">▶ 点击查看答案</button>
  <div class="answer-panel">
    <div><span class="correct">Answer text</span></div>
    <div class="explanation"><b>解析：</b>Explanation.</div>
  </div>
</div>
```

### CSS — Always include these exact styles

Use the complete CSS block from `references/html_skeleton.html`. Key interactive classes:

| Class | Purpose |
|-------|---------|
| `.opt` | Clickable option — border, padding, cursor:pointer |
| `.opt:hover:not(.selected)` | Hover highlight (blue border) |
| `.opt.selected` | Lock after click — pointer-events:none |
| `.opt.correct-opt` | Green highlight + ✓ icon |
| `.opt.wrong-opt` | Red highlight + ✗ icon |
| `.answer-panel` | display:none by default; `.show` reveals it |
| `.reveal-btn` | FIB reveal button |
| `.reveal-btn.done` | Hidden after click |

### JavaScript — Always include this exact script

```html
<script>
(function(){
  document.querySelectorAll('.card').forEach(function(card){
    var correct = card.getAttribute('data-correct');
    if (!correct) return;
    var opts = card.querySelectorAll('.opt');
    var panel = card.querySelector('.answer-panel');
    opts.forEach(function(opt){
      opt.addEventListener('click', function(){
        if (opt.classList.contains('selected')) return;
        opts.forEach(function(o){ o.classList.add('selected'); });
        var letter = opt.getAttribute('data-opt');
        if (letter === correct) {
          opt.classList.add('correct-opt');
          opt.querySelector('.opt-icon').textContent = '\u2713';
        } else {
          opt.classList.add('wrong-opt');
          opt.querySelector('.opt-icon').textContent = '\u2717';
          var correctOpt = card.querySelector('.opt[data-opt="' + correct + '"]');
          if (correctOpt) {
            correctOpt.classList.add('correct-opt');
            correctOpt.querySelector('.opt-icon').textContent = '\u2713';
          }
        }
        if (panel) panel.classList.add('show');
      });
    });
  });
})();
</script>
```

### Print-friendly rules

- `@media print`: white bg, no shadows, all `.answer-panel` shown, `.opt` non-clickable, `.reveal-btn` hidden.
- Use `break-inside:avoid` on `.section` to keep question cards together.

---

## Index Page Template

After all chapters are generated, produce `agentquiz/index.html`. The index must be self-contained and include:

### Required sections

1. **Header** — subject name + subtitle (e.g. semester/year info)
2. **Stats row** — total chapters, total questions, total choice, total fill-in-blank
3. **Tips box** — usage advice (review summary first, then quiz; print support; goal: all correct = mastered)
4. **Chapter cards** — one clickable card per chapter, each containing:
   - Chapter number (e.g. 第一章)
   - Chapter title (linked to `chapter_N_name.html`)
   - One-line topic description
   - Question count metadata (X 选择题 + Y 填空题)
5. **Footer** — course/institution info (optional)

### CSS styles for index

Use the same font/color scheme as chapter HTMLs. Key styles:

```css
.stats { display:flex; justify-content:center; gap:20px; flex-wrap:wrap; }
.stat-card { background:#fff; padding:16px 28px; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center; min-width:100px; }
.stat-card .num { font-size:2em; font-weight:700; color:#1a237e; }
.chapter-card { background:#fff; border-radius:10px; padding:20px 28px; box-shadow:0 2px 8px rgba(0,0,0,0.08); text-decoration:none; color:#222; display:block; transition:all 0.2s; border-left:5px solid #3949ab; }
.chapter-card:hover { transform:translateX(4px); box-shadow:0 4px 16px rgba(0,0,0,0.14); border-left-color:#1a237e; }
```

### Chapter card HTML

```html
<a class="chapter-card" href="chapter_1_name.html">
  <div class="ch-num">第一章</div>
  <div class="ch-title">Chapter Title</div>
  <div class="ch-desc">Brief topic list — one line</div>
  <div class="ch-meta">10 选择题 + 5 填空题</div>
</a>
```

---

## Quiz Interaction Behavior

**Choice questions (选择题):**
1. Default: all options show, answer panel hidden.
2. User clicks an option → selected option gets ✓ (correct) or ✗ (wrong).
3. If wrong choice, the correct option is simultaneously highlighted green.
4. All options become locked (no re-selection).
5. Answer panel auto-reveals with explanation.

**Fill-in-blank (填空题):**
1. User clicks "▶ 点击查看答案" button.
2. Button disappears, answer panel shows.
3. **No scoring, no input matching.** User self-checks by reading the revealed answer.

---

## Post-Generation Validation

After generating all chapters, validate the HTML files using `references/validate_quiz.py`. This script:

1. Checks that every `.card` inside a quiz section has `data-correct` (choice) or `data-type="fill"` (FIB).
2. Verifies that `.opt` divs have `data-opt` attributes and child `.opt-icon` spans.
3. Confirms the `<script>` block is present.
4. Reports any cards missing correct answers or malformed options.

Run it:
```bash
python references/validate_quiz.py <materials-folder>/agentquiz
```

If validation fails, fix the reported issues before delivering to the user.

---

## Mixing Question Types

Each chapter should have **8–15 total questions**, mixing:
- 6–10 single choice (单选) — core
- 2–6 fill-in-blank (填空) — for key definitions/formulas

Use the `<h3 style="color:#e65100;">—— 填空题 ——</h3>` header to separate FIB from choice questions.

---

## Question Coverage

**Every major sub-topic in the knowledge summary must have at least one corresponding quiz question.** Cross-check the summary bullet points against the quiz questions before finalizing each chapter. Prioritize high-frequency exam topics, but do not skip any sub-topic entirely — a student should be able to test themselves on every知识点 covered in the summary.

## Content Guidelines

- **Knowledge summary**: Concise, organized by h3 sub-topics. Use `.highlight` for key terms, `.key-point` for formulas/critical notes, `.mnemonic` for memory aids.
- **Quiz questions**: Based on the source materials. Cover all major sub-topics. Include both factual recall and conceptual reasoning.
- **Explanations**: For each choice question, explain why the correct answer is right AND why each wrong option is wrong.
- **Language**: Match the source materials' language (typically Chinese for Chinese university courses).

---

## After All Chapters

When all chapters + index are generated and validated:
- Confirm the user can open `agentquiz/index.html` and navigate to any chapter.
- Ask if the user would like to:
  - Revise any specific chapter
  - Adjust quiz difficulty
  - Export or print as PDF