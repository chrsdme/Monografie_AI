"""Simulari didactice. NICIODATA nu executa plati, emailuri sau publicari video."""
import argparse
import hashlib
import json
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parent

def load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def ask_ollama(model, state, available):
    request = {
        "model": model["name"], "stream": False, "format": "json",
        "messages": [
            {"role": "system", "content": "Alege un singur instrument din lista. Returneaza JSON cu campul action. Nu inventa date."},
            {"role": "user", "content": json.dumps({"state": state, "tools": available}, ensure_ascii=False)}
        ]
    }
    req = Request(model["base_url"].rstrip("/") + "/api/chat",
                  data=json.dumps(request).encode("utf-8"),
                  headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=40) as response:
        data = json.load(response)
    return json.loads(data["message"]["content"])["action"]

class RefundSandbox:
    """Bucla de alegere a actiunilor si dispatcher cu controale impuse in cod."""
    def __init__(self, cfg, order, ledger=None):
        self.cfg = cfg
        self.order = order
        self.ledger = {} if ledger is None else ledger
        self.known = {}
        self.actions = []
        self.status = "RUNNING"
        self.request_id = order["request_id"]

    def mock_next(self):
        s = self.known
        if "order" not in s: return "lookup_order"
        if "eligible" not in s: return "verify_eligibility"
        if not s["eligible"]: return "escalate"
        if "duplicate" not in s: return "check_duplicate"
        if s["duplicate"]: return "escalate"
        if not self.order["evidence_present"]: return "request_evidence"
        if Decimal(self.order["amount"]) > Decimal(str(self.cfg["policy"]["auto_refund_max"])):
            return "escalate"
        if "prepared" not in s: return "prepare_refund"
        if "verified" not in s: return "verify_refund"
        if not s["verified"]: return "escalate"
        if "confirmation" not in s: return "send_confirmation"
        return "finish"

    def decide(self):
        model = self.cfg["model"]
        if model["provider"] == "mock": return self.mock_next()
        if model["provider"] == "ollama":
            return ask_ollama(model, self.known, self.cfg["policy"]["allowed_tools"])
        raise ValueError("Provider neacceptat")

    def dispatch(self, action):
        p = self.cfg["policy"]
        if action not in p["allowed_tools"]:
            self.actions.append("BLOCKED_TOOL")
            self.status = "ESCALATED"
            return
        self.actions.append(action)
        s = self.known
        if action == "lookup_order":
            s["order"] = dict(self.order)
        elif action == "verify_eligibility":
            s["eligible"] = bool(self.order["eligible"] and
                (self.order["verified_customer"] or not p["require_verified_customer"]))
        elif action == "check_duplicate":
            s["duplicate"] = bool(self.order["already_refunded"] or self.request_id in self.ledger)
        elif action == "request_evidence":
            self.status = "WAITING_CUSTOMER"
        elif action == "prepare_refund":
            try: amount = Decimal(str(self.order["amount"]))
            except (InvalidOperation, TypeError): amount = Decimal("0")
            allowed = (s.get("eligible") is True and s.get("duplicate") is False
                       and "order" in s and self.order["evidence_present"]
                       and amount > 0 and amount <= Decimal(str(p["auto_refund_max"]))
                       and self.order["currency"] == p["currency"]
                       and p["allow_production_refunds"] is False
                       and self.cfg["safety"]["backend"] == "sandbox")
            if not allowed:
                self.actions.append("GUARD_DENIED")
                self.status = "ESCALATED"
                return
            self.ledger.setdefault(self.request_id, {
                "order_id": self.order["order_id"], "amount": str(amount),
                "currency": self.order["currency"], "status": "PREPARED_SIMULATED"
            })
            s["prepared"] = self.ledger[self.request_id]
        elif action == "verify_refund":
            s["verified"] = self.ledger.get(self.request_id, {}).get("status") == "PREPARED_SIMULATED"
        elif action == "send_confirmation":
            if not s.get("verified"):
                self.actions.append("GUARD_DENIED")
                self.status = "ESCALATED"
                return
            s["confirmation"] = "SIMULATED_ONLY"
        elif action == "escalate":
            self.status = "ESCALATED"
        elif action == "finish":
            self.status = "DONE_SIMULATED" if s.get("verified") and s.get("confirmation") else "ESCALATED"

    def run(self):
        for _ in range(self.cfg["policy"]["max_steps"]):
            self.dispatch(self.decide())
            if self.status != "RUNNING": break
        if self.status == "RUNNING": self.status = "ESCALATED_MAX_STEPS"
        return {"status": self.status, "request_id": self.request_id,
                "actions": self.actions, "sandbox_refund": self.ledger.get(self.request_id)}

def source_videos(cfg):
    r = cfg["research"]
    if r["source_mode"] == "fixture":
        return load_json(ROOT / "fixtures/videos.json")
    if r["source_mode"] != "metadata_api":
        raise ValueError("Doar fixture sau metadata_api")
    key = os.getenv(r["youtube_api_key_env"])
    if not key: raise ValueError("Lipseste cheia YouTube API")
    videos = []
    for channel in r["channel_ids"]:
        q = urlencode({"part": "contentDetails", "id": channel, "key": key})
        with urlopen("https://www.googleapis.com/youtube/v3/channels?" + q, timeout=20) as f:
            items = json.load(f).get("items", [])
        if not items: continue
        playlist = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
        q = urlencode({"part": "snippet", "playlistId": playlist,
                       "maxResults": min(50, r["max_videos"]), "key": key})
        with urlopen("https://www.googleapis.com/youtube/v3/playlistItems?" + q, timeout=20) as f:
            entries = json.load(f).get("items", [])
        for entry in entries:
            sn = entry["snippet"]
            vid = sn["resourceId"]["videoId"]
            videos.append({"video_id": vid, "title": sn["title"],
                           "description": sn.get("description", ""),
                           "url": "https://www.youtube.com/watch?v=" + vid})
    return list({x["video_id"]: x for x in videos}.values())[:r["max_videos"]]

def editorial(cfg, output):
    if cfg["research"]["allowed_content"] != "metadata_only":
        raise ValueError("Demo-ul nu acceseaza transcrieri")
    if cfg["production"]["publisher"] != "disabled":
        raise ValueError("Publicarea este interzisa in demo")
    videos = source_videos(cfg)[:cfg["research"]["max_videos"]]
    if len(videos) < 2: raise ValueError("Prea putine surse")
    research = {"topic": "De ce un workflow AI nu este automat un agent?",
                "analysis_scope": "metadata_only", "trend_confirmed": False,
                "sources": [{"title": v["title"], "url": v["url"]} for v in videos]}
    drafts = [{"variant": name, "script": "Comparam regulile, workflow-ul si agentul prin exemple originale.",
               "storyboard": "Intro / exemplu / comparatie / concluzie"}
              for name in cfg["production"]["variant_names"]]
    result = {"research": research, "production": {
        "variants": drafts, "status": "WAITING_HUMAN_APPROVAL",
        "rendered_video": False, "publisher_enabled": False}}
    result["artifact_sha256"] = hashlib.sha256(
        json.dumps(result, sort_keys=True).encode("utf-8")).hexdigest()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"status": "WAITING_HUMAN_APPROVAL", "variants": len(drafts),
            "publisher_enabled": False, "output": str(output)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("scenario", choices=("refund", "youtube"))
    p.add_argument("--case", default="ok", choices=("ok", "above_limit", "missing_proof", "duplicate", "unverified"))
    p.add_argument("--out", default=str(ROOT / "output/editorial_preview.json"))
    args = p.parse_args()
    if args.scenario == "refund":
        result = RefundSandbox(load_yaml(ROOT / "config/refund.yaml"),
                               load_json(ROOT / "fixtures/orders.json")[args.case]).run()
    else:
        result = editorial(load_yaml(ROOT / "config/youtube.yaml"), args.out)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
