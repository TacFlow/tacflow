# ✅ Post-Deploy Validation Checklist

Use this checklist to verify everything is working after the GitHub updates.

---

## 🔄 Redirects & Infrastructure (CRITICAL — must not break)

- [ ] `git clone https://github.com/TacFlow/tacflow` works
- [ ] `git clone https://github.com/tacflow1-tech/tacflow` redirects to new URL
- [ ] One-liner installer still works (test in clean environment):
  - Windows: `iwr -useb https://get.tacflow.ai/install.ps1 | iex`
  - Linux: `curl -fsSL https://get.tacflow.ai/install.sh | bash`
- [ ] All existing release tags are accessible
- [ ] All existing release binaries are downloadable

## 📄 README & Documentation

- [ ] README.md renders correctly with all badges
- [ ] Mermaid architecture diagram renders
- [ ] All links (docs, website, community) are valid
- [ ] TAC_LANGUAGE.md is accessible
- [ ] MEMORY_ARCHITECTURE.md is accessible
- [ ] AGENT_DNA.md is accessible

## 🏷️ Profile & Branding

- [ ] Organization/user name is `TacFlow`
- [ ] Avatar/logo is displayed
- [ ] Bio describes TacFlow accurately
- [ ] Website link points to tacflow.ai
- [ ] Pinned repositories in correct order:
  1. `tacflow`
  2. `tac-language`
  3. `tacbot-edge`
  4. `tacflow-examples`

## 📂 Repository Content

- [ ] `/docs/` folder exists with 3 documents
- [ ] `/examples/` folder exists with 5 `.tac` files
- [ ] `/assets/` folder exists (with placeholders for media)
- [ ] `LICENSE` file present (Proprietary)
- [ ] Topics/tags set on each repository

## 🔗 External Links

- [ ] tacflow.ai loads and shows content
- [ ] Discord/community invite works
- [ ] Documentation site (docs.tacflow.ai) is accessible

## 🧪 Test the Narrative

- [ ] Someone visiting for the first time understands in <30s what TacFlow does
- [ ] The comparison table clearly differentiates from Hermes/CrewAI/AutoGPT
- [ ] The 3 unique pillars (TAC Language, Memory, DNA) are prominently visible
- [ ] Call-to-action (install / join community) is clear
