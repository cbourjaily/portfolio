import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const EditExercisePage = ({ exerciseToEdit }) => {
  const navigate = useNavigate();

  const e = exerciseToEdit || {};

  const [name, setName] = useState(e.name || "");
  const [reps, setReps] = useState(e.reps ?? "");
  const [weight, setWeight] = useState(e.weight ?? "");
  const [unit, setUnit] = useState(e.unit || "");
  const [date, setDate] = useState(e.date || "");

  const editExercise = async () => {
    const editedExercise = { name, reps, weight, unit, date };
    const response = await fetch(`/exercises/${e._id}`, {
      method: "PUT",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify(editedExercise),
    });
    if (response.status === 200) {
      alert("Successfully edited the exercise");
    } else {
      alert("Failed to edit the exercise, status code = " + response.status);
    }
    navigate("/");
  };

  return (
    <div>
      <h2>Edit Exercise</h2>
      <input
        type="text"
        placeholder="Name of exercise"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="number"
        min="1"
        placeholder="Enter reps: (integer > 0)"
        value={reps}
        onChange={(e) => setReps(e.target.valueAsNumber)}
      />
      <input
        type="number"
        min="1"
        placeholder="Enter weight: (integer > 0)"
        value={weight}
        onChange={(e) => setWeight(e.target.valueAsNumber)}
      />
      <select value={unit} onChange={(e) => setUnit(e.target.value)}>
        <option value="">-- select unit --</option>
        <option value="lbs">lbs</option>
        <option value="kgs">kgs</option>
      </select>
      <input
        type="text"
        placeholder="Date: (MM-DD-YY)"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />
      <button onClick={editExercise}>Update</button>
    </div>
  );
};

export default EditExercisePage;
