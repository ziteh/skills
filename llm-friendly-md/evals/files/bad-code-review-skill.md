# Code Review Skill! 🎯

---

Welcome to the Code Review Skill. In this section, we will discuss how Claude should perform code reviews for software projects. This skill enables Claude to thoroughly review code changes.

## Overview

#### Introduction

This skill is about reviewing code. It can be used by developers, engineers, and other team members who write code and want feedback.

## What You Should Do

1. Read through the code carefully
2. Look for issues and problems
3. Consider the coding style
4. Think about security vulnerabilities
5. Check for bugs and logic errors

### Security Checks

Always remember that you should not forget to look at security issues:

| Check | Description | Priority |
|-------|-------------|----------|
| SQL Injection | Look for unsanitized inputs in DB queries | High |
| XSS | Check for unescaped output in HTML | High |
| Auth | Verify authentication and authorization logic | Medium |
| Secrets | Make sure no hardcoded API keys or passwords | High |

### Code Style

It's not uncommon for code to have style issues. They should be noted and communicated to the developer in a constructive way.

## How to Give Feedback

In this section we will cover how feedback should be given. It should be constructive and clear. The reviewer needs to be specific. Don't be vague.

## Output Format

```
Return your review in the following format...
```

The review should include a summary at the top.
