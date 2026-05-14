/**
 * To jest plik, który dostarcza backlog
 * Należy dodać endpoint do zmiany priorytetu zadania (opisałem to poniżej :) )
 */

import { useState } from 'react';

export default function BacklogTab({ projectId, programmers }) {

  const [editingTaskId, setEditingTaskId] = useState(null);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskAssignedTo, setNewTaskAssignedTo] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState('ustaw priorytet');
  const [showTaskForm, setShowTaskForm] = useState(false);

  const [tasks, setTasks] = useState([
    {
        id: 1,
        title: 'Login page',
        assignedTo: 'Jan Kowalski',
        priority: 'ustaw priorytet',
    },
    {
        id: 2,
        title: 'Dashboard UI',
        assignedTo: 'Anna Nowak',
        priority: 'poważny',
    },
    {
        id: 3,
        title: 'Fix navbar',
        assignedTo: 'Piotr Zielinski',
        priority: 'średni',
    },
  ]);

  // DLA BACKENDU wystarczy dać tu endpoint coś w stylu:
  //await axios.put('/api/task/priority', ...)
  const handlePriorityChange = (taskId, newPriority) => {
    setTasks((prevTasks) =>
        prevTasks.map((task) =>
        task.id === taskId
            ? { ...task, priority: newPriority }
            : task
        )
    );
  };

  const handleCreateTask = (e) => {

    e.preventDefault();

    if (newTaskTitle.trim() === '') return;

    const newTask = {
        id: Date.now(),
        title: newTaskTitle,
        assignedTo: newTaskAssignedTo || 'Nie przypisano',
        priority: newTaskPriority,
    };

    setTasks((prev) => [...prev, newTask]);

    // reset formularza
    setNewTaskTitle('');
    setNewTaskAssignedTo('');
    setNewTaskPriority('ustaw priorytet');

    // zamknięcie formularza
    setShowTaskForm(false);
    };

  const PRIORITIES = {
    'ustaw priorytet': { style: 'bg-gray-100 text-gray-700 border-gray-200', text: 'Ustaw Priorytet' },
    'krytyczny': { style: 'bg-red-100 text-red-700 border-red-200', text: 'Krytyczny' },
    'poważny': { style: 'bg-orange-100 text-orange-700 border-orange-200', text: 'Poważny' },
    'średni': { style: 'bg-yellow-100 text-yellow-700 border-yellow-200', text: 'Średni' },
    'neutralny': { style: 'bg-green-100 text-green-700 border-green-200', text: 'Neutralny' },
  }

  return (
    <div className="p-6">

      <div className="flex justify-between items-center mb-6">
        <h2
          className="text-2xl font-bold"
          style={{ color: 'var(--text-h)' }}
        >
          Backlog
        </h2>

        <button
            onClick={() =>
                setShowTaskForm((prev) => !prev)
            }
            className="px-4 py-2 rounded-lg text-white font-bold cursor-pointer"
            style={{ backgroundColor: 'var(--accent)' }}
            >
            {showTaskForm
                ? 'Zamknij'
                : '+ Dodaj zadanie'}
        </button>
      </div>

      {showTaskForm && (
        <form
            onSubmit={handleCreateTask}
            className="p-5 rounded-xl border mb-6"
            style={{
            backgroundColor: 'var(--code-bg)',
            borderColor: 'var(--border)',
            }}
        >

            <h3 className="font-bold mb-4">
            Dodaj nowe zadanie
            </h3>

            <input
            type="text"
            value={newTaskTitle}
            onChange={(e) =>
                setNewTaskTitle(e.target.value)
            }
            placeholder="Nazwa zadania"
            className="w-full px-4 py-2 mb-3 rounded border"
            style={{
                backgroundColor: 'var(--bg)',
                borderColor: 'var(--border)',
            }}
            />

            <select
                value={newTaskAssignedTo}
                onChange={(e) =>
                    setNewTaskAssignedTo(e.target.value)
                }
                placeholder="Osoba odpowiedzialna"
                className="w-full px-4 py-2 mb-3 rounded border"
                style={{
                    backgroundColor: 'var(--bg)',
                    borderColor: 'var(--border)',
                }}
            >
                <option value="">-</option>
                {
                    programmers.map((p) => <option key={p.id} value={p.name}>{ p.name }</option>)
                }
            </select>

            <select
            value={newTaskPriority}
            onChange={(e) =>
                setNewTaskPriority(e.target.value)
            }
            className="w-full px-4 py-2 mb-4 rounded border"
            style={{
                backgroundColor: 'var(--bg)',
                borderColor: 'var(--border)',
            }}
            >
              {
                Object.entries(PRIORITIES).map(([k, v]) => <option key={k} value={k}>{ v.text }</option>)
              }
            </select>

            <button
            type="submit"
            className="w-full py-2 rounded-lg font-bold text-white cursor-pointer"
            style={{
                backgroundColor: 'var(--accent)',
            }}
            >
            Dodaj zadanie
            </button>

        </form>
        )}

        <div className="space-y-4">

         {tasks.map((task) => (
            <div
                key={task.id}
                className="p-5 rounded-xl border flex justify-between items-center"
                style={{
                    backgroundColor: 'var(--code-bg)',
                    borderColor: 'var(--border)',
                }}
                >

                <div>
                    <h3 className="font-bold text-lg">
                    {task.title}
                    </h3>

                    <p className="text-sm opacity-60">
                    Przypisane do: {task.assignedTo}
                    </p>
                </div>

                <div className="flex items-center gap-4">

                    {/* PRIORITY */}
                    {editingTaskId === task.id ? (
                    <select
                        value={task.priority}
                        onChange={(e) =>
                        handlePriorityChange(task.id, e.target.value)
                        }
                        className="px-3 py-2 rounded border"
                        style={{
                        backgroundColor: 'var(--bg)',
                        borderColor: 'var(--border)',
                        }}
                    >
                      {
                        Object.entries(PRIORITIES).map(([k, v]) => <option key={k} value={k}>{ v.text }</option>)
                      }
                    </select>
                    ) : (
                    <span
                        className={`px-3 py-1 rounded-full text-xs font-bold border ${PRIORITIES[task.priority]?.style}`}
                    >
                        { PRIORITIES[task.priority]?.text ?? "-" }
                    </span>
                    )}

                    {/* BUTTON */}
                    {editingTaskId === task.id ? (
                    <button
                        onClick={() => setEditingTaskId(null)}
                        className="px-3 py-2 rounded text-white font-bold cursor-pointer"
                        style={{ backgroundColor: 'var(--accent)' }}
                    >
                        Zapisz
                    </button>
                    ) : (
                    <button
                        onClick={() => setEditingTaskId(task.id)}
                        className="px-3 py-2 rounded border font-bold cursor-pointer"
                        style={{
                        borderColor: 'var(--border)',
                        }}
                    >
                        Edytuj
                    </button>
                    )}

                </div>

            </div>
            ))}

        </div>
    </div>
  );
}