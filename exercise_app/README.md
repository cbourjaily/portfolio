# Exercise Tracker — Node/Express + MongoDB + Vite/React

A minimal MERN-style app: Express REST API with MongoDB (Mongoose) and a Vite/React frontend.

exercise_tracker_app/
├─ exercises_controller.mjs # Express API (routing, validation)
├─ exercises_model.mjs # Mongoose connection + model functions
└─ exercises_react/ # Vite React SPA (Home, Create, Edit)


## 1) Backend (Express + Mongoose)

**Requires:** Node 18+, MongoDB running locally or in Atlas  
**Env vars:** `PORT` (use **3000**), `MONGODB_CONNECT_STRING`

Create `.env` in project root:
```env
PORT=3000
MONGODB_CONNECT_STRING=mongodb://localhost:27017

Install and run:

npm install express express-async-handler dotenv mongoose
node exercises_controller.mjs
# -> Server listening on port 3000...

Data Model (collection: exercises)
Field	Type	Rules
name	String	required, non-empty
reps	Number	required, integer > 0
weight	Number	required, integer > 0
unit	String	required, "kgs" or "lbs"
date	String	required, MM-DD-YY (e.g., 03-10-25)

Validation lives in exercises_controller.mjs (validateBody) and isDateValid() (/^\d\d-\d\d-\d\d$/).
REST API (Base: http://localhost:3000)

    POST /exercises → create (expects exactly 5 keys)

        201: created doc JSON

        400: {"Error":"Invalid request"}

    GET /exercises → list all

        200: JSON array (possibly empty)

    GET /exercises/:id → get by id

        200: doc JSON

        404: {"Error":"Not found"}

    PUT /exercises/:id → update by id (requires a full valid body)

        200: updated doc JSON

        400/404 on invalid/missing

    DELETE /exercises/:id → delete by id

        204: no body

        404: {"Error":"Not found"}

2) Frontend (Vite + React)

Folder: exercises_react/
Key bits you implemented:

    App.jsx sets up react-router-dom routes and page shell (<Navigation />, header/footer).

    HomePage.jsx fetches /exercises, shows table, and wires Edit/Delete.

    CreateExercisePage.jsx posts to /exercises (name, reps, weight, unit, date).

    EditExercisePage.jsx PUTs to /exercises/:id with full body.

    ExerciseTable.jsx + ExerciseRow.jsx render rows with edit (MdModeEdit) and delete (TiDelete) icons.

Install & run:

cd exercises_react
npm install
npm run dev
# -> Vite dev server (default http://localhost:5173)

Dev Proxy (recommended)

Frontend uses relative paths like /exercises. Configure Vite to proxy API to port 3000 during dev (in vite.config.js):

server: { proxy: { '/exercises': 'http://localhost:3000' } }

This keeps fetch('/exercises') working without CORS.
3) Workflow

    Start MongoDB (local or Atlas connection string in .env)

    Run backend at :3000:

node exercises_controller.mjs

Run frontend at :5173:

    cd exercises_react && npm run dev

    Visit http://localhost:5173

        Home lists exercises, supports Edit and Delete

        Create Exercise form posts to /exercises

        Edit Exercise form PUTs to /exercises/:id

Notes

    Uses ES modules (.mjs) and the Fetch API (no Axios).

    Controller strictly validates body shape (must be exactly 5 fields).

    Backend uses express-async-handler for clean async routes.

    Frontend pre-fills edit form via lifted state (exerciseToEdit).

© 2025 Christopher Vote