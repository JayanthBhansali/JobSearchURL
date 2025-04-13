import json

def remove_duplicate_jobs(file_path="jobright_jobs.json"):
    try:
        with open(file_path, "r") as f:
            jobs = json.load(f)

        unique_jobs = []
        seen_urls = set()

        for job in jobs:
            if job["application_url"] not in seen_urls:
                unique_jobs.append(job)
                seen_urls.add(job["application_url"])

        with open(file_path, "w") as f:
            json.dump(unique_jobs, f, indent=2)

        print(f"✅ Removed duplicates. {len(jobs) - len(unique_jobs)} duplicates found.")
    except Exception as e:
        print(f"❌ Error processing file: {e}")

if __name__ == "__main__":
    remove_duplicate_jobs()