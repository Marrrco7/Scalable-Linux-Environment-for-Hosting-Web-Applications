# Git Strategies and CI With GitHub Actions

This document outlines the implementation of the GitFlow and TrunkBased strategies where the Treading Labs web application project served us as a practical scenario to explore and dig into both strategies and their relationship with CI practices as well their impact in a DevOps environment.  
Effective Git strategies give the possibility to enhance team collaboration, ensure code quality, and make the release process more fluent.

---

## Objectives

1. [Compare Git Strategies](#git-strategies-comparison)
2. [Understand CI Workflows Implementation](#workflow-and-ci)
3. [Provide Guidelines](#guidelines)
4. [Facilitate Collaboration](#collaboration)

---

## Git Strategies Comparison

### GitFlow Strategy

This Git strategy is a more organized approach generally ideal for large scale projects, with structured branching model, where multiple branches serve a specific purpose in team collaboration.  
The GitFlow strategy provides clear organization and the security of having stable releases by testing the implementations in develop and release branches before reaching the production stage in the development life cycle.

**GitFlow branches:**

- **main:** The production ready branch containing stable releases. 
- **develop:** The active, long-lived branch where new features are integrated and tested.
- **feature:** Short lived branches created for developing new features and then merged into develop.
- **release:** Temporary branches used to prepare for production releases.
- **hotfix:** Urgent fixes for production issues in the main branch.

---

### Trunk-Based Strategy

The Trunk-Based development is a Git strategy that emphasizes rapid integration and continuous delivery. Thanks to its simplified branching complexity, the team collaboration is simplified by just focusing on a single long-lived branch, the main branch, which it contains the production ready code.  
This strategy is particularly optimal for projects and environments where fast iterations and continuous deployments are primordial, since it encourages continuous integrations by its reduced complexity, where new features can be added just by merging a feature branch directly into the main branch.

**Trunk-Based branches:**

- **main:**  
  The central branch containing production ready code.  
  All changes are merged directly into main, ensuring it's always in a deployable state.  
  New releases are taken from this branch directly.

- **feature:**  
  Short lived branches created for developing individual features, bug fixes, or improvements.  
  Feature branches are continuously integrated into main after review and testing, and ideally,  
  kept as small and focused as possible to minimize merge conflicts and integration issues.

---

### Why Trunk-Based Strategy for This Project?

Trunk-based development is a simplified strategy compared to GitFlow, and it might be particularly more suitable for this project, where dealing with CI practices is a must. GitFlow, with its develop branch and release cycles, can potentially delay testing and deployment until changes are stabilized in the release branch, which slows down feedback.  

Trunk-based pairs well with GitHub Actions, since the automation given by the GitHub workflow aligns with the focus of Trunk-based development on smaller and incremental changes, then we would be able to take maximum benefit of the GitHub Actions automation.  

In this project, simplicity and speed are priorities, therefore a leaner and easier to manage but at the same time, more efficient Trunk-based workflow, can be more benefiting for this particular project.

---

## Workflow and CI

This project incorporates a **reusable workflow** in order to improve maintainability and centralized the logic of the whole workflow if changes are meant to be done, as well as supporting the **DRY principle** of software development by avoiding redundancy, and hopefully making scalability easier in the project by avoid dealing with repetitive script on each workflow file.  
Both strategies can access the reusable workflow automatically by making calls on it when both of them are triggered by the pushes and pulls of the respective branches in each strategy that trigger each workflow in both strategies.

The reusable workflow file in the `.github/workflows` folder, named as `workflow.yaml`, is responsible to provide the functionality of getting the common jobs done when being called. It sets the Python version, installs dependencies, sets a PostgreSQL database service, runs migrations, and runs the tests previously implemented.

---

## Gitflow Workflow

Handles branch specific builds on pushes to:  
- `develop`  
- `main`  
- `feature/*`  
- `release/*`  

It injects the credentials for connecting to our database stored in GitHub Secrets and specifies the file path of the reusable workflow in order to run the common jobs.  

If the workflow is triggered by a push on a release branch, then it creates a release tag, having previously enabled the file to write contents in our repository.  

After that, it installs **GitVersion**, and creates a release tag by gathering the credentials of the user who makes the changes, and then pushing the tag to our repository.

---

## Trunk-Based Workflow

The Trunk-Based workflow is implemented in a way that it gets called when there are push or pull requests in the `main` branch.  

Similarly as in the GitHub Workflow file, it sets writing permissions for the tags, specifies the path to use the reusable file, and sets the database credentials.  

However, after that, it creates a release tag only if there is a push event directly to the `main` branch, then, same as before, it installs **GitVersion** and creates the release tag after being triggered by a push to the main branch.

---

## Guidelines

### Branching Guidelines

- **Feature Branches**  
  Always create a new feature branch for every new implementation with the following format: `feature/description`.  
  Keep feature branches short lived and merge frequently to avoid merge conflicts.

### Commit Messages

- Write clear commit messages, so it is easier to understand the new additions of each developer.

### Pull Requests

- Ensure that all the PRs have a clear description of the changes made.
- Link related tasks or issues in the PR description, and request at least one review before merging into main.
- Along with that, check constantly the CI pipeline to ensure that there are no failures when merging branches or pushing new code.

---

