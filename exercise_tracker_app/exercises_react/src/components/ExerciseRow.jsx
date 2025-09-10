import { MdModeEdit } from "react-icons/md";
import { TiDelete } from "react-icons/ti";

function ExerciseRow({ exercise, onEdit, onDelete }) {
  return (
    <tr>
      <td>{exercise.name}</td>
      <td>{exercise.reps}</td>
      <td>{exercise.weight}</td>
      <td>{exercise.unit}</td>
      <td>{exercise.date}</td>
      <td>
        <MdModeEdit
          onClick={() => onEdit(exercise)}
          style={{ cursor: "pointer", marginRight: "8px" }}
          title="Edit Exercise"
        />
        <TiDelete
          onClick={() => onDelete(exercise._id)}
          style={{ cursor: "pointer", marginLeft: "8px" }}
          title="Delete Exercise"
        />
      </td>
    </tr>
  );
}

export default ExerciseRow;
