import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function ProgrammerPage() {
  const navigate = useNavigate();

  const project = {
    name: 'ScrumBoard App',
    description: 'Aplikacja do zarządzania projektami scrumowymi',
    productOwner: 'Admin Admin',
    scrumMaster: 'Anna Nowak',
    members: ['Jan Kowalski', 'Anna Nowak', 'Piotr Zielinski'],
  };

  const [tasks, setTasks] = useState([
    { id: 1, title: 'Stworzyć ekran logowania', status: 'W trakcie' },
    { id: 2, title: 'Dodać walidację formularza', status: 'Do zrobienia' },
  ]);

  const handleCompleteTask = (taskId) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? { ...task, status: 'Ukończone' } : task
      )
    );
  };

  return (
    <div className="flex-1 flex flex-col p-8 text-left bg-gray-50/30">
      <header className="flex justify-between items-center mb-10">
        <div>
          <h2 className="text-2xl font-bold" style={{ color: 'var(--text-h)' }}>
            Panel Programisty
          </h2>
          <p className="text-sm opacity-60">Twoje projekty i zadania</p>
        </div>

        <button
          onClick={() => navigate('/login')}
          className="px-4 py-2 rounded-md border text-sm font-medium cursor-pointer"
          style={{ borderColor: 'var(--border)', backgroundColor: 'var(--bg)' }}
        >
          Wyloguj
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div
          className="p-6 rounded-xl border"
          style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
        >
          <h3 className="font-bold mb-3">Projekt</h3>
          <h2 className="text-xl font-bold mb-2">{project.name}</h2>
          <p className="text-sm opacity-70 mb-4">{project.description}</p>

          <p className="text-sm">
            <strong>Product Owner:</strong> {project.productOwner}
          </p>
          <p className="text-sm">
            <strong>Scrum Master:</strong> {project.scrumMaster}
          </p>

          <h4 className="font-bold mt-6 mb-2">Członkowie projektu</h4>
          <ul className="text-sm opacity-80 list-disc pl-5">
            {project.members.map((member) => (
              <li key={member}>{member}</li>
            ))}
          </ul>
        </div>

        <div
          className="p-6 rounded-xl border"
          style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
        >
          <h3 className="font-bold mb-4">Moje zadania</h3>

          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="p-4 rounded-lg border flex justify-between items-center"
                style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
              >
                <div>
                  <p className="font-bold">{task.title}</p>
                  <p className="text-sm mt-1">
                    <span className="opacity-60">Status: </span>
                    <span className={`font-medium ${task.status === 'Ukończone' ? 'text-green-500' : 'opacity-80'}`}>
                      {task.status}
                    </span>
                  </p>
                </div>
                {task.status !== 'Ukończone' && (
                  <button
                    onClick={() => handleCompleteTask(task.id)}
                    className="px-3 py-1.5 rounded-md text-xs font-bold text-white transition-opacity hover:opacity-90 cursor-pointer"
                    style={{ backgroundColor: 'var(--accent)' }}
                  >
                    Zakończ
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}