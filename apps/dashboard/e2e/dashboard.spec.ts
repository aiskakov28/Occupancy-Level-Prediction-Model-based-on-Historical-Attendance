import { test, expect } from "@playwright/test";

test("dashboard loads", async ({ page }) => {
  await page.goto("http://localhost:3000/");
  await expect(page.getByText(/Occupancy Dashboard/i)).toBeVisible();
  await expect(page.getByTestId("forecast-chart")).toBeVisible();
});
