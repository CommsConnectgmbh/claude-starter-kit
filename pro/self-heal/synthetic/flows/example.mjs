// Example flow — copy this per critical path of your app.
//
// A flow opens a page and clicks through one real user journey. The harness (run.mjs)
// watches for console errors, page errors, failed requests and HTTP 5xx the whole time,
// so you mostly just need to *drive* the UI here.
//
// Keep flows on the happy path: load → do the one thing this screen is for → assert it
// landed. Login/seed failures should `throw` (they surface as `step-failed`).

export default {
  name: "example-home",
  url: "https://example.com",

  async run(page) {
    // Wait for the thing that proves the page actually rendered.
    await page.waitForSelector("h1", { timeout: 10000 });

    // Drive a real journey. Prefer role/text selectors over brittle CSS.
    // await page.getByRole("link", { name: "Pricing" }).click();
    // await page.waitForURL("**/pricing");
    // await page.getByRole("button", { name: "Start free" }).click();

    // Optional explicit assertion — throwing here shows up as step-failed.
    // if (!(await page.getByText("Welcome").isVisible())) throw new Error("home CTA missing");
  },
};

// --- Logged-in flows ---------------------------------------------------------
// For journeys behind auth, prefer a dedicated review/test account whose
// credentials come from the environment — never hardcode secrets in a flow:
//
//   const email = process.env.REVIEW_EMAIL, code = process.env.REVIEW_CODE;
//   await page.goto("https://app.example.com/login");
//   await page.getByLabel("Email").fill(email);
//   await page.getByLabel("Code").fill(code);
//   await page.getByRole("button", { name: "Sign in" }).click();
//   await page.waitForURL("**/dashboard");
