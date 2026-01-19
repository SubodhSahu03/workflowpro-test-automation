# WorkflowPro Test Automation Framework

PART 1 — Debugging Flaky Playwright Test Code
1. Identify Flakiness Issues (Root-Cause Enumeration)

The given Playwright tests exhibit multiple sources of flakiness that can cause intermittent failures.

A. Missing Explicit Waits

No wait for navigation after clicking Login

Immediate assertion on page.url

Immediate access to dynamically loaded elements

B. Dynamic Content Loading

Dashboard elements (.welcome-message, .project-card) are loaded asynchronously

Test assumes synchronous availability of UI components

C. Hard URL Assertion
assert page.url == "https://app.workflowpro.com/dashboard"


URL change may not complete when assertion runs

Redirect chains or delayed navigation break this check

D. Lack of Browser Context Isolation

Tests reuse browser without isolated context

Cookies/session state may leak between tests

E. No Handling of Conditional Authentication (2FA)

Login flow includes optional 2FA

Test assumes a single deterministic login path

F. Multi-Tenant Timing Variability

Different tenants have:

Different data volumes

Different API response times

Causes inconsistent element availability

G. Headless Execution Sensitivity

CI runs tests in headless mode

Faster execution exposes race conditions not visible locally

2. Root Causes: CI/CD vs Local Environment
Factor	Local Execution	CI/CD Execution
CPU	High performance	Resource throttled
Network	Stable	Variable latency
Browser	Usually Chromium	Chromium / Firefox / WebKit
Rendering	Headed	Headless
Timing	Slower user pace	Very fast automation
Parallelism	Single run	Parallel jobs
Why This Causes Flakiness

CI machines execute instructions faster than UI can update

Async API calls complete later than assertions

Headless browsers expose synchronization bugs

Network jitter delays element rendering

3. Corrected & Reliable Test Implementation
Key Improvements Applied

✔ Explicit waits for navigation
✔ Element-level synchronization
✔ Context isolation
✔ Resilient assertions
✔ CI-safe browser handling

Corrected Login Test (Reliable Version):-
      import pytest
      from playwright.sync_api import sync_playwright

      def test_user_login():
          with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Navigate to login page
            page.goto("https://app.workflowpro.com/login", wait_until="networkidle")

            # Fill login form
            page.fill("#email", "admin@company1.com")
            page.fill("#password", "password123")
            page.click("#login-btn")

            # Wait for successful navigation
            page.wait_for_url("**/dashboard", timeout=15000)

            # Wait for dashboard to load completely
            page.wait_for_selector(".welcome-message", timeout=15000)

            # Assertion
            assert page.locator(".welcome-message").is_visible()

            context.close()
            browser.close()

Corrected Multi-Tenant Test (Reliable Version):-

        def test_multi_tenant_access():
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                page.goto("https://app.workflowpro.com/login", wait_until="networkidle")

                page.fill("#email", "user@company2.com")
                page.fill("#password", "password123")
                page.click("#login-btn")

                # Wait for dashboard
                page.wait_for_url("**/dashboard", timeout=15000)
                page.wait_for_selector(".project-card", timeout=20000)

                projects = page.locator(".project-card")
                count = projects.count()

                for i in range(count):
                    assert "Company2" in projects.nth(i).inner_text()

                context.close()
                browser.close()

4. Reliability Improvements Summary
Improvement	Benefit
wait_until="networkidle"	Ensures API calls complete
wait_for_url()	Prevents premature URL assertions
wait_for_selector()	Synchronizes with dynamic UI
Browser context isolation	Prevents test contamination
Headless execution	CI consistency
Timeout tuning	Handles slow tenant loading
5. Conclusion (Submission-Ready)

The original test failures were caused by timing assumptions, missing synchronization, and environment variability.
By introducing explicit waits, context isolation, and resilient assertions, the tests become deterministic, CI-stable, and production-ready.

This solution aligns with enterprise SaaS automation best practices and is suitable for CI/CD pipelines and cross-browser execution.