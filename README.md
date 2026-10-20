# MicroX — Django Software House & Hackathon Portal

A Django implementation inspired by the supplied MicroX SRS. **This is a functional starter, not a verified production-complete implementation of every SRS requirement.**

## Run locally (Python 3.11+)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Set SECRET_KEY and DEBUG=True using your shell environment
python manage.py makemigrations website hackathon
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The project uses SQLite locally if DATABASE_URL is empty. For production, set DATABASE_URL to your PostgreSQL URL and install `psycopg[binary]` or `psycopg2-binary`. Also set SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, secure HTTPS settings and a real SMTP provider. Run `python manage.py collectstatic --noinput` and `python manage.py check --deploy`. Set up persistent private media storage; local uploads are not suitable for ephemeral cloud servers.

## Content and setup

Open `/admin/`, add published Services and Projects (and set projects Featured for homepage), create an Event, Tracks, and its real dates/rules. No client testimonials or case studies are invented. Add judges to the `Judges` group and assign their submissions via JudgeAssignment.

## Important production gaps / acceptance checklist

- Email verification, verified-email-only registration, password reset confirmation routes, bulk announcement email and notification delivery are **not yet complete**.
- Production uploads need private object storage, malware scanning and authorization; current PDF validation checks extension, size and signature only.
- Team membership race conditions require a database with row locking (PostgreSQL), and deadline checks must also be enforced inside write transactions for strict boundary guarantees.
- Event rubric weights, conflict-of-interest checks, audit logs, full RBAC, moderation, CSV export permissions and certificate generation need further work.
- FAQ chatbot/LLM integration, consent-managed analytics, real legal documents, CAPTCHA, throttling, sitemap, structured SEO metadata, newsletter, and CMS rich text need implementation.
- No automated integration, load or security tests have been run. Perform them before production release.
- SRS assumes MERN, but this project deliberately uses Django templates and ORM per your request.
