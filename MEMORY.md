# MEMORY.md - Long-Term Memory

## Key Facts
- **My name:** Ori_
- **My human:** Steven (UK, GMT timezone)
- **Born:** 2026-02-03
- **Vibe:** Sharp & efficient — minimal words, maximum results

## Active Projects

5. **Zabbix Service Desk** (`localhost:8003` dev, `http://100.64.150.79:8003` live)
   - Location: `/home/openclaw_user/apps/zabbix-servicedesk`
   - Purpose: Mobile-first support ticketing for Zabbix alerts & client requests with LLM integration
   - Stack: FastAPI + SQLite (dev) / PostgreSQL (prod) + vanilla JS frontend (no CDN deps)
   - Features: 
     - ✅ **JWT Authentication** - Login page, token-based access, role-based (admin/operator/viewer)
     - ✅ Ticket creation/management with real-time dashboard
     - ✅ Archive system (resolved tickets >7 days → separate table)
     - ✅ Admin settings panel (configurable retention)
     - ✅ Metadata storage (JSONB) for LLM processing
     - ✅ Semantic search ready (pending pgvector)
     - ✅ Mobile-responsive UI (bottom nav, responsive grid)
     - ✅ Dashboard, filtering, notes, detail view
   - Status: ✅ **Running on 0.0.0.0:8003** with auth working (live accessible from phone)
   - Database: SQLite (dev: `servicedesk.db`), PostgreSQL ready for prod
   - Test Users: admin/admin123 (ADMIN), testuser/testuser123 (OPERATOR)
   - Documentation: ✅ ARCHITECTURE.md + DESIGN_LOG.md
   - Todo: Zabbix webhooks, pgvector embeddings, email notifications, RBAC enforcement
   - **GitHub:** https://github.com/oribot89/zabbix-servicedesk (private repo, 6 commits)

## Active Projects
1. **Inventory App** (`localhost:8000`)
   - Location: `/home/openclaw_user/apps/fastapi-app`
   - Stack: FastAPI + Vuetify + SQLite + Chart.js
   - Features: Multi-category inventory (Produce/Meat), 6-month stock trends, real-time system health dashboard
   - DB: `inventory.db` (inventory + stock_history tables, 180 days pre-seeded)
   - Service: `fastapi-app.service` (systemd auto-restart enabled)
   - Tested on iPhone 17 Pro Max mobile layout
   - WebSocket endpoints: `/ws/health` (system metrics), `/ws/openclaw-status` (OpenClaw status)
   - Car search: 6 UK sources (Autotrader, Motors, CarWow, eBay, Gumtree, Facebook)
   - **GitHub:** https://github.com/oribot89/inventory-app (private repo, venv excluded from tracking)

2. **example1-clone** (`localhost:8001`)
   - Location: `/home/openclaw_user/apps/example1-clone`
   - Target: https://www.example1.co.uk (IT Support Company, Edinburgh/Glasgow)
   - Stack: FastAPI + Vue.js
   - Status: Backend framework ready, frontend structure to build
   - Todo: Vue.js accordion/carousel components, contact form
   - **GitHub:** https://github.com/oribot89/example1-clone (private repo)

3. **InstanceOne** (`localhost:8002` dev, `https://www.instanceone.co` live)
   - Location: `/home/openclaw_user/apps/instanceone`
   - Purpose: AI-driven on-premises infrastructure automation for Proxmox + bare metal servers
   - Stack: FastAPI + Vue.js + SQLite/PostgreSQL
   - Features: Proxmox native integration, Zabbix monitoring, AI orchestration, bare metal optimization
   - Status: ✅ **LIVE** on CloudPanel (91.134.252.26)
   - Deployment: Static HTML landing page deployed via SFTP (2026-02-10 00:11 UTC)
   - Backup: WordPress archived at `/home/instanceone/htdocs/www.instanceone.co-wordpress-backup-20260210.tar.gz`
   - **Case Study Page:** 
     - Company: Enterprise Services Group (ESG), 200 employees, 15+ year legacy infrastructure
     - Narrative: 4-phase transformation (Discovery → Planning → Implementation → Migration → Optimization)
     - Focus: Process-driven outcome narrative; no metrics/percentages (Steven preference)
     - Files: `case-study.html` (756 lines), updated `index.html` with CTA button
     - **Status:** ✅ Deployed live to https://www.instanceone.co/case-study.html

4. **infra.instanceone.co** (Flask API, CloudPanel deployment)
   - Location: `/home/instanceone-infra/htdocs/infra.instanceone.co/` (server)
   - Local repo: `/tmp/instanceone-infra-repo`
   - GitHub: https://github.com/oribot89/instanceone-infra (private)
   - Stack: Flask 3.0.0 + Werkzeug 3.0.1 + uWSGI 2.0 + NGINX
   - Status: ⚠️ **GitHub Actions deployment working, but uWSGI not responding**
   - Deployment method: GitHub Actions (`appleboy/ssh-action`) with secrets
   - Secrets configured: DEPLOY_HOST, DEPLOY_USER, DEPLOY_KEY
   - Passwordless sudo: ✅ Configured for `instanceone-infra` user
   - **Issue:** uWSGI listening on 127.0.0.1:8090 but returning "Empty reply" / Flask not loading
   - **Blocked:** SSH to deployment server closing immediately (may be firewall/SSH daemon issue)

4. **ori-ai-artifacts** (Private)
   - Location: `/home/openclaw_user/ori-ai-artifacts`
   - Purpose: Long-term memory, scripts, templates, decision logs
   - **GitHub:** https://github.com/oribot89/ori-ai-artifacts (private repo)

## Key Decisions
- **Haiku model**: Cost optimization (~$0.14/day)
- **Lazy USER.md loading**: Only when needed, not every turn
- **URL generation over scraping**: Car search uses Autotrader/partner URLs to avoid Playwright dependency hell
- **WebSocket for real-time**: System health & OpenClaw status via async endpoints
- **Mobile-first UI**: Bottom tab nav (mobile), sidebar (desktop), iPhone safe areas supported
- **Separate ports**: 8000 (inventory), 8001 (example1-clone) for isolation

## Gmail Integration
- **Account**: `oribot@edinprint3d.co.uk`
- **OAuth Status**: ✅ Connected (refresh token stored in gog keyring)
- **Tools**: `gog` CLI for Gmail API access (labels, search, send, etc.)
- **Cron Job**: Every 5 minutes checks inbox and reports new emails via OpenClaw
- **Config**: Webhooks enabled in `hooks.token` for future Pub/Sub integration
- **Keyring**: Encrypted with `GOG_KEYRING_PASSWORD` (set in systemd service env)

## GitHub Setup
- **Account**: oribot89 (oribot@edinprint3d.co.uk)
- **SSH Key (GitHub)**: ED25519 at `~/.ssh/github_ori` (SHA256:qzVpyrq8APk1AHtpzfQQZ0VYeeikmyjcqxOOd48ZpVw)
- **SSH Key (OpenClaw)**: ED25519 at `~/.ssh/id_openclaw` (SHA256:PBTxTxYLzN6wwVaj7Gqvm83YmRbHW2hm/SCuwneaAZ0) - added to CloudPanel server
- **SSH Config**: Added to `~/.ssh/config` for github.com
- **Git User**: Ori_ (oribot@edinprint3d.co.uk)
- **Repos**: 4 private (inventory-app, example1-clone, instanceone, ori-ai-artifacts)
- **Known Issue**: Resolved venv/Playwright binary size (115.55 MB) exceeding GitHub's 100 MB limit via `git rm -r --cached venv/` and force push

## History
- 2026-02-03: First boot. Steven named me Ori_. Set up identity and user files.
- 2026-02-04: First session after initial setup. Created memory system.
- 2026-02-04: Built FastAPI inventory app with Vuetify frontend, SQLite DB, 6-month stock trends, system health monitoring, car search.
- 2026-02-04: Started example1-clone project (IT support company website clone on port 8001).
- 2026-02-06: Completed Gmail OAuth setup with gog. Created desktop OAuth app (no domain restrictions), obtained refresh token, stored in gog keyring. Added GOG_KEYRING_PASSWORD to fastapi-app systemd service. Set up cron job for periodic inbox checks.
- 2026-02-06: GitHub account created, SSH keys generated, all 3 repositories initialized and pushed (example1-clone, inventory-app, ori-ai-artifacts). Resolved large venv issue.
- 2026-02-09: All GitHub repos converted to private. Created InstanceOne project (on-prem infrastructure automation). Positioned for Proxmox/bare-metal with Zabbix monitoring.
- 2026-02-10: Updated OpenClaw config - set `tools.exec.security=full` to enable outbound network operations (SFTP, SSH).
- 2026-02-10: Generated OpenClaw SSH key (`~/.ssh/id_openclaw`), added to CloudPanel server for automated deployments via SFTP.
- 2026-02-10: Deployed InstanceOne live to https://www.instanceone.co via SFTP. Archived WordPress backup (45 MB), deployed static HTML landing page. Site is live and verified.
- **Latest:** Created comprehensive case study page for InstanceOne (Enterprise Services Group modernization narrative). Committed to GitHub. **Blocked on deployment:** Need SFTP password for `oribot@91.134.252.26` or CloudPanel web access to deploy case-study.html + updated index.html.
