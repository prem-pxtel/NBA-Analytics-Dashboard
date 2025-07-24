import React, { useEffect, useState } from "react";

function UserList() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchUsers = async () => {
      const res = await fetch("http://localhost:8000/api/auth/view_users", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const data = await res.json();
      if (res.ok) {
        setUsers(data);
      } else {
        setError(data.error || "Failed to fetch users");
      }
    };

    const role = localStorage.getItem("role");
    console.log("meow", role)
    if (role === "admin") {
      fetchUsers();
    }
  }, []);

  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>User List</h2>
      <ul>
        {users.map((u) => (
          <li key={u.user_id}>
            {u.username} — <strong>{u.role}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
