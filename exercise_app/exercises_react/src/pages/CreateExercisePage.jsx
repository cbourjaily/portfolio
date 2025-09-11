import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const CreateExercisePage = () => {
  const [name, setName] = useState("");
  const [reps, setReps] = useState("");
  const [weight, setWeight] = useState("");
  const [unit, setUnit] = useState("");
  const [date, setDate] = useState("");

  const navigate = useNavigate();

  const createExercise = async () => {
    const newExercise = { name, reps, weight, unit, date };
    const response = await fetch("/exercises", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newExercise),
    });
    if (response.status === 201) {
      alert("Successfully created the exercise");
    } else {
      alert("Failed to create exercise, status code = " + response.status);
    }
    navigate("/");
  };

  return (
    <div>
      <h2>Create exercise</h2>
      <input
        type="text"
        placeholder="Name of exercise"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="number"
        min="1"
        value={reps}
        placeholder="Enter reps: (integer > 0)"
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
      <button onClick={createExercise}>Add</button>
    </div>
  );
};

export default CreateExercisePage;
