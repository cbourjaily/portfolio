import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import HomePage from "./pages/HomePage";
import EditExercisePage from "./pages/EditExercisePage";
import CreateExercisePage from "./pages/CreateExercisePage";
import { useState } from "react";

function App() {
  const [exerciseToEdit, setExerciseToEdit] = useState({});

  return (
    <div className="app">
      <Router>
        <header>
          <h1>Iron Log</h1>
          <p>Log every lift and track your gains</p>
        </header>

        <Navigation />
        <Routes>
          <Route
            path="/"
            element={<HomePage setExerciseToEdit={setExerciseToEdit} />}
          ></Route>
          <Route
            path="/create-exercise"
            element={<CreateExercisePage />}
          ></Route>
          <Route
            path="/edit-exercise"
            element={<EditExercisePage exerciseToEdit={exerciseToEdit} />}
          ></Route>
        </Routes>
        <footer>&copy; 2025 Christopher Vote</footer>
      </Router>
    </div>
  );
}

export default App;
