# Automation & QA Developer — Take-Home Assessment
**Candidate:** Anmol Madhav | **Email:** anmolmadhav2004@gmail.com

---

## Deliverables

### Task 1 — Web App QA & Debug Report
| Item | File |
|------|------|
| QA Report PDF | [`Task1_QA_Report_AnmolMadhav.pdf`](./Task1_QA_Report_AnmolMadhav.pdf) |
| App Tested | [Conduit (RealWorld Angular Demo)](https://demo.realworld.show) |
| Bugs Found | **7 issues** — 2 Critical · 2 High · 3 Medium |
| RCA Focus | Bug #1 — Silent 422 error on article update (Angular service layer gap) |

**Bugs summary:**
| # | Title | Severity |
|---|-------|----------|
| 1 | No error feedback on failed article update (422) | High |
| 2 | No password strength validation on sign-up | **Critical** |
| 3 | No email format validation on sign-up | High |
| 4 | Duplicate usernames allowed on registration | **Critical** |
| 5 | Login error message has poor UX styling | Medium |
| 6 | Original demo site returns 404 (NoSuchBucket) | High |
| 7 | Comment form does not submit via browser automation | Medium |

---

### Task 2 — n8n API Integration Workflow
| Item | File |
|------|------|
| Workflow JSON | [`Task2_Workflow_AnmolMadhav.json`](./Task2_Workflow_AnmolMadhav.json) |
| README | [`Task2_README.md`](./Task2_README.md) |

**Workflow: GitHub Trending Morning Brief**
- **Trigger:** Schedule (every 1 hour)
- **API 1:** GitHub REST API — search TypeScript repos created in last 7 days, sorted by stars
- **Transform:** Code node extracts fields, sorts descending, keeps top 5
- **API 2:** GitHub REST API — fetch README of #1 repo (base64 decoded)
- **Branch:** IF stars > 100 → High Stars Alert path; else → Standard Digest path
- **Output:** Email (SMTP) + Slack webhook
- **Error Handling:** `continueOnFail` on all HTTP nodes + dedicated Error Handler code node → routes failures to Slack with ⚠️

---

### Bonus — Uptime Monitor Workflow
| Item | File |
|------|------|
| Workflow JSON | [`Bonus_UptimeMonitor_AnmolMadhav.json`](./Bonus_UptimeMonitor_AnmolMadhav.json) |

**Features:**
- Pings `https://demo.realworld.show` every 5 minutes
- Checks HTTP status code (200 = UP)
- **Retry logic** — 2nd ping on failure before alerting
- **Response-time tracking** — recorded per check
- **Slack alert** on confirmed downtime with both attempt results
- **Daily summary** — uptime %, avg/min/max response time, downtime events posted to Slack

---

### Screenshots
| Screenshot | Description |
|------------|-------------|
| [`realworld_home.png`](./realworld_home.png) | Conduit home page |
| [`realworld_logged_in.png`](./realworld_logged_in.png) | Logged-in state |
| [`realworld_article_created.png`](./realworld_article_created.png) | Article detail page |
| [`realworld_profile.png`](./realworld_profile.png) | User profile |
| [`realworld_login_error.png`](./realworld_login_error.png) | Login error (Bug #5) |
| [`realworld_failed_update_no_error.png`](./realworld_failed_update_no_error.png) | Silent 422 (Bug #1) |

---

## How to Run the n8n Workflows

### Prerequisites
- n8n (Docker): `docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n`
- Or n8n Cloud free trial

### Import Steps
1. Open n8n at `http://localhost:5678`
2. Go to **Workflows → Import from File**
3. Import `Task2_Workflow_AnmolMadhav.json`
4. Configure **SMTP credentials** in n8n's Credential store
5. Replace `YOUR/SLACK/WEBHOOK` in Slack nodes with your actual Slack Incoming Webhook URL
6. Click **Execute Workflow** to test manually
7. Repeat steps 2–6 for `Bonus_UptimeMonitor_AnmolMadhav.json`

### Quick API Test (no n8n needed)
```bash
curl "https://api.github.com/search/repositories?q=created:>2026-05-25+language:typescript&sort=stars&order=desc&per_page=10"
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **GitHub API** | Free, no API key required for public endpoints, rich repo data |
| **Stars > 100 threshold** | Represents genuine early traction for a recently created repo |
| **Two-pronged error handling** | `continueOnFail` prevents crash; Error Handler node ensures all failures reach Slack |
| **demo.realworld.show** | Used because `demo.realworld.io` is down (404/NoSuchBucket) — this itself became Bug #6 |
| **Retry before alert** | Single failed ping could be a transient network blip; 2nd confirmation avoids false alarms |
