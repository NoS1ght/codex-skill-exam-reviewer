# Exam Reviewer — Codex Skill

Generate chapter-by-chapter HTML study question banks from subject materials (notes, slides, textbooks, practice exams). Produces self-contained interactive HTML files with knowledge summaries and auto-grading quizzes.

## Install

```bash
codex skill install github.com/NoS1ght/codex-skill-exam-reviewer
```

Or via Codex UI: Skills → Install from GitHub → paste the repo URL.

## What it does


| Phase       | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| 1. Scan     | Reads all study files, generates one-paragraph summaries        |
| 2. Plan     | Groups files into logical chapters, waits for user confirmation |
| 3. Generate | Creates self-contained chapter HTMLs with embedded CSS/JS       |
| 4. Index    | Builds index.html navigation page linking all chapters          |
| 5. Validate | Runs validate_quiz.py to check HTML structure                   |

## Features

- ✅ Zero dependencies — open HTML in any browser
- ✅ Interactive quizzes — click-to-reveal answers with explanations
- ✅ Print-friendly — all answers auto-reveal on print
- ✅ Chinese + English support
- ✅ 8-15 questions per chapter (choice + fill-in-blank)

## File structure

```
exam-reviewer/
├── SKILL.md                    # Main skill instructions
├── agents/
│   └── openai.yaml             # Agent metadata
├── references/
│   ├── html_skeleton.html      # HTML/CSS/JS template
│   └── validate_quiz.py        # Post-generation validation
└── .gitignore
```

## License

MIT

Generate chapter-by-chapter HTML study question banks from subject materials (notes, slides, textbooks, practice exams). Produces self-contained interactive HTML files with knowledge summaries and auto-grading quizzes.

## Install

`bash codex skill install github.com/NoS1ght/codex-skill-exam-reviewer `

Or via Codex UI: Skills → Install from GitHub → paste the repo URL.

## What it does


| Phase       | Description                                                     |
| ----------- | --------------------------------------------------------------- |
| 1. Scan     | Reads all study files, generates one-paragraph summaries        |
| 2. Plan     | Groups files into logical chapters, waits for user confirmation |
| 3. Generate | Creates self-contained chapter HTMLs with embedded CSS/JS       |
| 4. Index    | Builds index.html navigation page linking all chapters          |
| 5. Validate | Runs validate_quiz.py to check HTML structure                   |

## Features

- ✅ Zero dependencies — open HTML in any browser
- ✅ Interactive quizzes — click-to-reveal answers with explanations
- ✅ Print-friendly — all answers auto-reveal on print
- ✅ Chinese + English support
- ✅ 8-15 questions per chapter (choice + fill-in-blank)

## File structure

`exam-reviewer/ ├── SKILL.md                    # Main skill instructions ├── agents/ │   └── openai.yaml             # Agent metadata ├── references/ │   ├── html_skeleton.html      # HTML/CSS/JS template │   └── validate_quiz.py        # Post-generation validation └── .gitignore`

## License

MIT
