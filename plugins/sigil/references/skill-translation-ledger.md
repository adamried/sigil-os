# Claude-skill to Codex-procedure translation ledger

The Codex package exposes only eight outcome skills. Claude-edition internal
skills map to explicit private references as follows:

| Source skill | Codex reference owner |
|---|---|
| accessibility | draw design procedure / design role |
| design-md-generator | draw design procedure |
| design-skills-loader | external-design-skills integration |
| design-system-reader | draw design procedure |
| figma-review | Figma integration |
| framework-selector | draw design procedure |
| propose-and-confirm | setup/config plan-and-confirm behavior |
| ui-designer | draw design procedure / design role |
| ux-patterns | draw design procedure |
| adr-writer | draw planning procedure / architecture role |
| commit-conventions | draw Git protocol |
| database-migration | draw planning and implementation procedures |
| documentation-generator | draw implementation procedure |
| foundation-writer | Discovery chain / architecture role |
| refactoring-backend | draw implementation procedure |
| refactoring-frontend | draw implementation procedure |
| task-decomposer | draw tasks procedure / task-planning role |
| technical-planner | draw planning procedure / architecture role |
| test-generator | draw tasks, implementation, and validation procedures |
| jira | Jira integration |
| learning-capture | learn workflow |
| learning-reader | learn workflow |
| learning-review | learn workflow |
| qa-escalation-policy | safety gates / validation procedure |
| qa-fixer | validation procedure / implementation role |
| qa-validator | validation procedure / validation role |
| codebase-assessment | Discovery chain / architecture role |
| constraint-discovery | Discovery chain |
| knowledge-search | learn workflow / planning procedure |
| problem-framing | Discovery chain |
| researcher | planning procedure / architecture role |
| stack-recommendation | Discovery chain / architecture role |
| code-reviewer | review procedure / code-review role |
| deploy-checker | deployment-readiness role |
| security-reviewer | review procedure / security role |
| connect-wizard | setup/config integration mode |
| profile-generator | setup/config profile mode |
| shared-context-sync | shared-context integration / learn workflow |
| quick-spec | Quick Flow / specification procedure |
| spec-writer | specification procedure / specification role |
| design-skill-creator | external-design-skills governance |
| flutter-ui | implementation role + frontend overlay |
| react-native-ui | implementation role + frontend overlay |
| react-ui | implementation role + frontend overlay |
| swift-ui | implementation role + frontend overlay |
| vue-ui | implementation role + frontend overlay |
| clarifier | specification procedure / specification role |
| complexity-assessor | draw chain selection |
| constitution-writer | setup / Discovery chain |
| handoff-back | Jira integration / export workflow |
| handoff-packager | export workflow |
| preflight-check | draw/setup preamble + hook fallback |
| routing-rules | draw chain selection |
| specialist-selection | specialist-selection protocol |
| status-reporter | draw status procedure |
| story-preparer | export workflow |
| ticket-loader | Jira integration / specification procedure |
| visual-analyzer | draw design procedure |

The authored source linter verifies that every current Claude skill appears
exactly once in this table. Runtime sequencing is explicit in the chain and
procedure references; Codex does not execute source metadata relationships.
