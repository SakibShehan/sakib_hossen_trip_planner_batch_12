# Smart Group Trip Planner API

A REST API for managing group trips, their travelers and expenses, and the trip lifecycle. It is built with Python, Flask and SQLite.

The focus of the project is correctness: every business rule is enforced on the server, and invalid operations are rejected with a clear JSON error and the right HTTP status code.



##  Project overview

### Problem statement

A travel organization needs a backend service for group trips. A trip has a destination, a date range, a budget, a capacity, travelers, expenses and a lifecycle status. The service must stop invalid operations such as:

- overbooking a trip,
- adding the same traveler to a trip twice,
- putting one traveler on two trips with overlapping dates,
- spending more than the trip budget,
- moving a trip through an invalid status change.

### What the API does

- Create, list, read, update and delete trips.
- Add and remove travelers on a trip. A traveler is identified by email.
- Record expenses against a trip and keep the total within the budget.
- Move a trip through its lifecycle: `PLANNED` → `ONGOING` → `COMPLETED`, or to `CANCELLED`.
- Return a calculated summary of seats and money for each trip.

All data is stored in SQLite, so it survives a restart. All responses are JSON.

---

##  Prerequisites

- **Python 3.11 or newer**, with the `venv` module. On Debian or Ubuntu, install it with `sudo apt install python3-venv` if it is missing.
- **pip** (comes with Python).
- **bash**, to use `./run.sh` (Linux, macOS, or Git Bash / WSL on Windows). Without bash, use the [manual run](#4-manual-run).
- Internet access on the first run, to download the packages in `requirements.txt`.

No database server and no manual SQL are needed. SQLite is part of Python.

---

## Run from a fresh clone

```bash
git clone https://github.com/SakibShehan/sakib_hossen_trip_planner_batch_12
cd sakib_hossen_trip_planner_batch_12
./run.sh
```

The script does everything needed, in this order:

1. Creates a local virtual environment in `.venv` (or reuses it if it already exists).
2. Installs the packages from `requirements.txt`.
3. Starts the Flask API on **http://127.0.0.1:5000**. On startup the app creates the SQLite database and its tables automatically.

If the script is not executable on your system, run `chmod +x run.sh` first, or start it with `bash run.sh`.

Check that the API is running, from another terminal:

```bash
curl http://127.0.0.1:5000/health
```

Expected response:

```json
{"status": "ok"}
```

Stop the server with `Ctrl + C`. Starting it again keeps all data.

---



##  API endpoints

Base path: `/api/v1`. Request and response bodies are JSON. Dates use the format `YYYY-MM-DD`. Statuses are uppercase.

| Method | Endpoint | Purpose | Success | Error codes |
|---|---|---|---|---|
| GET | `/health` | Application health | 200 | none |
| POST | `/api/v1/trips` | Create a trip | 201 | 400 |
| GET | `/api/v1/trips` | List trips (ordered by id) | 200 | none |
| GET | `/api/v1/trips/<trip_id>` | Get one trip | 200 | 404 |
| PUT | `/api/v1/trips/<trip_id>` | Update a trip | 200 | 400, 404, 409 |
| DELETE | `/api/v1/trips/<trip_id>` | Delete a trip | 200 | 404 |
| POST | `/api/v1/trips/<trip_id>/travelers` | Add a traveler | 201 | 400, 404, 409 |
| DELETE | `/api/v1/trips/<trip_id>/travelers/<traveler_id>` | Remove a traveler | 200 | 404, 409 |
| POST | `/api/v1/trips/<trip_id>/expenses` | Add an expense | 201 | 400, 404, 409 |
| PATCH | `/api/v1/trips/<trip_id>/status` | Change trip status | 200 | 400, 404, 409 |
| GET | `/api/v1/trips/<trip_id>/summary` | Calculated trip summary | 200 | 404 |
| GET | `/api/v1/trips/<trip_id>/travelers` | List travelers of a trip (extra) | 200 | 404 |

The last endpoint is an addition to the required contract. It is read-only and does not change any rule.

### Request bodies

| Endpoint | Fields |
|---|---|
| Create / update trip | `destination` (text), `start_date`, `end_date`, `budget` (number), `max_travelers` (whole number) |
| Add traveler | `name` (text), `email` (text) |
| Add expense | `title` (text), `amount` (number) |
| Change status | `status` (`PLANNED`, `ONGOING`, `COMPLETED` or `CANCELLED`) |

All fields are required. Extra fields are ignored. `id` and `status` of a trip cannot be set on create or update.

### Response format

Successful responses return the resource as a JSON object (or an array for lists). Delete operations return a short message.

Every error uses the same shape:

```json
{
  "error": "TRIP_FULL",
  "message": "The trip has reached its maximum traveler capacity."
}
```

### Status codes

| Code | Meaning in this API |
|---|---|
| 200 | Successful read, update or delete |
| 201 | Resource created |
| 400 | Invalid request data (validation failed, malformed JSON) |
| 404 | Unknown trip, traveler or URL |
| 405 | Method not allowed for the URL |
| 409 | Business conflict (the request is valid, but a rule forbids it) |
| 500 | Unexpected server error (returned as JSON, never as an HTML page) |

A failed operation never returns a 2xx status.

### Error codes

| Error code | Status | When it happens |
|---|---|---|
| `VALIDATION_ERROR` | 400 | Missing, wrong-typed or out-of-range input |
| `NOT_FOUND` | 404 | The trip, traveler or URL does not exist |
| `METHOD_NOT_ALLOWED` | 405 | Wrong HTTP method for the URL |
| `TRIP_NOT_EDITABLE` | 409 | Editing a `COMPLETED` or `CANCELLED` trip |
| `CAPACITY_BELOW_TRAVELER_COUNT` | 409 | `max_travelers` set lower than the current traveler count |
| `BUDGET_BELOW_EXPENSES` | 409 | Budget set lower than the expenses already recorded |
| `TRIP_NOT_OPEN_FOR_TRAVELERS` | 409 | Adding or removing a traveler when the trip is not `PLANNED` |
| `DUPLICATE_TRAVELER` | 409 | The email is already on this trip |
| `TRIP_FULL` | 409 | The trip has no free seat |
| `TRAVELER_TRIP_OVERLAP` | 409 | The traveler has another active trip with overlapping dates |
| `TRIP_NOT_OPEN_FOR_EXPENSES` | 409 | Adding an expense when the trip is not `PLANNED` or `ONGOING` |
| `BUDGET_EXCEEDED` | 409 | The expense is larger than the remaining budget |
| `INVALID_STATUS_TRANSITION` | 409 | The status change is not allowed by the lifecycle |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected error |

---

## Example requests and responses

The examples use `curl` against a running server. They are shown in the order of a normal trip.

### Create a trip

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips \
  -H "Content-Type: application/json" \
  -d '{
        "destination": "Cox's Bazar",
        "start_date": "2026-10-20",
        "end_date": "2026-10-23",
        "budget": 30000,
        "max_travelers": 5
      }'
```

Response `201 Created`:

```json
{
  "id": 1,
  "destination": "Cox's Bazar",
  "start_date": "2026-10-20",
  "end_date": "2026-10-23",
  "budget": 30000.0,
  "max_travelers": 5,
  "status": "PLANNED"
}
```

### Add a traveler

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/travelers \
  -H "Content-Type: application/json" \
  -d '{"name": "Sakib Hossen", "email": "sakib@example.com"}'
```

Response `201 Created`:

```json
{
  "id": 1,
  "name": "Sakib Hossen",
  "email": "sakib@example.com",
  "trip_id": 1
}
```

Sending the same email again returns `409 Conflict`:

```json
{
  "error": "DUPLICATE_TRAVELER",
  "message": "This traveler has already joined this trip."
}
```

### Add an expense

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Hotel", "amount": 12000}'
```

Response `201 Created`:

```json
{
  "id": 1,
  "trip_id": 1,
  "title": "Hotel",
  "amount": 12000.0
}
```

An expense larger than the remaining budget (`{"title": "Tour", "amount": 20000}`) returns `409 Conflict`:

```json
{
  "error": "BUDGET_EXCEEDED",
  "message": "This expense exceeds the remaining budget of 18000.00."
}
```

### Get the trip summary

```bash
curl http://127.0.0.1:5000/api/v1/trips/1/summary
```

Response `200 OK`:

```json
{
  "trip_id": 1,
  "destination": "Cox's Bazar",
  "status": "PLANNED",
  "budget": 30000.0,
  "max_travelers": 5,
  "traveler_count": 1,
  "available_seats": 4,
  "total_expense": 12000.0,
  "remaining_budget": 18000.0
}
```

### Change the trip status

```bash
curl -X PATCH http://127.0.0.1:5000/api/v1/trips/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "ONGOING"}'
```

Response `200 OK` returns the trip with `"status": "ONGOING"`. Trying to go back to `PLANNED` returns `409 Conflict`:

```json
{
  "error": "INVALID_STATUS_TRANSITION",
  "message": "A trip cannot change from ONGOING to PLANNED."
}
```

### Update, remove and delete

```bash
# update a trip (all five fields are required)
curl -X PUT http://127.0.0.1:5000/api/v1/trips/1 \
  -H "Content-Type: application/json" \
  -d '{"destination": "Cox'"'"'s Bazar", "start_date": "2026-10-20", "end_date": "2026-10-24", "budget": 35000, "max_travelers": 6}'

# remove a traveler from a PLANNED trip
curl -X DELETE http://127.0.0.1:5000/api/v1/trips/1/travelers/1
# {"message": "Traveler removed from the trip successfully."}

# delete a trip
curl -X DELETE http://127.0.0.1:5000/api/v1/trips/1
# {"message": "Trip deleted successfully."}
```

### Validation and not-found errors

A start date that is not before the end date returns `400 Bad Request`:

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Start date must be before end date."
}
```

An unknown trip returns `404 Not Found`:

```json
{
  "error": "NOT_FOUND",
  "message": "Trip not found."
}
```

---

## Business rules and assumptions

### Business rules

| Rule | Requirement | Where it is enforced |
|---|---|---|
| BR-01 | A trip's `end_date` must be later than its `start_date`. | `trip_validator.py` |
| BR-02 | `budget` must be greater than zero. | `trip_validator.py`, `money_validator.py` |
| BR-03 | `max_travelers` must be greater than zero. | `trip_validator.py` |
| BR-04 | The same traveler cannot join the same trip twice. Email is the identity. | `traveler_service.py` |
| BR-05 | A trip never holds more travelers than `max_travelers`. | `traveler_service.py` |
| BR-06 | A traveler cannot be on two trips with overlapping dates. Back-to-back trips on different days are allowed. | `overlap_service.py` |
| BR-07 | An expense amount must be greater than zero. | `expense_validator.py` |
| BR-08 | Total expenses never exceed the budget. Spending exactly the remaining budget is valid. | `expense_service.py`, `trip_service.py` |
| BR-09 | `max_travelers` cannot be reduced below the current traveler count. | `trip_service.py` |
| BR-10 | Travelers can be added only while the trip is `PLANNED`. | `traveler_service.py` |
| BR-11 | Expenses can be added only while the trip is `PLANNED` or `ONGOING`. | `expense_service.py` |
| BR-12 | A `COMPLETED` trip cannot be edited, accept travelers or expenses, or change status. | all services |
| BR-13 | A `CANCELLED` trip cannot be edited, accept travelers or expenses, or change status. | all services |
| BR-14 | Only the defined lifecycle transitions are allowed. | `trip_service.py` |

### Trip lifecycle

```
PLANNED ──> ONGOING ──> COMPLETED
   │           │
   └──> CANCELLED <──┘
```

Allowed: `PLANNED → ONGOING`, `ONGOING → COMPLETED`, `PLANNED → CANCELLED`, `ONGOING → CANCELLED`. Everything else returns `409`, including staying in the same status and any change out of `COMPLETED` or `CANCELLED`.

### Assumptions

The assignment leaves some details open. These are the decisions made, so the behavior is predictable.

**Travelers**
- A traveler is a person identified by **email**. The email is trimmed and stored in lowercase, so `Ayesha@Example.com` and `ayesha@example.com` are the same person.
- A person is stored once and can join many trips. If an email already exists, the name stored the first time is kept.
- Removing a traveler from a trip removes only the link to that trip. The person remains in the database.
- A traveler can be removed only while the trip is `PLANNED`. This is not stated in the assignment, so it was chosen to match the rule for adding.

**Dates and overlap**
- Overlap uses an **inclusive** comparison. A trip ending on the 23rd and another starting on the 23rd overlap. Back-to-back means the second trip starts on a later day.
- `CANCELLED` trips are ignored when checking for overlap.
- Changing a trip's dates with PUT is checked against the other trips of every traveler on that trip.

**Updating and deleting**
- PUT replaces all five trip fields, so all five are required. A `status` field in the body is ignored. Status changes go through `PATCH .../status` only.
- A trip can be edited while it is `PLANNED` or `ONGOING`. The assignment only forbids editing `COMPLETED` and `CANCELLED` trips.
- A trip can be deleted in any status. Deleting a trip also deletes its expenses and its traveler links.

**Money and limits**
- Money values have at most 2 decimal places. Budget and expense are compared in whole cents, so values such as `0.1 + 0.2` and a budget of `0.30` behave exactly.
- Upper limits keep numbers inside what SQLite can store: budget and expense amount up to 1,000,000,000, and `max_travelers` up to 10,000. Text fields are limited to 100 characters (email 254).

**Requests and errors**
- Checks run in a fixed order: unknown resource (404), then state conflicts (409), then input validation (400). The status endpoint validates the body first, because the transition check needs the new status.
- The `Content-Type: application/json` header is not required. A missing or broken body returns a JSON `400`.
- An ID larger than SQLite can store cannot exist, so it returns `404`.
- Responses may contain extra fields beyond the required ones (for example `trip_id` in the summary).

---

## Project structure

```
sakib_hossen_trip_planner_batch_12/
├── run.sh                  
├── run.py                    
├── requirements.txt         
├── README.md
├── test.py                   
├── .gitignore
├── .gitattributes
├── app/
│   ├── __init__.py           
│   ├── models/               
│   │   ├── trip.py
│   │   ├── traveler.py
│   │   ├── trip_traveler.py  
│   │   └── expense.py
│   ├── routes/              
│   │   ├── health.py
│   │   ├── trips.py          
│   │   ├── travelers.py
│   │   ├── expenses.py
│   │   └── summary.py
│   ├── services/             
│   │   ├── trip_service.py
│   │   ├── traveler_service.py
│   │   ├── expense_service.py
│   │   ├── summary_service.py
│   │   └── overlap_service.py
│   └── validators/           
│       ├── errors.py         
│       ├── trip_validator.py
│       ├── traveler_validator.py
│       ├── expense_validator.py
│       ├── status_validator.py
│       └── money_validator.py
└── instance/
    └── trip_planner.db       # created automatically, not committed
```

### How a request flows

```
route  →  service  →  validator  →  model
```

1. The **route** reads the request and returns the status code.
2. The **service** applies the business rules and talks to the database.
3. The **validator** checks the shape and values of the input.
4. The **model** defines the table.

Errors raised in a service or validator travel up to the handlers in `validators/errors.py`, which turn them into the JSON error shape. To find where a rule lives, start in the service named after the resource.

---

## How SQLite is initialized and stored

- The database is a single file: **`instance/trip_planner.db`**.
- Nothing has to be created by hand. When the app starts, `create_app()` calls `db.create_all()`, which creates the `instance/` folder, the database file and any missing tables.
- The file is listed in `.gitignore` and is **not committed**. Every fresh clone starts with an empty database and creates its own.
- Data is saved on every request, so it is still there after a restart.

### Tables

| Table | Columns | Notes |
|---|---|---|
| `trips` | `id`, `destination`, `start_date`, `end_date`, `budget`, `max_travelers`, `status` | One row per trip |
| `travelers` | `id`, `name`, `email` | `email` is unique: one row per person |
| `trip_travelers` | `trip_id`, `traveler_id` | Link table. The pair is the primary key, so a traveler cannot be linked to the same trip twice |
| `expenses` | `id`, `trip_id`, `title`, `amount` | Each expense belongs to one trip |

```
trips (1) ──< trip_travelers >── (1) travelers      many-to-many
trips (1) ──< expenses                               one-to-many
```

### Starting again from an empty database

Stop the server, delete the file and start the app:

```bash
rm instance/trip_planner.db
./run.sh
```

`create_all()` only creates tables that are missing. It does not change existing ones, so after a change to a model the database file must be deleted and rebuilt. This project does not use migrations.

---

## Running the tests

The 5 unit tests cover some important service functions: creating a trip, duplicate travelers and capacity, overlapping trips, the expense budget limit and the status lifecycle.

```bash
source .venv/bin/activate # after ./run.sh has created the environment
python test.py
```

The first line of the output shows `PASSED` or `FAILED`, followed by one line per test. The tests use a temporary in-memory database, so they never change `instance/trip_planner.db`.

---

## Known limitations


- **Concurrency:** capacity, budget and overlap checks read first and then write, so two requests arriving at the same instant could both pass; SQLite also does not enforce foreign keys unless `PRAGMA foreign_keys=ON` is set.
- **Database:** tables are created with `create_all()` and there are no migrations, so changing a model means deleting `instance/trip_planner.db`; money is stored as floats limited to 2 decimals.
- **Scope:** it runs on Flask's development server with no authentication, no paging on `GET /api/v1/trips`, and `./run.sh` needs bash (use the manual run steps on plain Windows).
---

**Author:** Sakib Hossen Shehan— Internship Batch 12