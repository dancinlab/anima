#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        return fm_text, content[match.end():]
    return "", content

def parse_yaml_simple(fm_text):
    """Simple YAML parser for key fields."""
    result = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"\'')
            result[key] = val
    return result

def count_falsifiers(body):
    """Count falsifier items in markdown."""
    if '## Falsifier' in body or '## Falsifiers' in body:
        # Find section and count list items
        match = re.search(r'## Falsifier[s]?\n(.*?)(?=\n##|\Z)', body, re.DOTALL)
        if match:
            section = match.group(1)
            items = re.findall(r'^\s*[-*]\s+', section, re.MULTILINE)
            return len(items)
    return 0

def extract_math_signals(content):
    """Find math tokens and formula indicators."""
    signals = []
    if re.search(r'\$.*?\$', content):
        signals.append('latex')
    if re.search(r'equation|formula|closed-form', content, re.I):
        signals.append('equation')
    if re.search(r'[\d.]+\s*(?:×|×|·|\*|x)\s*10\^', content):
        signals.append('scientific-notation')
    if re.search(r'\b(?:integer|whole|natural|prime|fibonacci|sequence)\b', content, re.I):
        signals.append('integer-identity')
    if re.search(r'dimensional|unit|dimension', content, re.I):
        signals.append('dimensional-analysis')
    if re.search(r'constant|value|parameter', content, re.I):
        signals.append('constant-value')
    if re.search(r'predict|prediction|forecast', content, re.I):
        signals.append('prediction')
    if re.search(r'falsif|test|experiment|verif', content, re.I):
        signals.append('falsifiable')
    return ','.join(signals) if signals else ''

def classify_file(filepath):
    """Classify a single hypothesis file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract frontmatter and body
        fm_text, body = extract_frontmatter(content)
        fm = parse_yaml_simple(fm_text)
        
        # Extract fields
        file_id = fm.get('id', Path(filepath).stem)
        title = fm.get('title', '')
        status = fm.get('status', 'unknown')
        domain = fm.get('domain', '')
        
        # Check for merged status
        if status.startswith('merged-to-H_'):
            merged_to = status.replace('merged-to-', '')
            return {
                'id': file_id,
                'class': 'MERGED',
                'domain': domain,
                'status': status,
                'title': title,
                'merged_to': merged_to,
                'verifiable_claim': '',
                'falsifier_count': 0,
                'math_signal': ''
            }
        
        # Check for stub (Migration TODO with minimal content)
        lines = body.strip().split('\n')
        if 'Migration TODO' in body and len([l for l in lines if l.strip()]) < 5:
            return {
                'id': file_id,
                'class': 'STUB',
                'domain': domain,
                'status': status,
                'title': title,
                'merged_to': '',
                'verifiable_claim': '',
                'falsifier_count': 0,
                'math_signal': ''
            }
        
        # Check for dead/suspended
        if 'suspended' in status.lower() or 'dead' in status.lower() or 'duplicate' in status.lower():
            return {
                'id': file_id,
                'class': 'DEAD',
                'domain': domain,
                'status': status,
                'title': title,
                'merged_to': '',
                'verifiable_claim': '',
                'falsifier_count': 0,
                'math_signal': ''
            }
        
        # Extract signals
        math_signal = extract_math_signals(content)
        falsifier_count = count_falsifiers(body)
        
        # Check for concrete prediction/formula
        has_equation = bool(re.search(r'\$.*?\$|formula|closed-form', content, re.I))
        has_prediction = bool(re.search(r'## Prediction|numerical|value of', body, re.I))
        has_physics_constant = bool(re.search(r'(?:c|h|G|k_B|e|m_e|α|ℏ|π|φ)', content))
        has_falsifier = falsifier_count > 0
        has_atlas = 'atlas' in content.lower() or 'anchor' in content.lower()
        has_hypothesis = bool(re.search(r'## Hypothes|## Claim|## Main', body, re.I))
        
        # Classification logic
        ripe_score = sum([has_equation, has_prediction, has_physics_constant, has_falsifier, has_atlas])
        borderline_score = has_hypothesis and ripe_score < 3
        
        if ripe_score >= 2:
            claim = extract_first_claim(body)
            return {
                'id': file_id,
                'class': 'RIPE',
                'domain': domain,
                'status': status,
                'title': title,
                'merged_to': '',
                'verifiable_claim': claim,
                'falsifier_count': falsifier_count,
                'math_signal': math_signal
            }
        elif has_hypothesis and len(body.strip()) > 200:
            claim = extract_first_claim(body)
            return {
                'id': file_id,
                'class': 'BORDERLINE',
                'domain': domain,
                'status': status,
                'title': title,
                'merged_to': '',
                'verifiable_claim': claim,
                'falsifier_count': falsifier_count,
                'math_signal': math_signal
            }
        else:
            return {
                'id': file_id,
                'class': 'STUB',
                'domain': domain,
                'status': status,
                'title': title,
                'merged_to': '',
                'verifiable_claim': '',
                'falsifier_count': 0,
                'math_signal': ''
            }
    
    except Exception as e:
        return {
            'id': Path(filepath).stem,
            'class': 'ERROR',
            'error': str(e)
        }

def extract_first_claim(body):
    """Extract first substantial claim from body."""
    # Look for hypothesis section
    match = re.search(r'## Hypothes.*?\n\n(.*?)(?:\n##|\Z)', body, re.DOTALL)
    if match:
        text = match.group(1).strip()
        sentences = re.split(r'[.!?]\s+', text)
        if sentences:
            claim = sentences[0].strip()
            if len(claim) > 10 and len(claim) < 200:
                return claim + '.'
    
    # Fallback: first paragraph
    para = re.search(r'^\s*([^#\n][^\n]*[.!?])', body, re.MULTILINE)
    if para:
        text = para.group(1).strip()
        if 10 < len(text) < 200:
            return text
    
    return ''

if __name__ == '__main__':
    output_file = '/tmp/triage_4.jsonl'
    
    # Read file list
    with open('/tmp/hc_batch_4.txt', 'r') as f:
        lines = f.readlines()
    
    base_path = '/home/summer/mac_home/core/anima'
    
    with open(output_file, 'w') as out:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            filepath = f"{base_path}/{line}"
            result = classify_file(filepath)
            out.write(json.dumps(result) + '\n')
    
    print(f"Processed {len(lines)} files -> {output_file}")
