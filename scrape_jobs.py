# scrape_jobright_with_apply_urls.py

import asyncio
import json
import nest_asyncio
from playwright.async_api import async_playwright
from remove_duplicate_jobs import remove_duplicate_jobs
nest_asyncio.apply()

async def scrape_jobright_ai(keywords=["data science intern", "machine learning"], max_jobs=20):
    jobs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Load cookies
        try:
            with open("jobright_cookies.json", "r") as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)
            print("🍪 Loaded session cookies from jobright_cookies.json")
        except Exception as e:
            print(f"⚠️ Could not load cookies: {e}")

        page = await context.new_page()

        for keyword in keywords:
            print(f"\n🔍 Searching for: {keyword}")
            search_url = f"https://www.jobright.ai/?q={keyword.replace(' ', '%20')}"
            await page.goto(search_url)
            await page.wait_for_timeout(6000)


            container = await page.query_selector("ul.ant-list-items")
            if not container:
                print("⚠️ Could not find job list container.")
                continue

            job_cards = await container.query_selector_all("div.index_job-card__AsPKC")
            print(f"📦 Found {len(job_cards)} job cards for '{keyword}'")

            for i, card in enumerate(job_cards[:max_jobs]):
                try:
                    title_el = await card.query_selector("h2.index_job-title__UjuEY")
                    company_el = await card.query_selector("div.index_company-name__gKiOY")
                    location_el = await card.query_selector("div.index_job-metadata-item__ThMv4 span")
                    apply_button = await card.query_selector("button.index_apply-button__kp79C")

     
                    title = await title_el.inner_text() if title_el else "N/A"
                    company = await company_el.inner_text() if company_el else "N/A"
                    location = await location_el.inner_text() if location_el else "N/A"
                    application_url = "N/A"

                    if apply_button:
                        try:
                            # Listen for a new tab opening
                            async with context.expect_page() as new_page_info:
                                await page.evaluate('(btn) => btn.click()', apply_button)

                            apply_page = await new_page_info.value
                            await apply_page.wait_for_load_state("domcontentloaded")
                            application_url = apply_page.url
                            await apply_page.close()
                        except asyncio.TimeoutError:
                            print(f"⚠️ Timeout while waiting for new page after clicking apply button.")
                        except Exception as e:
                            print(f"❌ Error handling apply button: {e}")

                    jobs.append({
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": location.strip(),
                        "application_url": application_url.strip(),
                        "keyword": keyword
                    })

                except Exception as e:
                    print(f"❌ Error scraping job card {i+1}: {e}")
                    continue

        await browser.close()
    return jobs

async def main():
    keywords = ["data science intern", "machine learning"]
    max_jobs = 25

    scraped = await scrape_jobright_ai(keywords, max_jobs)
    with open("jobright_jobs.json", "w") as f:
        json.dump(scraped, f, indent=2)

    print(f"\n✅ Scraped {len(scraped)} jobs and saved to jobright_jobs.json")
    remove_duplicate_jobs("jobright_jobs.json")
    print("✅ Removed duplicates from jobright_jobs.json")
    print("✅ Finished scraping and cleaning job data.")

if __name__ == "__main__":
    asyncio.run(main())
