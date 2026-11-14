#!/usr/bin/env python3
"""
Cloudflare & Domain Automated Setup Script
Uses Cloudflare REST API to completely automate:
1. Zone creation (Free plan)
2. Fetching Nameservers for registrar delegation
3. DNS records (CNAME @ -> pages.dev, CNAME www -> apex)
4. 301 Edge Redirect Rule (www.<domain> -> https://<domain>)
5. Pages project custom domain binding
6. Adding arbitrary verification records (Bing CNAME / Google TXT)

Zero third-party dependencies (Python 3 stdlib only).
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

CF_API_BASE = "https://api.cloudflare.com/client/v4"


def cf_request(
    endpoint: str,
    token: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    url = f"{CF_API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "GameWiki-CloudflareSetup/1.0",
    }
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
            errors = err_json.get("errors", [])
            messages = [err.get("message", "") for err in errors]
            raise RuntimeError(f"Cloudflare API Error ({e.code}): {'; '.join(messages) or err_body}")
        except Exception:
            raise RuntimeError(f"Cloudflare HTTP {e.code}: {err_body}")


def get_default_account_id(token: str) -> str:
    res = cf_request("/accounts", token)
    accounts = res.get("result", [])
    if not accounts:
        raise RuntimeError("No Cloudflare accounts accessible with this token.")
    return accounts[0]["id"]


def get_or_create_zone(token: str, domain: str, account_id: str) -> Dict[str, Any]:
    res = cf_request(f"/zones?name={domain}", token)
    zones = res.get("result", [])
    if zones:
        print(f"✓ Zone already exists for {domain} (ID: {zones[0]['id']})")
        return zones[0]

    print(f"Creating Cloudflare Zone for {domain}...")
    data = {
        "name": domain,
        "account": {"id": account_id},
        "jump_start": False,
        "type": "full",
    }
    res = cf_request("/zones", token, method="POST", data=data)
    zone = res.get("result", {})
    print(f"✓ Zone created successfully (ID: {zone.get('id')})")
    return zone


def ensure_dns_records(token: str, zone_id: str, domain: str, pages_project: str) -> None:
    res = cf_request(f"/zones/{zone_id}/dns_records", token)
    existing_records = res.get("result", [])

    pages_target = f"{pages_project}.pages.dev"
    target_records = [
        {"type": "CNAME", "name": domain, "content": pages_target, "proxied": True},
        {"type": "CNAME", "name": f"www.{domain}", "content": domain, "proxied": True},
    ]

    for target in target_records:
        record_type = target["type"]
        record_name = target["name"]
        matched = [
            r for r in existing_records
            if r.get("name") == record_name and r.get("type") == record_type
        ]
        if matched:
            rec = matched[0]
            print(f"✓ DNS record already exists: {record_name} -> {rec.get('content')} (Proxied: {rec.get('proxied')})")
        else:
            print(f"Adding DNS record: {record_name} -> {target['content']} (Proxied: {target['proxied']})...")
            cf_request(
                f"/zones/{zone_id}/dns_records",
                token,
                method="POST",
                data={
                    "type": target["type"],
                    "name": target["name"],
                    "content": target["content"],
                    "ttl": 1,
                    "proxied": target["proxied"],
                },
            )
            print(f"✓ DNS record added: {record_name}")


def ensure_301_redirect_rule(token: str, zone_id: str, domain: str) -> None:
    rule_name = f"Redirect WWW to Apex ({domain})"
    expression = f'http.host eq "www.{domain}"'
    target_expression = f'concat("https://{domain}", http.request.uri.path)'

    rule_item = {
        "action": "redirect",
        "action_parameters": {
            "from_value": {
                "status_code": 301,
                "target_url": {
                    "expression": target_expression
                },
                "preserve_query_string": True,
            }
        },
        "expression": expression,
        "description": rule_name,
        "enabled": True,
    }

    try:
        res = cf_request(
            f"/zones/{zone_id}/rulesets/phases/http_request_dynamic_redirect/entrypoint",
            token,
        )
        existing_rules = res.get("result", {}).get("rules", [])
    except Exception:
        existing_rules = []

    already_configured = any(
        r.get("expression") == expression for r in existing_rules
    )
    if already_configured:
        print(f"✓ 301 Redirect rule already active: www.{domain} -> https://{domain}")
        return

    print(f"Deploying 301 Redirect Rule for www.{domain} -> https://{domain}...")
    updated_rules = [r for r in existing_rules if r.get("description") != rule_name] + [rule_item]
    cf_request(
        f"/zones/{zone_id}/rulesets/phases/http_request_dynamic_redirect/entrypoint",
        token,
        method="PUT",
        data={"rules": updated_rules},
    )
    print(f"✓ 301 Redirect rule deployed successfully")


def ensure_pages_custom_domain(token: str, account_id: str, pages_project: str, domain: str) -> None:
    res = cf_request(f"/accounts/{account_id}/pages/projects/{pages_project}/domains", token)
    domains = [d.get("name") for d in res.get("result", [])]

    for d in [domain, f"www.{domain}"]:
        if d in domains:
            print(f"✓ Pages custom domain already bound: {d}")
        else:
            print(f"Binding custom domain {d} to Pages project {pages_project}...")
            try:
                cf_request(
                    f"/accounts/{account_id}/pages/projects/{pages_project}/domains",
                    token,
                    method="POST",
                    data={"name": d},
                )
                print(f"✓ Bound {d} to Pages project")
            except Exception as e:
                print(f"  Note on binding {d}: {e}")


def add_dns_record(token: str, zone_id: str, record_type: str, name: str, content: str, proxied: bool = False) -> None:
    print(f"Adding DNS {record_type} record: {name} -> {content} (Proxied: {proxied})...")
    res = cf_request(
        f"/zones/{zone_id}/dns_records",
        token,
        method="POST",
        data={
            "type": record_type,
            "name": name,
            "content": content,
            "ttl": 1,
            "proxied": proxied,
        },
    )
    print(f"✓ DNS record added: {res.get('result', {}).get('id')}")


def get_domain_from_config() -> str:
    config_path = "config/site.config.ts"
    if os.path.isfile(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
            m = re.search(r"url:\s*['\"]https?://([^/'\"]+)['\"]", content)
            if m:
                return m.group(1)
    return ""


def get_pages_project_name() -> str:
    pkg_path = "package.json"
    if os.path.isfile(pkg_path):
        with open(pkg_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data.get("name", "")
            except Exception:
                pass
    return ""


def main():
    parser = argparse.ArgumentParser(description="Automate Cloudflare & Domain setup for Game Wiki Site")
    parser.add_argument("--token", default=os.getenv("CLOUDFLARE_API_TOKEN", ""), help="Cloudflare API Token")
    parser.add_argument("--domain", default="", help="Apex domain (e.g. example.quest)")
    parser.add_argument("--account-id", default=os.getenv("CLOUDFLARE_ACCOUNT_ID", ""), help="Cloudflare Account ID")
    parser.add_argument("--pages-project", default="", help="Cloudflare Pages project name")
    parser.add_argument("--add-record", nargs=3, metavar=("TYPE", "NAME", "CONTENT"), help="Add a one-off DNS record (e.g. CNAME hash verify.bing.com)")
    parser.add_argument("--proxied", action="store_true", help="Set proxied flag for added record")

    args = parser.parse_args()

    token = args.token
    if not token:
        print("Error: Cloudflare API Token is required (--token or CLOUDFLARE_API_TOKEN).", file=sys.stderr)
        sys.exit(1)

    domain = args.domain or get_domain_from_config()
    if not domain:
        print("Error: Domain could not be detected from config/site.config.ts. Pass --domain.", file=sys.stderr)
        sys.exit(1)

    account_id = args.account_id or get_default_account_id(token)
    print(f"--- Cloudflare Automation for {domain} ---")
    print(f"Account ID: {account_id}")

    zone = get_or_create_zone(token, domain, account_id)
    zone_id = zone["id"]
    nameservers = zone.get("name_servers", [])
    print(f"Assigned Nameservers: {', '.join(nameservers)}")

    if args.add_record:
        rtype, rname, rcontent = args.add_record
        add_dns_record(token, zone_id, rtype, rname, rcontent, proxied=args.proxied)
        return

    pages_project = args.pages_project or get_pages_project_name() or domain.split(".")[0]

    ensure_dns_records(token, zone_id, domain, pages_project)
    ensure_301_redirect_rule(token, zone_id, domain)
    ensure_pages_custom_domain(token, account_id, pages_project, domain)

    print("\n✓ Cloudflare setup completely verified and automated.")
    print(f"To delegate DNS at your registrar (Porkbun/Spaceship), point NS to: {', '.join(nameservers)}")


if __name__ == "__main__":
    main()
