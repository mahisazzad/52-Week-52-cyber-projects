import requests
from urllib.parse import urlparse, urlencode, urljoin
from bs4 import BeautifulSoup
import argparse
import json

# Common payloads
SQLI_PAYLOAD = "' OR '1'='1"
XSS_PAYLOAD = "<script>alert(1)</script>"
REDIRECT_PAYLOAD = "http://evil.com"
TRAVERSAL_PAYLOAD = "../../etc/passwd"

# Security headers to check
SECURITY_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]

def check_sql_injection(url):
    parsed = urlparse(url)
    if parsed.query:
        params = dict([p.split("=") for p in parsed.query.split("&")])
        for key in params:
            params[key] = SQLI_PAYLOAD
        test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(params)}"
        res = requests.get(test_url)
        if "sql" in res.text.lower() or "syntax" in res.text.lower():
            return True
    return False

def check_xss(url):
    parsed = urlparse(url)
    if parsed.query:
        params = dict([p.split("=") for p in parsed.query.split("&")])
        for key in params:
            params[key] = XSS_PAYLOAD
        test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(params)}"
        res = requests.get(test_url)
        if XSS_PAYLOAD in res.text:
            return True
    return False

def check_open_redirect(url):
    parsed = urlparse(url)
    if parsed.query:
        params = dict([p.split("=") for p in parsed.query.split("&")])
        for key in params:
            params[key] = REDIRECT_PAYLOAD
        test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(params)}"
        res = requests.get(test_url, allow_redirects=False)
        if res.status_code in [301, 302] and REDIRECT_PAYLOAD in res.headers.get("Location", ""):
            return True
    return False

def check_directory_traversal(url):
    test_url = urljoin(url, TRAVERSAL_PAYLOAD)
    res = requests.get(test_url)
    if "root:" in res.text or "passwd" in res.text:
        return True
    return False

def check_security_headers(url):
    res = requests.get(url)
    missing = []
    for header in SECURITY_HEADERS:
        if header not in res.headers:
            missing.append(header)
    return missing

def scan(url):
    print(f"\nScanning {url}...\n")
    results = {
        "SQL Injection": check_sql_injection(url),
        "XSS": check_xss(url),
        "Open Redirect": check_open_redirect(url),
        "Directory Traversal": check_directory_traversal(url),
        "Missing Security Headers": check_security_headers(url)
    }
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Web Vulnerability Scanner")
    parser.add_argument("--url", required=True, help="Target URL to scan")
    args = parser.parse_args()
    scan(args.url)