/**
 * Christopher Vote
 */
import 'dotenv/config';
import express from 'express';
import asyncHandler from 'express-async-handler';
import * as exercises from './exercises_model.mjs';

const ERROR_INVALID_REQUEST = {
    Error: "Invalid request"
};

const ERROR_NOT_FOUND = {
    Error: "Not found"
};

const PORT = process.env.PORT;
const app = express();

app.use(express.json());

app.listen(PORT, async () => {
    await exercises.connect()
    console.log(`Server listening on port ${PORT}...`);
});


/**
 *
 * @param {string} date
 * Return true if the date format is MM-DD-YY where MM, DD and YY are 2 digit integers
 */
function isDateValid(date) {
    // Test using a regular expression. 
    const format = /^\d\d-\d\d-\d\d$/;
    return format.test(date);
}


/**
 * Helper function to validate that a body passed in is valid for the operations.
 * Checks that all required querry parameters of name, reps, weight, unit, and date
 * are present in a request.
 * @param {Object} body - a JSON object which is the body of a request.
 * @returns {boolean} true if the object is valid, otherwise false.
 */
function validateBody(body) {
    const keys = Object.keys(body || {});
    if (keys.length !== 5 ||
        !REQUIRED_KEYS.every(k => Object.prototype.hasOwnProperty.call(body, k)) ||
        keys.some(k => !REQUIRED_KEYS.includes(k))) {
        return false
    }

    if (typeof body.name !== 'string' || body.name.trim().length < 1) {
        return false;
    }
    if (!Number.isInteger(body.reps) || body.reps <= 0) {
        return false;
    }
    if (!Number.isInteger(body.weight) || body.weight <= 0) {
        return false;
    }
    if (body.unit !== 'kgs' && body.unit !== 'lbs') {
        return false;
    }
    if (typeof body.date !== 'string' || !isDateValid(body.date)) {
        return false;
    }
    return true;
}


/**
 * Creates a new exercise with the query parameters provided in the body.
 */
const REQUIRED_KEYS = ['name', 'reps', 'weight', 'unit', 'date'];

app.post('/exercises', asyncHandler(async (req, res) => {
    const body = req.body;

    if (!validateBody(body)) {
        return res.status(400).json(ERROR_INVALID_REQUEST)
    }

    try {
        const exercise = await exercises.createExercise(
            req.body.name,
            req.body.reps,
            req.body.weight,
            req.body.unit,
            req.body.date
        );
        res.status(201).json(exercise);
    } catch (err) {
        res.status(400).json(ERROR_INVALID_REQUEST)
    }
}));


/**
 * Retrieves all exercises in the database.
 */
app.get('/exercises', asyncHandler(async (req, res) => {
    const exerciseArray = await exercises.findExercises({});
    res.status(200).json(exerciseArray);
}));


/**
 * Retrieves the exercise matching a unique id.
 * 
 */
app.get('/exercises/:id', asyncHandler(async (req, res) => {
    const exercise = await exercises.retrieveID(req.params.id);
    if (exercise) {
        res.status(200).json(exercise);
    } else {
        res.status(404).json(ERROR_NOT_FOUND);
    }
}));


/**
 * Updates a data element for the exercise matching the unique id.  
 * If the exercise does not exist, an ERROR_NOT_FOUND message is raised.
 * If the request is invalid, an ERROR_INVALID_REQUEST message is raised.
 */
app.put('/exercises/:id', asyncHandler(async (req, res) => {
    const body = req.body;

    if (!validateBody(body)) {
        return res.status(400).json(ERROR_INVALID_REQUEST)
    }

    const updatedExercise = await exercises.updateExercise(req.params.id, req.body);
    if (updatedExercise) {
        res.status(200).json(updatedExercise);
    } else {
        res.status(404).json(ERROR_NOT_FOUND);
    }
}));


/**
 * Deletes the exercise matching a unique ID. If no exercise matches the ID,
 * an ERROR_NOT_FOUND message is raised.
 */
app.delete('/exercises/:id', asyncHandler(async (req, res) => {
    const deleteExercise = await exercises.deleteExercise(req.params.id);
    if (deleteExercise) {
        res.sendStatus(204);
    } else {
        res.status(404).json(ERROR_NOT_FOUND);
    }
}));