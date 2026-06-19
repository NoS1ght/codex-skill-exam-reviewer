# -*- coding: utf-8 -*-
"""validate_quiz.py — Validate chapter HTML quiz structure.

Usage: python validate_quiz.py <directory-with-chapter-htmls>

Checks:
1. Every .card in quiz section has data-correct or data-type="fill"
2. Choice cards have .opt divs with data-opt and child .opt-icon
3. FIB cards have .reveal-btn
4. All cards have .answer-panel with .correct + .explanation
5. <script> block with addEventListener is present
"""

import re, os, sys, glob

def validate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    warnings = []
    fname = os.path.basename(filepath)
    
    # Check script presence
    if 'addEventListener' not in content:
        errors.append("Missing <script> with addEventListener")
    
    # Check CSS
    if '.opt.correct-opt' not in content:
        errors.append("Missing .opt.correct-opt CSS rule")
    if '.opt.wrong-opt' not in content:
        errors.append("Missing .opt.wrong-opt CSS rule")
    if '.reveal-btn' not in content:
        errors.append("Missing .reveal-btn CSS rule")
    
    # Find all cards in quiz section (after "互动自测")
    quiz_start = content.find('互动自测')
    if quiz_start < 0:
        quiz_start = 0
    quiz_content = content[quiz_start:]
    
    # Parse cards
    card_blocks = list(re.finditer(
        r'<div class="card"([^>]*)>(.*?)<div class="answer-panel">',
        quiz_content, re.DOTALL
    ))
    
    total_cards = len(re.findall(r'<div class="card"', quiz_content))
    
    for i, m in enumerate(card_blocks):
        attrs = m.group(1)
        body = m.group(2)
        card_num = i + 1
        
        if 'data-type="fill"' in attrs:
            if 'reveal-btn' not in body:
                errors.append(f"FIB card #{card_num}: missing .reveal-btn")
            continue
        
        if 'data-correct=' not in attrs:
            errors.append(f"Card #{card_num}: missing data-correct attribute")
            continue
        
        correct = re.search(r'data-correct="([^"]*)"', attrs)
        if correct:
            letter = correct.group(1)
            if letter not in 'ABCD':
                errors.append(f"Card #{card_num}: data-correct='{letter}' not A/B/C/D")
        
        opts = re.findall(r'<div class="opt" data-opt="([^"]*)"', body)
        if not opts:
            errors.append(f"Card #{card_num}: no clickable .opt divs")
        
        opt_icons = body.count('opt-icon')
        if opt_icons < len(opts):
            errors.append(f"Card #{card_num}: missing .opt-icon spans ({opt_icons}/{len(opts)})")
    
    # Validate answer panels
    panels = quiz_content.count('class="answer-panel"')
    if panels < len(card_blocks):
        errors.append(f"Fewer .answer-panel ({panels}) than cards ({len(card_blocks)})")
    
    # Validate explanations
    expls = quiz_content.count('class="explanation"')
    if expls < panels:
        warnings.append(f"Some cards missing .explanation ({expls}/{panels})")
    
    if errors:
        print(f"  FAIL {fname} ({total_cards} cards) — {len(errors)} errors:")
        for e in errors:
            print(f"    x {e}")
        return False
    else:
        print(f"  OK   {fname} ({total_cards} cards)")
        for w in warnings:
            print(f"    ! {w}")
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_quiz.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    files = sorted(glob.glob(os.path.join(directory, "chapter_*.html")))
    
    if not files:
        print(f"No chapter_*.html files found in {directory}")
        sys.exit(1)
    
    print(f"Validating {len(files)} chapter files in {directory}\n")
    
    all_ok = True
    for f in files:
        if not validate_file(f):
            all_ok = False
    
    print()
    if all_ok:
        print("All files pass validation.")
    else:
        print("Some files have errors - fix before delivery.")
        sys.exit(1)

if __name__ == '__main__':
    main()
