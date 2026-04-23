// po zalogowaniu, co tutaj bedzie, zespoł, projekt, obecny sprint, przyszly i przeszly??
// jak na razie nic sensownego to nie fetchuje 


import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);


  useEffect(() => {
    const token = localStorage.getItem('access');

    if (!token) {
      navigate('/login');
      return;
    }

    fetch('http://localhost:8000/api/projects/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(res => {
        if (res.status === 401) {
          // token nie działa
          localStorage.removeItem('access');
          navigate('/login');
        }
        return res.json();
      })
      .then(data => setProjects(data))
      .catch(err => console.error(err));

  }, [navigate]);

  
  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');

    setProjects([]);

    navigate('/login');
  };

  return (
    <div className="p-6">
      <div className="flex justify-between mb-6">
        <h1 className="text-xl font-bold">Dashboard</h1>
        <button onClick={handleLogout}>
          Logout
        </button>
      </div>

      <h2 className="mb-4">Twoje projekty:</h2>

      {projects.length === 0 ? (
        <p>Brak projektów</p>
      ) : (
        <ul>
          {projects.map((project) => (
            <li key={project.id}>
              {project.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}