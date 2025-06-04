---
title: "You Are Using Cursor AI Incorrectly..."
date: 2025-04-08
ref: https://ghuntley.com/stdlib/
---


Quoting [Geoffrey Huntley](https://ghuntley.com/stdlib/):

> --- description: Cursor Rules Location globs: *.mdc --- # Cursor Rules Location Rules for placing and organizing Cursor rule files in the repository. <rule> name: cursor_rules_location description: Standards for placing Cursor rule files in the correct directory filters: # Match any .mdc files - type: file_extension pattern: &#34;\\.mdc$&#34; # Match files that look like Cursor rules - type: content pattern: &#34;(?s)<rule>.*?</rule>&#34; # Match file creation events - type: event pattern: &#34;file_create&#34; actions: - type: reject conditions: - pattern: &#34;^(?!\\.\\/\\.cursor\\/rules\\/.*\\.mdc$)&#34; message: &#34;Cursor rule files (.mdc) must be placed in the .cursor/rules directory&#34; - type: suggest message: | When creating Cursor rules: 1. Always place rule files in PROJECT_ROOT/.cursor/rules/: ``` .cursor/rules/ ├── your-rule-name.mdc ├── another-rule.mdc └── ... ``` 2. Follow the naming convention: - Use kebab-case for filenames - Always use .mdc extension - Make names descriptive of the rule's purpose 3. Directory structure: ``` PROJECT_ROOT/ ├── .cursor/ │ └── rules/ │ ├── your-rule-name.mdc │ └── ... └── ... ``` 4. Never place rule files: - In the project root - In subdirectories outside .cursor/rules - In any other location examples: - input: | # Bad: Rule file in wrong location rules/my-rule.mdc my-rule.mdc .rules/my-rule.mdc # Good: Rule file in correct location .cursor/rules/my-rule.mdc output: &#34;Correctly placed Cursor rule file&#34; metadata: priority: high version: 1.0 </rule>