import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function ScrumMasterPage() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState([
    { id: 1, title: 'Stworzyć ekran logowania', assignedTo: 'Jan Kowalski', status: 'W trakcie' },
  ]);

  const [newTask, setNewTask] = useState('');

  const handleAddTask = (e) => {
    e.preventDefault();

    if (!newTask.trim()) return;

    setTasks([
      ...tasks,
      {
        id: Date.now(),
        title: newTask,
        assignedTo: 'Nieprzypisane',
        status: 'Do zrobienia',
      },
    ]);

    setNewTask('');
  };

  const handleDeleteTask = (taskId) => {
    if (!window.confirm("Czy na pewno chcesz usunąć to zadanie?")) return;
    setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
  };

  return (
    <div className="flex-1 flex flex-col p-8 text-left bg-gray-50/30">
      <header className="flex justify-between items-center mb-10">
        <div>
          <h2 className="text-2xl font-bold" style={{ color: 'var(--text-h)' }}>
            Panel Scrum Mastera
          </h2>
          <p className="text-sm opacity-60">Zarządzanie sprintami i zadaniami</p>
        </div>

        <button
          onClick={() => navigate('/login')}
          className="px-4 py-2 rounded-md border text-sm font-medium cursor-pointer"
          style={{ borderColor: 'var(--border)', backgroundColor: 'var(--bg)' }}
        >
          Wyloguj
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div
          className="p-6 rounded-xl border"
          style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
        >
          <h3 className="font-bold mb-4">Sprint</h3>
          <p className="text-sm opacity-70 mb-2">Aktualny sprint:</p>
          <h2 className="text-xl font-bold">Sprint 1</h2>
          <p className="text-sm opacity-60 mt-2">Status: aktywny</p>
        </div>

        <div
          className="lg:col-span-2 p-6 rounded-xl border"
          style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
        >
          <h3 className="font-bold mb-4">Zadania w sprincie</h3>

          <form onSubmit={handleAddTask} className="flex gap-3 mb-6">
            <input
              value={newTask}
              onChange={(e) => setNewTask(e.target.value)}
              placeholder="Nowe zadanie"
              className="flex-1 px-4 py-2 rounded border"
              style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
            />

            <button
              className="px-4 py-2 rounded font-bold text-white cursor-pointer"
              style={{ backgroundColor: 'var(--accent)' }}
            >
              Dodaj
            </button>
          </form>

          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="p-4 rounded-lg border flex justify-between items-start"
                style={{ borderColor: 'var(--border)', backgroundColor: 'var(--code-bg)' }}
              >
                <div>
                  <p className="font-bold">{task.title}</p>
                  <p className="text-sm opacity-60">Przypisane do: {task.assignedTo}</p>
                  <p className="text-sm opacity-60">Status: {task.status}</p>
                </div>
                <button
                  type="button"
                  onClick={() => handleDeleteTask(task.id)}
                  className="p-2 rounded-md text-red-500 hover:bg-red-50 transition-colors border border-transparent hover:border-red-100 cursor-pointer"
                  title="Usuń zadanie"
                >
                  Usuń
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}