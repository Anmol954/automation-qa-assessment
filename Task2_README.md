# Task 2 - GitHub Trending Morning Brief (n8n Workflow)

## Overview

This n8n workflow watches the GitHub REST API for trending TypeScript repositories, enriches the top result by fetching its README, applies a conditional branch based on star count, and posts a digest to both email and Slack. It includes robust error handling to ensure no failure goes unnoticed.

## APIs Used

| API | Endpoint | Purpose |
|-----|----------|---------|
| **GitHub REST API** | `GET /search/repositories` | Fetch trending repos sorted by stars, filtered to TypeScript and recently created |
| **GitHub REST API** | `GET /repos/:owner/:repo/readme` | Enrich the #1 repo by fetching its README content (base64 decoded) |

**Why these APIs?** GitHub's REST API is free, well-documented, requires no API key for public endpoints (rate-limited to 60 requests/hour unauthenticated), and provides rich data about repositories including stars, descriptions, and README content. The search endpoint supports complex queries with date filtering and sorting, making it ideal for a "morning brief" use case.

## Workflow Steps

1. **Schedule Trigger** - Fires every 1 hour (adjustable to daily for production)
2. **GitHub Trending Repos** - HTTP request to search for recently created TypeScript repos sorted by stars
3. **Transform & Top 5** - Code node that reshapes the response: extracts name, description, stars, language, URL; sorts by stars descending; keeps only the top 5 results
4. **Fetch Top Repo README** - HTTP request to the #1 repo's README endpoint for enrichment
5. **Build Digest** - Code node that combines the top 5 list and README snippet into a formatted text digest
6. **IF Stars > 100** - Conditional branch: if the top repo has more than 100 stars, it's flagged as a high-alert item
7. **High Stars Message** / **Standard Message** - Branch-specific formatting (high-stars gets an urgent prefix)
8. **Send Email Digest** - Emails the digest to the team
9. **Slack Notification** - Also posts to a Slack channel via webhook (standard branch only, to avoid duplicate alerts)
10. **Error Handler** + **Error to Slack** - If any HTTP request fails, the error is captured and posted to Slack with a warning emoji

## Transformation Logic

The **Transform & Top 5** node performs the following:
- Extracts only relevant fields: `full_name`, `description`, `stargazers_count`, `language`, `html_url`, `owner.login`, `created_at`
- Sorts by `stargazers_count` in descending order
- Limits output to 5 items
- Adds metadata: `count` and `fetched_at` timestamp

The **Build Digest** node:
- Formats a human-readable text message with numbered repo list
- Appends the top repo's README snippet (first 500 characters, decoded from base64)
- Sets the `isHighStars` flag for the conditional branch

## Conditional Branch

The **IF Stars > 100** node routes based on the threshold:
- **True (high-stars)**: Adds an "HIGH STARS ALERT" prefix and recommendation to review immediately. Sends via email only (urgent channel).
- **False (standard)**: Adds a "Standard Digest" prefix. Sends via both email and Slack.

The threshold of 100 stars was chosen because it represents a repo that is gaining significant traction in a short time, warranting immediate team attention.

## Error Handling

- **Continue On Fail** is enabled on both HTTP Request nodes (GitHub Search and README Fetch)
- If the GitHub Search fails, the Transform node detects empty data and returns an error object
- If the README fetch fails, the digest still includes the repo list but shows "README not available"
- A dedicated **Error Handler** Code node checks for errors from the HTTP nodes
- Errors are forwarded to **Error to Slack** which posts a warning message to the same Slack channel
- The workflow never crashes silently - all failures are logged or routed to a fallback

## Credentials

All credentials should be stored in n8n's Credentials store:
- **SMTP account** - For sending email digests (configure with your SMTP provider)
- **Slack Webhook URL** - Replace `YOUR/SLACK/WEBHOOK` in the Slack Notification and Error to Slack nodes with your actual Slack webhook URL

**Do NOT hard-code secrets in the workflow JSON.** Reference credentials from n8n's built-in credential system.

## Testing

You can test this workflow by:
1. Manually executing it from the n8n canvas
2. Or hitting the Schedule Trigger with the "Execute Workflow" button
3. Verify that the digest email is received and the Slack notification appears

For quick API testing with curl:
```bash
curl "https://api.github.com/search/repositories?q=created:>2026-05-25+language:typescript&sort=stars&order=desc&per_page=10"
```
