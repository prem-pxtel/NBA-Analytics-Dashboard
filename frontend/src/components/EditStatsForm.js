import React, { useState } from "react";

function EditStatsForm({ playerName, gameId, onClose }) {
  const [form, setForm] = useState({
    points: "",
    assists: "",
    rebounds: "",
    blocks: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      player_name: playerName,
      game_id: gameId,
      ...Object.fromEntries(
        Object.entries(form).filter(([_, v]) => v !== "")
      ),
    };

    const res = await fetch("http://localhost:8000/api/player/update_game_stats", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (res.ok) {
      alert("Stats updated!");
      onClose();
    } else {
      alert("Error: " + data.error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Edit Stats for {playerName}</h3>
      <label>
        Points:
        <input type="number" name="points" value={form.points} onChange={handleChange} />
      </label>
      <label>
        Assists:
        <input type="number" name="assists" value={form.assists} onChange={handleChange} />
      </label>
      <label>
        Rebounds:
        <input type="number" name="rebounds" value={form.rebounds} onChange={handleChange} />
      </label>
      <label>
        Blocks:
        <input type="number" name="blocks" value={form.blocks} onChange={handleChange} />
      </label>
      <button type="submit">Submit</button>
      <button type="button" onClick={onClose}>Cancel</button>
    </form>
  );
}

export default EditStatsForm;
