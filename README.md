# Django Signals – What Actually Happens Under the Hood

## Why I Built This

I didn’t build this project to just “use” Django signals — I built it to **understand what really happens when they run**.

There’s a lot of vague explanations online like:
> “Signals run when something happens”

That’s not enough.

I wanted clear answers to 3 things:
- Are signals synchronous or async?
- Do they run in the same thread?
- Do they respect database transactions?

So instead of reading theory, I tested everything myself.

---

## What This Project Does

This project is a set of small experiments using Django signals.

Each endpoint answers one specific question by actually running code and observing behavior.

---

## Key Findings 

### 1. Signals are NOT async

I added a `time.sleep(5)` inside a signal.

When I hit the endpoint:
- The response took ~5 seconds

That means:
The request waits for the signal to finish

So:
**Signals are synchronous and blocking**

---

### 2. Signals run in the SAME thread

I printed thread IDs:
- One inside the view
- One inside the signal

Both were identical.

So:
 No new thread is created  
 No background execution  

Everything runs in the same flow.

---

### 3. Signals run inside the SAME transaction

I wrapped everything inside a transaction and forced a failure.

What happened:
- Signal executed
- But database changes were rolled back

So:
 Signal runs inside the transaction  
 But rollback still undoes DB changes  

---

## The Important Insight

Signals are NOT background jobs.

They are:
- Inline
- Blocking
- Tightly coupled to your request flow

If you misuse them, you will:
- Slow down APIs
- Create inconsistent behavior
- Trigger side effects at the wrong time

---

## Endpoints to Test

Run the server and open these:
http://127.0.0.1:8000/test-signal/

http://127.0.0.1:8000/test-thread/

http://127.0.0.1:8000/test-transaction/




What they do:

- `/test-signal/` → shows delay (proves sync behavior)
- `/test-thread/` → check terminal for thread IDs
- `/test-transaction/` → shows rollback behavior

---

## How to Run This Project

```bash
pip install django

python manage.py makemigrations
python manage.py migrate

python manage.py runserver


##Project structure

signals_project/
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── signals.py
│   └── apps.py
│
├── signals_project/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
└── db.sqlite3
