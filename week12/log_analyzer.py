from collections import defaultdict

def analyze_log(file_path):
    ip_failures = defaultdict(int)
    status_counts = defaultdict(int)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            ip = parts[0]
            status = parts[-1]

            # Count status codes
            status_counts[status] += 1

            # Count failures (status >= 400)
            if status.isdigit() and int(status) >= 400:
                ip_failures[ip] += 1

    print("=== Status counts ===")
    for s, c in status_counts.items():
        print(f"{s}: {c}")

    print("\n=== IPs with repeated failures ===")
    for ip, c in ip_failures.items():
        if c > 1:  # threshold
            print(f"{ip}: {c} failures")

if __name__ == "__main__":
    analyze_log("access.log")