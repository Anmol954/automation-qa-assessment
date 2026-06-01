# Automation & QA Developer - Assessment Submission

## Deliverables

### Task 1: Web App QA & Debug Report
- **File**: `Task1_QA_Report.pdf`
- **App Tested**: Conduit (RealWorld Angular Demo) at https://demo.realworld.show
- **Issues Found**: 7 issues (2 Critical, 2 High, 3 Medium)
- **Root-Cause Analysis**: Focused on Bug #1 (silent 422 error on article update) - explains the Angular service layer gap and proposes a 3-layer fix

### Task 2: n8n API Integration Workflow
- **Workflow JSON**: `Task2_Workflow.json`
- **README**: `Task2_README.md`
- **APIs Used**: GitHub REST API (Search Repositories + Fetch README)
- **Features**: Schedule trigger, HTTP requests, data transformation, conditional branching (stars > 100), email + Slack output, error handling with Slack alerts
- **Error Handling**: Continue On Fail on HTTP nodes + dedicated Error Handler code node that routes failures to Slack

### Bonus: Uptime Monitor Workflow
- **Workflow JSON**: `Bonus_UptimeMonitor.json`
- **Features**: Pings https://demo.realworld.show every 5 minutes, checks HTTP status code, retry logic (2nd ping on failure), Slack alerts on downtime, response time tracking, daily uptime summary with statistics
- **Bonus Points**: Retry logic, response-time tracking, daily summary

## Screenshots
Screenshots of the testing process are available in the `/download` directory:
- `realworld_home.png` - Home page
- `realworld_logged_in.png` - Logged-in state
- `realworld_article_created.png` - Article detail page
- `realworld_profile.png` - User profile page
- `realworld_login_error.png` - Login error with poor UX

## How to Test the n8n Workflows
1. Install n8n (Docker or npx): `npx n8n`
2. Import `Task2_Workflow.json` via n8n's Import menu
3. Configure SMTP credentials in n8n's Credentials store
4. Replace Slack webhook URLs with your actual webhook
5. Execute the workflow manually to test
6. Import `Bonus_UptimeMonitor.json` separately for uptime monitoring

## Key Decisions
- **App choice**: Used demo.realworld.show since the original demo.realworld.io is down (404/NoSuchBucket) - this itself became Bug #6
- **GitHub API**: Chosen for the n8n workflow because it's free, well-documented, and requires no API key for public endpoints
- **Star threshold**: 100 stars was chosen as a meaningful threshold - repos with 100+ stars in a short period represent genuine community interest
- **Error handling strategy**: Two-pronged approach - Continue On Fail prevents workflow crashes, plus a dedicated Error Handler node that checks for failures and routes them to Slack
