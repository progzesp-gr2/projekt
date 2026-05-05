import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function ScrumMasterPage() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState([
    { id: 1, title: 'Stworzyć ekran logowania', assignedTo: ['Jan Kowalski'], status: 'W trakcie' },
  ]);

  const [newTask, setNewTask] = useState('');

  // robocza lista osób, po połączeniu z backendem do wyrzucenia
  const [teamMembers] = useState([
    { id: 'P1', name: 'Jan Kowalski' },
    { id: 'P2', name: 'Anna Nowak' },
    { id: 'P3', name: 'Piotr Zielinski' },
  ]);

  const [assignModalTaskId, setAssignModalTaskId] = useState(null);

  const handleAddTask = (e) => {
    e.preventDefault();

    if (!newTask.trim()) return;

    setTasks([
      ...tasks,
      {
        id: Date.now(),
        title: newTask,
        assignedTo: [],
        status: 'Do zrobienia',
      },
    ]);

    setNewTask('');
  };

  const handleDeleteTask = (taskId) => {
    if (!window.confirm("Czy na pewno chcesz usunąć to zadanie?")) return;
    setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
  };

  const handleToggleAssignee = (taskId, memberName) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) => {
        if (task.id !== taskId) return task;
        const isAssigned = task.assignedTo.includes(memberName);
        const updatedAssignees = isAssigned
          ? task.assignedTo.filter((name) => name !== memberName)
          : [...task.assignedTo, memberName];

        return { ...task, assignedTo: updatedAssignees };
      })
    );
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
                  <p className="text-sm opacity-60">
                    Przypisane do: {task.assignedTo.length > 0 ? task.assignedTo.join(', ') : 'Brak'}
                  </p>
                  <p className="text-sm opacity-60">Status: {task.status}</p>
                </div>
                <div className="flex flex-col gap-2 items-end">
                  <button
                    type="button"
                    onClick={() => setAssignModalTaskId(task.id)}
                    className="px-3 py-1.5 rounded-md text-sm font-medium border hover:bg-gray-100 transition-colors cursor-pointer"
                    style={{ borderColor: 'var(--border)', color: 'var(--text-h)' }}
                  >
                    Przypisz osoby
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDeleteTask(task.id)}
                    className="px-2 py-1 rounded-md text-xs text-red-500 border border-transparent hover:bg-red-100 hover:border-red-300 hover:text-red-700 transition-colors cursor-pointer"
                  >
                    Usuń
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      {assignModalTaskId && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
          <div 
            className="w-full max-w-sm p-6 rounded-xl border shadow-2xl"
            style={{ backgroundColor: 'var(--bg)', borderColor: 'var(--border)' }}
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-lg m-0" style={{ color: 'var(--text-h)' }}>
                Przypisz do zadania
              </h3>
              <button
                onClick={() => setAssignModalTaskId(null)}
                className="w-8 h-8 flex items-center justify-center rounded-md hover:bg-gray-100 transition-colors cursor-pointer opacity-50 hover:opacity-100 text-2xl"
                title="Zamknij"
                style={{ color: 'var(--text-h)' }}
              >
                &times;
              </button>
            </div>
            
            <div className="space-y-2 mb-6">
              {teamMembers.map((member) => {
                const activeTask = tasks.find((t) => t.id === assignModalTaskId);
                const isAssigned = activeTask?.assignedTo.includes(member.name);
                return (
                  <label 
                    key={member.id} 
                    className="flex items-center gap-3 p-2 rounded hover:bg-gray-50/50 cursor-pointer border border-transparent transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={isAssigned || false}
                      onChange={() => handleToggleAssignee(assignModalTaskId, member.name)}
                      className="w-4 h-4 cursor-pointer accent-blue-600"
                    />
                    <span className="font-medium text-sm">{member.name}</span>
                  </label>
                );
              })}
            </div>
            <div className="flex justify-end">
              <button
                onClick={() => setAssignModalTaskId(null)}
                className="px-6 py-2 rounded-lg font-bold text-white cursor-pointer"
                style={{ backgroundColor: 'var(--accent)' }}
              >
                Gotowe
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}